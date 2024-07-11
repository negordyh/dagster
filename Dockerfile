# Dagster
FROM python:3.8-slim as dagster

# Update and upgrade the system packages
RUN apt-get update && apt-get upgrade -yqq

# Set an environment variable for Dagster's home directory
ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# Create the Dagster home directory
RUN mkdir -p $DAGSTER_HOME

# Set the working directory to Dagster's home
WORKDIR $DAGSTER_HOME

# Copy necessary files into the working directory
COPY requirement.txt dagster.yaml workspace.yaml .env $DAGSTER_HOME

# Install the dependencies from the requirements file
RUN pip install -r requirement.txt

# Copy the project directories into the container
COPY /orchestration $DAGSTER_HOME/orchestration
# COPY /orchestration-dbt $DAGSTER_HOME/orchestration-dbt
# COPY /dbt_project $DAGSTER_HOME/dbt_project

# Expose port 3000 for web access
EXPOSE 3000

# Define the command to run the Dagster webserver
CMD ["sh", "-c", "dagster-webserver -h 0.0.0.0 -p 3000 & dagster-daemon run"]

