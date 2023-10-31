from typer import Typer

app = Typer()


@app.command()
def hello() -> None:
    print("hello")


if __name__ == "__main__":
    app
