import typer

from rich import print
from earthscope_cli.sso import device_flow
from earthscope_sdk.user.user import get_user

app = typer.Typer()


@app.command()
def get():
    device_flow.load_tokens()
    user = get_user(device_flow.access_token)
    print(user)
