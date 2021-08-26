#!/usr/bin/env python3
"""
Basic script to take the signing key in as a string and convert it to a file.
This is required as mender only accepts a file for signing the artifact.
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
parsed_args, passthrough_args = parser.parse_known_args()

# Private key file
private_key = tempfile.NamedTemporaryFile(mode="w", delete=False)
private_key.write(parsed_args.signing_key)
private_key.close()

try:
    subprocess.run(
        [
            os.environ["GITHUB_ACTION_PATH"] + "/docker-compose-artifact-gen",
            *passthrough_args,
            "--signing-key", private_key.name,
        ],
        check=True
    )
finally:
    Path(private_key.name).unlink(missing_ok=True)
sys.exit(0)
