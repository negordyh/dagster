from dagster import define_asset_job, AssetSelection
from ..assets.rainforest_asset import *
from ..assets.example_asset import *

# Define jobs for both asset sets
rainforest_job = define_asset_job(
    "rainforest_job",
    selection=AssetSelection.assets(fetch_amazon_product_data)
)

example_assets_job = define_asset_job(
    "example_assets_job",
    selection=AssetSelection.assets(example_asset, dependent_asset)
)
