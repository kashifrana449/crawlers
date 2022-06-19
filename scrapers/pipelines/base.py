class BasePipeline(object):
    __abstract__ = True
    model_name = None
    buffer = list()
    buffer_busy = list()
    buffer_size = 50

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        if self.buffer:
            self.model_name.bulk_save_with_ignore(self.buffer)
            self.buffer = list()

    def process_item(self, item, spider):
        pass

    def create_data(self, item, model_class, excluded_columns=[]):

        columns = [column for column in model_class.__table__.columns.keys() if column not in excluded_columns]

        data = dict()
        for column in columns:
            data[column] = item.get(column)

        return data

    def add_with_ignore(self, data, model):
        if len(self.buffer) < self.buffer_size:
            self.buffer.append(data)
        else:
            model.bulk_save_with_ignore(self.buffer)
            self.buffer = list()
            self.buffer.append(data)


class SingleTablePipeline(BasePipeline):
    model_name = None

    excluded_columns = ['id', 'createdDate', 'created', 'modified']

    def process_item(self, item, spider):
        data = self.create_data(item, model_class=self.model_name, excluded_columns=self.excluded_columns)
        self.add_with_ignore(data=data, model=self.model_name)


class SingleTablePipelineNonUpdate(BasePipeline):
    model_name = None
    excluded_columns = ['id', 'createdDate', 'created', 'modified']
    unique_key = None
    unique_key_columns = None
    exist_in_db = {}

    # def add_update(self, ):

    def get_key_value(self, item):
        return ';'.join([item.get(x, '') for x in self.unique_key_columns])

    def open_spider(self, spider):
        super().open_spider(spider)
        records = self.model_name.query.with_entities(getattr(self.model_name, self.unique_key)).all()
        if records:
            records = list(list(zip(*records))[0])
            self.exist_in_db = dict(zip(records, [True]*len(records)))

    def process_item(self, item, spider):
        super().process_item(item, spider)
        key = self.get_key_value(item)
        crime = self.exist_in_db.get(key, '')
        if not crime:
            item[self.unique_key] = self.get_key_value(item)
            data = self.create_data(item, model_class=self.model_name, excluded_columns=self.excluded_columns)
            self.add_with_ignore(data=data, model=self.model_name)
            self.exist_in_db[key] = True
        else:
            data = self.create_data(item, model_class=self.model_name, excluded_columns=self.excluded_columns)
            record = self.model_name.query.filter(getattr(self.model_name, self.unique_key) == key).first()
            self.model_name.update(data, record)


class BasePCPipeline(BasePipeline):
    parent_class = None
    child_class = None

    parent_unique_key = None
    child_foreign_key = None
    excluded_columns = ['id', 'createdDate', 'created', 'modified']

    parent_exist_item_db = []

    def open_spider(self, spider):
        self.parent_exist_item_db = dict(self.parent_class.query.with_entities(
            getattr(self.parent_class, self.parent_unique_key), getattr(self.parent_class, 'id')))

    def close_spider(self, spider):
        if self.buffer:
            self.child_class.bulk_save_with_ignore(self.buffer)
            self.buffer = list()

    def process_item(self, item, spider):
        data = self.create_data(model_class=self.parent_class, item=item, excluded_columns=self.excluded_columns)
        parent_id = self.parent_exist_item_db.get(item.get(self.parent_unique_key))
        if parent_id:
            parent_data = self.parent_class.query.filter(self.parent_class.id == parent_id)
            self.parent_class.update(data, parent_data)
        else:
            parent_data = self.parent_class(**data)
            self.parent_class.save(parent_data)
            parent_id = parent_data.id
            self.parent_exist_item_db[item.get(self.parent_unique_key)] = parent_id
        data = self.create_data(model_class=self.child_class, item=item, excluded_columns=self.excluded_columns)
        data[self.child_foreign_key] = parent_id
        child_data = self.child_class(**data)
        self.add_with_ignore(model=self.child_class, data=data)


