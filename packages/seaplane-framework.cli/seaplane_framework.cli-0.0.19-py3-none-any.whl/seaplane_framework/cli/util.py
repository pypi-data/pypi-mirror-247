import datetime
import os
import sys

import click
import requests
import jwt

import seaplane_framework.config
import seaplane_framework.api


def api_config():
    if not seaplane_framework.config.exists():
        click.echo(
            click.style("Configuration doesn't exist, run config init first.", fg="red")
        )
        sys.exit(1)
    config = seaplane_framework.config.read()
    current_jwt = config.current_context.options.get("jwt")
    if current_jwt is None or is_jwt_expired(current_jwt):
        refresh_jwt()
        # Reload the config after retrieving a JWT. This is preferred
        # in case some code path likes to change other things.
        config = seaplane_framework.config.read()
    configuration = seaplane_framework.api.Configuration()
    if config.current_context.options.get("carrier-api-url"):
        configuration.host = config.current_context.options["carrier-api-url"]
    configuration.access_token = config.current_context.options.get("jwt")  # type: ignore
    return configuration


def refresh_jwt():
    config = seaplane_framework.config.read()
    identity_url = (
        config.current_context.api_key.issuer_url
        or seaplane_framework.config.DEFAULT_KEY_ISSUER_URL
    )
    key = config.current_context.api_key.value
    token = "Bearer {}".format(key)
    resp = requests.request(
        "POST", identity_url, data=None, headers={"Authorization": token}
    )
    if resp.status_code == 200:
        click.echo(click.style("JWT refreshed", fg="green"), err=True)
    else:
        click.echo(
            click.style(
                "Error getting JWT with Seaplane Token ({}):".format(resp.status_code),
                fg="red",
            )
            + resp.content.decode("utf-8")
        )
        click.echo(
            click.style("  Your key may be invalid in this environment.", fg="yellow")
        )
    jwt_str = resp.content.decode()
    config.current_context.options["jwt"] = jwt_str.strip()
    seaplane_framework.config.write(config)


def is_jwt_expired(jwt_str):
    if not jwt_str:
        return True
    try:
        decoded = jwt.decode(jwt=jwt_str, options={"verify_signature": False})
        return datetime.datetime.utcnow() > datetime.datetime.utcfromtimestamp(
            decoded["exp"]
        )
    except jwt.exceptions.DecodeError:
        return True


def read_or_return_string(string_or_file):
    if string_or_file.startswith("@"):
        # File
        file_obj = sys.stdin
        if string_or_file[1:] != "-":
            file_obj = open(os.path.expanduser(string_or_file[1:]), "r")
        string_or_file = file_obj.read()
    return string_or_file


def map_nested_dicts(ob):
    if hasattr(ob, "items") and callable(ob.items):
        return {k: map_nested_dicts(v) for k, v in ob.items()}
    else:
        return ob
