from dagster import ScheduleDefinition
from ..jobs import rainforest_job, example_assets_job

# Define schedules
rainforest_schedule = ScheduleDefinition(
    job=rainforest_job,
    cron_schedule="0 5 * * *",  # Runs daily at 5 AM
    name="rainforest_daily_schedule"
)

example_schedule = ScheduleDefinition(
    job=example_assets_job,
    cron_schedule="0 */4 * * *",  # Runs every 4 hours
    name="example_assets_schedule"
)
