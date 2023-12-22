import datetime
import json
import pprint
import sys

import click
import tabulate
import yaml

import seaplane_framework.api
from seaplane_framework.api.models import Flow
from seaplane_framework.api.apis.tags import flow_api
from seaplane_framework.cli import util
from seaplane_framework.common import sse
from seaplane_framework.common import spinner


@click.group()
def flow():
    """Seaplane Flows"""


@flow.command(name="list")
@click.option("--region")
def list_flows(region):
    """list all flows"""
    configuration = util.api_config()
    if not configuration:
        return
    with seaplane_framework.api.ApiClient(configuration) as api_client:
        api_instance = flow_api.FlowApi(api_client)
        query_params = {}
        if region:
            query_params["region"] = region
        try:
            api_response = api_instance.list_flows(
                query_params=query_params,  # type: ignore
            )
            for flow in api_response.body:
                print(flow)
        except seaplane_framework.api.ApiException as e:
            click.echo(
                click.style(
                    "Exception when calling FlowApi->list_flows: %s\n" % e, fg="red"
                )
            )


@flow.command()
@click.argument("flow_name")
@click.option(
    "--flow",
    "-f",
    help="Flow definition JSON/YAML, @ to load a file, @- for stdin",
    required=True,
)
@click.option("--region")
def create(flow_name, flow, region):
    """create a flow"""
    configuration = util.api_config()
    if not configuration:
        return
    flow_definition = util.read_or_return_string(flow)
    # JSON is valid YAML...
    flow_definition_obj = yaml.safe_load(flow_definition)
    print(flow_definition_obj)
    with seaplane_framework.api.ApiClient(configuration) as api_client:
        api_instance = flow_api.FlowApi(api_client)
        path_params = {"flow_name": flow_name}
        query_params = {}
        if region:
            query_params["region"] = region
        try:
            _ = api_instance.create_flow(
                path_params=path_params,  # type: ignore
                query_params=query_params,  # type: ignore
                body=Flow(**flow_definition_obj),
            )
        except seaplane_framework.api.ApiException as e:
            click.echo(
                click.style(
                    "Exception when calling FlowApi->create_flow: %s\n" % e, fg="red"
                )
            )


@flow.command()
@click.argument("flow_name")
@click.option("--region")
def delete(flow_name, region):
    """delete a flow"""
    configuration = util.api_config()
    if not configuration:
        return
    with seaplane_framework.api.ApiClient(configuration) as api_client:
        api_instance = flow_api.FlowApi(api_client)
        path_params = {"flow_name": flow_name}
        query_params = {}
        if region:
            query_params["region"] = region
        try:
            _ = api_instance.delete_flow(
                path_params=path_params,  # type: ignore
                query_params=query_params,  # type: ignore
            )
        except seaplane_framework.api.ApiException as e:
            click.echo(
                click.style(
                    "Exception when calling FlowApi->delete_flow: %s\n" % e, fg="red"
                )
            )


@flow.command()
@click.argument("flow_name")
@click.option("--region")
def details(flow_name, region):
    """show details of flow (configuration)"""
    configuration = util.api_config()
    if not configuration:
        return
    with seaplane_framework.api.ApiClient(configuration) as api_client:
        api_instance = flow_api.FlowApi(api_client)
        path_params = {"flow_name": flow_name}
        query_params = {}
        if region:
            query_params["region"] = region
        try:
            resp = api_instance.get_flow(
                path_params=path_params,  # type: ignore
                query_params=query_params,  # type: ignore
            )
            pprint.pprint(util.map_nested_dicts(resp.body))
        except seaplane_framework.api.ApiException as e:
            click.echo(
                click.style(
                    "Exception when calling FlowApi->get_flow: %s\n" % e, fg="red"
                )
            )


