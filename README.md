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
    uses: quartx-analytics/mender-docker-compose@v1.1.2
    with:
      compose-file: "docker-compose.yml"
      software-name: "project-name"
      device-types: "raspberrypi3 raspberrypi4"
      signing-key: "${{ secrets.ARTIFACT_SIGNING_KEY }}"  # Optional
      compose-file-variables: "IMAGE_TAG=latest"  # Optional

  - name: Upload mender artifact
    uses: quartx-analytics/mender-artifact-uploader@v1.0.0
    with:
      artifact: ${{ steps.mender.outputs.artifact-file }}
      username: ${{ secrets.MENDER_USER }}
      password: ${{ secrets.MENDER_PASS }}
```
Here we specify the filename for the docker compose file, the file that contains all the details required to
build the docker container(s).
We also need to specify the software name, docker compose uses this for identifying the containers.
The device-types are the devices that this artifact will be built for. 
The artifact will not work on any other device but what is specified.
A signing-key can also be specified if required, this will ensure that the artifact has not been changed after creation.
It will also force the artifact to only work on the mender server that contains the corresponding private key.

We can then our other action that can upload the mender artifact to a mender server.
See [upload-artifact](https://github.com/actions/upload-artifact)


# Notes
For the artifact to work on mender, all mender devices need to have docker compose installed.
The `docker-compose` update module from this repo also needs to be placed in the
`/usr/share/mender/modules/v3` directory on all your mender devices.


# License
The scripts and documentation in this project are released under the [Apache License](LICENSE)
