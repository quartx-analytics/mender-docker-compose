#!/usr/bin/env python3
"""
Basic script to take the signing key in as a string and convert it to a file.
This is required as mender only accepts a file for signing the artifact.
"""
from pathlib import Path
import subprocess
import argparse
import tempfile
import pathlib
import sys
import os

# Intercept the signing-key and convert
parser = argparse.ArgumentParser()
parser.add_argument("compose_file", type=pathlib.Path)
parser.add_argument("--variables", nargs="?", const=None)
parser.add_argument("--signing-key", required=True)
parsed_args, passthrough_args = parser.parse_known_args()

# Create final compose file if given file is a compose file template
compose_file = parsed_args.compose_file
if compose_file.suffix in [".tpl", ".template"]:
    file_contents = compose_file.read_text()

    if parsed_args.variables is None:
        print("The variables argument is required when using a template file.", file=sys.stderr)
        sys.exit(1)

    # Extract variables from argument
    variables = dict(map(lambda x: x.split(":"), parsed_args.variables.split(",")))
    for key, val in variables.items():
        search_key = f"%%{key}%%"
        file_contents.replace(search_key, val)

    # Save changed docker file
    compose_file = "docker-compose.yml"
    with open(compose_file, "w") as stream:
        stream.write(file_contents)

# Private key file
private_key = tempfile.NamedTemporaryFile(mode="w", delete=False)
private_key.write(parsed_args.signing_key)
private_key.close()

try:
    subprocess.run(
        [
            os.environ["GITHUB_ACTION_PATH"] + "/docker-compose-artifact-gen",
            str(compose_file),
            *passthrough_args,
            "--signing-key", private_key.name,
        ],
        check=True
    )
finally:
    Path(private_key.name).unlink(missing_ok=True)

sys.exit(0)
