import click
import time

from ploomber_core.exceptions import modify_exceptions

from ploomber_cloud import api, zip_
from ploomber_cloud.config import PloomberCloudConfig

STATUS_COLOR = {
    "active": "yellow",
    "finished": "green",
    "success": "green",
    "pending": "white",
    "failed": "red",
    "stopped": "magenta",
}

INTERVAL_SECS = 15.0
TIMEOUT_MINS = 15.0


def _unpack_job_status(job):
    """
    Format and output a job status message.
    Return job status (and URL if success).

    Parameters
    ----------
    job: JSON
        Contains job status information to output and process.

    Returns
    ----------
    job_status: str
        Status of job. Possible values: "success", "running", or "failed".

    app_url: str
        URL to view dashboard. Only returned if job_status == "success".
    """
    tasks = job["summary"]
    status_msg = []

    for name, status in tasks:
        status_msg.append(f"{name}: {click.style(status, fg=STATUS_COLOR[status])} | ")

    click.echo("".join(status_msg))

    # First, check if job failed during docker build or deploy
    docker_status = job["status"]

    # Case 1: If docker_status == "finished", job failed during docker build/deploy.
    if docker_status == "finished":
        return "failed", None

    # If job hasn't failed during docker build/deploy, it has moved onto webservice.
    if "task_status" in job:
        web_status = job["task_status"]
        url_status = job["resources"]["is_url_up"]

        # Case 2: If web_status == "stopped", then job failed during webservice.
        if web_status == "stopped":
            return "failed", None

        # Case 3: If web_status == "running" and url_status == True, job has succeeded.
        elif web_status == "running" and url_status is True:
            return "success", job["resources"]["webservice"]

    # Remaining possible cases mean job is still running:

    # Case 4: docker_status == "running" and job not moved onto webservice:
    #   Docker build/deploy still in progress.

    # Case 5: web_status == "running" and url_status == False:
    #   Webservice still in progress.

    return "running", None


def _watch(client, project_id, job_id):
    start_time = time.time()
    interval = INTERVAL_SECS
    timeout = 60.0 * TIMEOUT_MINS

    # poll every 'interval' secs until 'timeout' mins
    while True:
        curr_time = time.time()
        time_diff = curr_time - start_time

        if time_diff >= timeout:
            click.secho("Timeout reached.", fg="yellow")
            return

        curr_time_formatted = time.strftime("%H:%M:%S", time.localtime(curr_time))
        click.echo(f"[{curr_time_formatted}]:")

        # get job status from API and send it to be formatted/output
        job = client.get_job_by_id(job_id)
        job_status, app_url = _unpack_job_status(job)

        status_page = api.PloomberCloudEndpoints().status_page(project_id, job_id)

        # deploy has either succeeded or failed
        if job_status != "running":
            click.secho(f"Deployment {job_status}.", fg=STATUS_COLOR[job_status])
            click.echo(f"View project dashboard: {status_page}")
            if job_status == "success":
                click.echo(f"View your deployed app: {app_url}")
            break

        time.sleep(interval - (time_diff % interval))


@modify_exceptions
def deploy(watch):
    """Deploy a project to Ploomber Cloud, requires a project to be initialized"""
    client = api.PloomberCloudClient()
    config = PloomberCloudConfig()
    config.load()

    with zip_.zip_app(verbose=True) as path_to_zip:
        click.echo("Deploying...")
        output = client.deploy(
            path_to_zip=path_to_zip,
            project_type=config.data["type"],
            project_id=config.data["id"],
        )
        if watch:
            _watch(client, output["project_id"], output["id"])
