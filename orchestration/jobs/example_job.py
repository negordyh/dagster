# jobs/example_job.py
from dagster import job

from ..assets.example_asset import example_asset, dependent_asset

@job
def example_job():
    example_asset()
    dependent_asset(example_asset())