@flow.command(name="list-secrets")
@click.argument("flow_name")
@click.option("--region")
def list_secrets(flow_name, region):
    """list all flow secrets"""
    configuration = util.api_config()
    if not configuration:
        return
    # Enter a context with an instance of the API client
    with seaplane_framework.api.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = flow_api.FlowApi(api_client)

        path_params = {
            "flow_name": flow_name,
        }
        query_params = {}
        if region:
            query_params["region"] = region
        try:
            # List all secrets
            api_response = api_instance.list_secrets(
                path_params=path_params,  # type: ignore
                query_params=query_params,  # type: ignore
            )
            unnested = util.map_nested_dicts(api_response.body)
            table = []
            for key, value in unnested.items():
                row = []
                row.append(key)
                row.append(value["destination"])
                row.append(value["hash"])
                row.append(
                    datetime.datetime.fromtimestamp(
                        float(value["timestamp"]) / 1000000000.0
                    )
                )
                table.append(row)
                print(
                    tabulate.tabulate(
                        table, headers=("secret", "destination", "hash", "timestamp")
                    )
                )
        except seaplane_framework.api.ApiException as e:
            click.echo(
                click.style(
                    "Exception when calling FlowApi->list_secrets: %s\n" % e, fg="red"
                )
            )


@flow.command(name="set-secret")
@click.argument("flow_name")
@click.argument("secret_name")
@click.option(
    "--destination",
    default="all",
    help="destination for secret (all|carrier-io|processor)",
    type=click.Choice(("all", "carrier-io", "processor")),
)
@click.option("--region")
def set_secret(flow_name, secret_name, destination, region):
    """set or create secret value for a flow"""
    configuration = util.api_config()
    if not configuration:
        return
    with seaplane_framework.api.ApiClient(configuration) as api_client:
        api_instance = flow_api.FlowApi(api_client)
        path_params = {
            "flow_name": flow_name,
            "secret_name": secret_name,
        }
        query_params = {}
        if region:
            query_params["region"] = region
        value = click.prompt("Value for {}".format(secret_name), hide_input=True)
        body = {"destination": destination, "value": value}
        try:
            # Set the secret value
            _ = api_instance.set_secret(
                path_params=path_params,  # type: ignore
                query_params=query_params,  # type: ignore
                body=body,  # type: ignore
            )
        except seaplane_framework.api.ApiException as e:
            click.echo(
                click.style(
                    "Exception when calling FlowApi->set_secret: %s\n" % e, fg="red"
                )
            )


@flow.command(name="delete-secret")
@click.argument("flow_name")
@click.argument("secret_name")
@click.option("--region")
def delete_secret(flow_name, secret_name, region):
    """delete a flow secret"""
    configuration = util.api_config()
    if not configuration:
        return
    with seaplane_framework.api.ApiClient(configuration) as api_client:
        api_instance = flow_api.FlowApi(api_client)
        path_params = {
            "flow_name": flow_name,
            "secret_name": secret_name,
        }
        query_params = {}
        if region:
            query_params["region"] = region
        try:
            # Set the secret value
            _ = api_instance.delete_secret(
                path_params=path_params,  # type: ignore
                query_params=query_params,  # type: ignore
            )
        except seaplane_framework.api.ApiException as e:
            click.echo(
                click.style(
                    "Exception when calling FlowApi->delete_secret: %s\n" % e, fg="red"
                )
            )


@flow.command(name="log")
@click.argument("flow_name")
@click.option("--offset")
@click.option("--utc", is_flag=True, default=False)
def flow_log(flow_name, offset, utc):
    """get/tail flow logs"""
    configuration = util.api_config()
    if not configuration:
        return
    headers = {"Authorization": "Bearer " + str(configuration.access_token)}
    if offset:
        headers["Last-Event-ID"] = offset
    event_source = sse.EventSource(
        configuration.host + f"/flow/{flow_name}/events",
        encoding="utf-8",
        headers=headers,
    )
    iterator = iter(event_source)
    # Simplest way to get local timezone. Do here once (rather than repeatedly below).
    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    while True:
        with spinner.Context():
            event = next(iterator)
            if event.event == "stderr":
                out = sys.stderr
            else:
                out = sys.stdout
            if event.data is None:
                continue
            try:
                log_event = json.loads(event.data)  # type:ignore
                if "date" in log_event:
                    unixts = log_event["date"]
                    dt = datetime.datetime.fromtimestamp(unixts, datetime.timezone.utc)
                    if not utc:
                        dt = dt.astimezone(local_tz)
                    out.write("[{}] ".format(dt.strftime("%Y-%m-%d %H:%M:%S %Z")))
                out.write(log_event["log"])
                out.flush()
            except json.decoder.JSONDecodeError:
                out.write(event.data)  # type:ignore
                out.flush()
