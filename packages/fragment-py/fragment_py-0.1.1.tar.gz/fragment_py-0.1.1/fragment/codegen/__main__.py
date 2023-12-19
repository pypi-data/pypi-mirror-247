import typer
from rich import print
from typing_extensions import Annotated

from fragment import Fragment
from fragment.codegen.generator import generate_code

app = typer.Typer()


@app.command()
def run(
    schema_path: Annotated[str, typer.Option("--schema-path")],
    destination: Annotated[str, typer.Option("--destination")],
) -> None:
    print(f"Generating entry types for schema {schema_path}")
    fragment = Fragment(schema_path)
    generated_loc = generate_code(
        fragment.schema.key, fragment.schema.entries, fragment.schema.accounts
    )
    print(f"Writing generated code to {destination}")
    with open(destination, "w") as f:
        f.write(generated_loc)


if __name__ == "__main__":
    app()
