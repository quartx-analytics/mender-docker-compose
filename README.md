# Mender Docker Compose Artifact
This action allows you to create artifacts to deploy docker containers to mender devices using docker compose.


Refer [mender](https://mender.io/)

# Usage
See [action.yml](action.yml)

See [upload-artifact](https://github.com/actions/upload-artifact)


### Create Artifact
```yaml
steps:
  - uses: actions/checkout@v2

  - id: mender
    name: Create mender artifact
    uses: quartx-analytics/mender-docker-compose@1.0.1
    with:
      compose-file: "docker-compose.yml"
      software-name: "project-name"
      device-types: "raspberrypi3 raspberrypi4"
      signing-key: "${{ secrets.ARTIFACT_SIGNING_KEY }}"  # Optional

  - name: Upload mender artifact
    uses: actions/upload-artifact@v2
    with:
      name: mender-artifacts
      path: ${{ steps.mender.outputs.artifact-file }}
```
Here we specify the filename for the docker compose file, the file that contains all the details required to
build the docker container(s).
We also need to specify the software name as docker compose uses this for identifying the containers.
The device-types are the devices that this artifact will be built for. 
The artifact will not work on any other devices but what is specified.
A signing-key can also be specified if required, this will ensure that the artifact has not been changed after creation.
It will also force the artifact to only work on the mender server that contains the corresponding private key.

GitHub's upload-artifact action can then be used to upload the created artifact to GitHub.


## Where does the upload go?
At the bottom of the workflow summary page, there is a dedicated section for artifacts.


# Notes
For the artifact to work on mender, all mender devices need to have docker compose installed.
The docker-compose update module from this repo also needs to be placed in the
`/usr/share/mender/modules/v3` directory on all your mender devices.

# License
The scripts and documentation in this project are released under the [Apache License](LICENSE)
