from dagster import Definitions, load_assets_from_modules

from .assets import example_asset
# from .jobs import example_job
# from .schedules import example_schedule
from .resources import example_resource


all_assets = load_assets_from_modules([example_asset])

defs = Definitions(
    assets=[*all_assets],
    # jobs=[example_job],
    # schedules=[example_schedule],
    resources={
        "example_resource": example_resource,
    }
)