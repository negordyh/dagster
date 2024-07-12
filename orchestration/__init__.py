# __init__.py
from dagster import Definitions, load_assets_from_modules

from orchestration.assets import example_asset
from orchestration.jobs.example_job import example_job
from orchestration.schedules.example_schedule import example_schedule
from orchestration.resources.example_resource import example_resource

all_assets = load_assets_from_modules([example_asset])

defs = Definitions(
    assets=[*all_assets],
    jobs=[example_job],
    schedules=[example_schedule],
    resources={
        "example_resource": example_resource,
    }
)
