from scrapers.models.big_data.spy_one import SpyOne
from scrapers.pipelines.base import SingleTablePipelineNonUpdate


class SpyOnePipeline(SingleTablePipelineNonUpdate):
    model_name = SpyOne
    unique_key = 'key'
    unique_key_columns = ['proxy']
