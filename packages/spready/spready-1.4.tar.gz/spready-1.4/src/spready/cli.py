import typer
from spready import app, EnvURLS
import json
import os


cliApp = typer.Typer()


@cliApp.command()
def register(credential_path: str):
    result = app.register(EnvURLS.PROD)
    with open(credential_path, "w") as f:
        json.dump(result, f)
    print(f"""
          
        ┌───────────────────────────────────────────────┐
        │  Congratulations!                             │
        │                                               │
        │  You've successfully registered your worker   │
        └───────────────────────────────────────────────┘
          
          URL: {EnvURLS.PROD}
          Use `{result['publicKey']}` in API header `x-auth-token` to authenticate

        """)


@cliApp.command()
def run(creditial_path: str, module_path: str):
    print(f"Setting path: {module_path}")
    print(os.getcwd())
    app.run(creditial_path, modulePath=module_path)


if __name__ == "__main__":
    cliApp()