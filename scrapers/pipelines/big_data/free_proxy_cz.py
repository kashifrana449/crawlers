from scrapers.models.big_data.free_proxy_cz import FreeProxyCZ
from scrapers.pipelines.base import SingleTablePipelineNonUpdate


class FreeProxyCZPipeline(SingleTablePipelineNonUpdate):
    model_name = FreeProxyCZ
    unique_key = 'key'
    unique_key_columns = ['ip', 'port', 'protocol']
