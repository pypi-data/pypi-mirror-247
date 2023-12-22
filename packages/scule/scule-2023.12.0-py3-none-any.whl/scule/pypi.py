import click
import pandas as pd
import requests
import html2text
import re


@click.command()
@click.option(
    "-i",
    "--input",
    prompt="Input Excel file",
    default="Input.xlsx",
    help="Input Excel file.",
)
@click.option(
    "-o",
    "--output",
    prompt="Output Excel file",
    default="Output.xlsx",
    help="Output Excel file.",
)
@click.option(
    "-r",
    "--re-check",
    is_flag=True,
    show_default=True,
    default=False,
    help="Re-Check entries of interrest.",
)
def search(input: str, output: str, re_check: bool) -> None:
    """Simple program to check wether a package name ist available on PyPI."""
    df = pd.read_excel(input)

    for index, row in df.iterrows():
        print(row.iloc[0], row.iloc[1], row.iloc[2])
        if re_check and row.iloc[2] == "yes":
            row.iloc[1] = "nan"

        if row.iloc[1] == "nan":
            response = requests.get(f"https://pypi.org/simple/{row.iloc[0]}/")
            if response.status_code == 200:
                row.iloc[1] = True
            else:
                row.iloc[1] = False

            print(index, row.iloc[0], row.iloc[1])

    df.to_excel(output, "Output", index=False)


@click.command()
@click.option(
    "-o",
    "--output",
    prompt="Output Excel file",
    default="List.xlsx",
    help="Output Excel file.",
)
def list(output: str) -> None:
    """Get a list of all packages on PyPI."""

    df = pd.DataFrame()
    pattern = "\\[(.*?)\\]"

    response = requests.get(f"https://pypi.org/simple/")
    if response.status_code == 200:
        text = html2text.html2text(response.text)
        result = re.findall(pattern, text)

        df = pd.DataFrame({"Pakete": result})

    else:
        print("Webpage could not be loaded")

    df.to_excel(output, "List", index=False)


if __name__ == "__main__":
    search()
