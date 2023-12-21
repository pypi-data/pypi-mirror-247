import click

from src.commands.base import cli
from src.config import ConfigManager


@cli.group()
def config():
    pass


@config.command(name="set")
@click.option('--server', '-s', help="Server url")
@click.option('--token', '-t', help="Account token")
def set_config(server, token):
    config_info = ConfigManager.read_config()
    if server:
        config_info.server_url = server
    if token:
        config_info.token = token
    ConfigManager.save_config(server_url=config_info.server_url, token=config_info.token)
    print("Success: config")


@config.command(name="show")
def show_config():
    config_info = ConfigManager.read_config()
    print(f"Server: {config_info.server_url}")
    print(f"Token: {config_info.token}")
