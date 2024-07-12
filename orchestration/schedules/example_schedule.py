# schedules/example_schedule.py
from dagster import schedule
from orchestration.jobs.example_job import example_job

@schedule(
    cron_schedule="0 0 * * *",  # This is a daily schedule at midnight
    job=example_job,
    execution_timezone="UTC",
)
def example_schedule():
    return {}
