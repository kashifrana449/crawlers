from scrapers.models.big_data.free_proxy import FreeProxy
from scrapers.pipelines.base import SingleTablePipelineNonUpdate


class FreeProxyPipeline(SingleTablePipelineNonUpdate):
    model_name = FreeProxy
    unique_key = 'key'
    unique_key_columns = ['ip', 'port']
