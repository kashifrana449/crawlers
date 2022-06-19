from scrapers.pipelines.base import SingleTablePipelineNonUpdate
from scrapers.models.crime.family_watch_dog import FWDCrimes


class FWDCrimePipeline(SingleTablePipelineNonUpdate):
    model_name = FWDCrimes
    unique_key = 'key'
    unique_key_columns = ['aid']
