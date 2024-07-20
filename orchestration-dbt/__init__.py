from dagster import Definitions, Config
from typing import List
from pydantic import Field
from pathlib import Path
import os
from dagster_dbt import DbtCliResource, build_schedule_from_dbt_selection, dbt_assets, DagsterDbtTranslatorSettings, DagsterDbtTranslator

# Define the path to the dbt project within your Docker environment
dbt_project_dir = Path(__file__).joinpath("..", "..", "dbt_project").resolve()
dbt = DbtCliResource(project_dir=os.fspath(dbt_project_dir))
dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")

dagster_dbt_translator = DagsterDbtTranslator(settings=DagsterDbtTranslatorSettings(enable_asset_checks=True))

# Create a Pydantic model to configure dbt run options
class MyDbtConfig(Config):
    full_refresh:  bool      = Field(default=False     , description="Flag to indicate if a full refresh.")
    exclude:       bool      = Field(default=True      , description="Flag to determine if certain tags or models should be excluded.")
    exclude_tag:   List[str] = Field(default=["static"], description="List of tags to exclude. Write in bullet points.")
    exclude_model: List[str] = Field(default=[""]      , description="List of models to exclude. Write in bullet points.")
    select_tag:    List[str] = Field(default=[""]      , description="List of tags to include. Write in bullet points.")
    select_model:  List[str] = Field(default=[""]      , description="List of models to include. Write in bullet points.")

@dbt_assets(
        manifest=dbt_manifest_path
        ,dagster_dbt_translator=dagster_dbt_translator
        )
def dbt_assets(context, config: MyDbtConfig):
    #Set variables (strip space for strings)
    dbt_build_args = ["build"]
    full_refresh = config.full_refresh
    exclude = config.exclude
    exclude_tag_string = " ".join(f"tag:{tag.strip()}" for tag in config.exclude_tag if tag.strip() != "")
    exclude_model_string = " ".join(model.strip() for model in config.exclude_model if model.strip() != "")
    select_tag_string = " ".join(f"tag:{tag.strip()}" for tag in config.select_tag if tag.strip() != "")
    select_model_string = " ".join(model.strip() for model in config.select_model if model.strip() != "")
    #Check conditions
    if full_refresh:
        dbt_build_args += ["--full-refresh"]
    if exclude and (exclude_tag_string or exclude_model_string):
        dbt_build_args += ["--exclude", exclude_tag_string, exclude_model_string]
    if select_tag_string or select_model_string:
        dbt_build_args += ["--select", select_tag_string, select_model_string]
        dbt_build_args = [arg for arg in dbt_build_args if arg != ""] #Remove empty strings from args list
        yield from dbt.cli(dbt_build_args, manifest=dbt_manifest_path).stream()
    else:
        dbt_build_args = [arg for arg in dbt_build_args if arg != ""]
        yield from dbt.cli(dbt_build_args, context=context).stream() #Remove empty strings from args list

# Define a schedule to run dbt assets daily
daily_dbt_schedule = build_schedule_from_dbt_selection(
    [dbt_assets],
    cron_schedule="0 8 * * *",  # Scheduled to run daily at 8:00 AM
    job_name="daily_dbt_models",
    dbt_exclude="tag:static"
)

# Define a schedule to run dbt assets monthly
monthly_dbt_schedule = build_schedule_from_dbt_selection(
    [dbt_assets],
    dbt_exclude="tag:static",
    dbt_select="tag:monthly",
    cron_schedule="0 13 1 * *",  # Scheduled to run on the first day of each month at 1:00 PM
    job_name="monthly_dbt_models"
)

defs = Definitions(
    assets=[dbt_assets],
    schedules=[daily_dbt_schedule, monthly_dbt_schedule]
)
