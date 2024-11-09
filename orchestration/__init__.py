from dagster import Definitions, load_assets_from_modules
from .assets import example_asset, rainforest_asset
from .jobs import rainforest_job, example_assets_job
from .schedules import rainforest_schedule, example_schedule
from .resources.example_resource import example_resource

# Load all assets
all_assets = load_assets_from_modules([example_asset, rainforest_asset])

# Define the Dagster definitions
defs = Definitions(
    assets=[*all_assets],
    jobs=[rainforest_job, example_assets_job],
    schedules=[rainforest_schedule, example_schedule],
    resources={
        "example_resource": example_resource
    }
)
