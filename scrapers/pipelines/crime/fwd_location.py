from scrapers.models.crime.family_watch_dog import FamilyWatchDogLocation
from scrapers.pipelines.base import SingleTablePipelineNonUpdate


class FWDLocationPipeline(SingleTablePipelineNonUpdate):
    model_name = FamilyWatchDogLocation
    unique_key = 'location'
