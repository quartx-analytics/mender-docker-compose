#!/usr/bin/env python3
"""
Basic script that translates inputs from github and convert them to work
with the mender artifact creation tool.
"""
from pathlib import Path
import subprocess
import argparse
import tempfile
import sys
import os

# Intercept the signing-key and convert
parser = argparse.ArgumentParser()
parser.add_argument("--signing-key", required=True)
parser.add_argument("--variables", nargs="?", const=None)
parsed_args, passthrough_args = parser.parse_known_args()

# Private key file
private_key = tempfile.NamedTemporaryFile(mode="w", delete=False)
private_key.write(parsed_args.signing_key)
private_key.close()

# Extract env variables from argument
variables = []
for env in parsed_args.variables.split(" "):
    variables.append("--env")
    variables.append(env)

try:
    subprocess.run(
        [
            os.environ["GITHUB_ACTION_PATH"] + "/docker-compose-artifact-gen",
            *passthrough_args, "--signing-key", private_key.name,
            *variables,
        ],
        check=True
    )
except subprocess.CalledProcessError as err:
    print(err.output, file=sys.stdout)
    print(err.stderr, file=sys.stderr)
    sys.exit(err.returncode)
finally:
    Path(private_key.name).unlink(missing_ok=True)

sys.exit(0)
