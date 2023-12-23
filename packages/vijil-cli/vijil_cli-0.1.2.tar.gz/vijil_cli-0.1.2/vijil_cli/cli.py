import click
import requests
import json

VIGIL_API_BASE_URL = "http://dockder-test-alb-2018306447.us-west-2.elb.amazonaws.com/api/v1"
CONFIG_FILE_PATH = "vijil_config.json"

def save_config(username, token):
    config_data = {"username": username, "token": token}
    with open(CONFIG_FILE_PATH, 'w') as config_file:
        json.dump(config_data, config_file)

def load_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data.get("username"), config_data.get("token")
    except FileNotFoundError:
        return None, None

@click.group()
def main():
    """Welcome to Vijil CLI tool."""

@main.command()
def demo():
    """Demonstrate the Vijil CLI."""
    click.echo("Hello from Vijil CLI!")

@main.command()
@click.option('--username', prompt='Enter your username')
@click.option('--token', prompt='Enter your token', hide_input=True)
def configure(username, token):
    """Configure the Vijil CLI."""
    click.echo(f"Configuring with username: {username} and token: {token}")
    save_config(username, token)
    verify_url = f"{VIGIL_API_BASE_URL}/tokens/verify"
    data = {"username": username, "token": token}

    try:
        response = requests.post(verify_url, json=data)
        response.raise_for_status()

        if response.json().get("verify"):
            click.echo("Token verification successful. Configuration complete.")
        else:
            click.echo("Token verification failed. Please check your credentials.")

    except requests.exceptions.RequestException as e:
        click.echo(f"Error during API request: {e}")

if __name__ == '__main__':
    main()
