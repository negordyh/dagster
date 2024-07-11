from dagster import asset

@asset
def example_asset():
    return "This is an example asset"

@asset
def dependent_asset(example_asset):
    return f"This asset depends on: {example_asset}"