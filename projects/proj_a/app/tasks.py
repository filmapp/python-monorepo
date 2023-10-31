import subprocess

import uvicorn
from typer import Typer

app = Typer()


@app.command()
def dev() -> None:
    uvicorn.run("app.main:app", port=8080, reload=True)


@app.command()
def build() -> None:
    subprocess.run(
        ["docker", "build", "--file=Dockerfile", "--tag=proj_a", "../.."],
        check=True,
    )


if __name__ == "__main__":
    app()
