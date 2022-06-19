from scrapers.models.real_estate.re_nz import ReNz, RENzPricing
from scrapers.pipelines.base import BasePCPipeline


class ReNzPipeline(BasePCPipeline):
    parent_class = ReNz
    child_class = RENzPricing

    parent_unique_key = 'propertyId'
    child_foreign_key = 'propertyKey'
