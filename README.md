# Mender Docker Compose Artifact
This action allows you to create mender artifacts to deploy docker containers using docker compose.
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
    uses: actions/mender-docker-compose@v1
    with:
      compose-file: "docker-compose.yml"
      software-name: "project-name"

  - name: Upload mender artifact
    uses: actions/upload-artifact@v2
    with:
      name: project-artifact
      path: ${{ steps.mender.outputs.artifact-file }}
```
Here we specify the filename for the docker compose file that contains
all the details needed to build the docker containers.
We also need to specify the software name as this is used by docker compose to mark the containers.

GitHub's upload-artifact action can be used to upload to created artifact to github.

## Where does the upload go?
At the bottom of the workflow summary page, there is a dedicated section for artifacts.

# License
The scripts and documentation in this project are released under the [Apache License](LICENSE)
