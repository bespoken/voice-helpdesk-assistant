# Setting up container dev
* Remote containers extension
* Using python image
* Add .devcontainer/devcontainer.json

## For New Developers
* Selected "Remote-Containers: Clone Repository in Container Volume..."
* Selected my repo
* python -m venv venv
* source venv/bin/activate
* Do normal setup:
  * pip install -r requirements.txt
  * pip install -r requirements-dev.txt
  * pre-commit install

## Gotchas
* Rebuild container - lost the installation stuff on the container :-(
  * repo changes were preserved though - what happened?
  * Make sure to use virtual environments
* Did not seem to work well with Python 3.8
* Duckling is in a separate vm, which requires networking between containers :-(
  * Create a docker network
  * Added my containers to the network
  * Updated my config to point at the Duckling container
  * Did a `rasa train` to make the config changes take effect
  * 

# Setting up Pyenv dev
* Install pyenv:
  * https://gist.github.com/monkut/35c2ef098b871144b49f3f9979032cee
  * Install tools for building
  * Install pyenv
  * Did the .bashrc stuff
* Install 3.7.9: pyenv install 3.7.9
* Create virtual environment: pyenv virtualenv 3.7.9 venv
* Activate environemnt: pyenv activate venv
* Do regular install stuff:
  * pip install -r requirements.txt
  * pip install -r requirements-dev.txt
  * rasa train

* Install Rasa X
  * pip3 install rasa-x --extra-index-url https://pypi.rasa.com/simple
  
* Start it up - three windows
  * rasa run actions
  * docker run -p 8000:8000 rasa/duckling
  * rasa shell --debug

* Running a connector
  * Need to do `rasa run`

  ## Gotchas
  * Erros with tensorflow

  # Setting up ECS With Docker Compose
  * Install docker compose ecs
    * https://docs.docker.com/engine/context/ecs-integration/
    * aws configure
  * created token for dockerhub access
    * docker secret create dockerhubAccessToken --username <dockerhubuser>  --password <dockerhubtoken>
  * Setup
    * docker context create rasa
  * Build
    * docker context use default
    * docker-compose -f docker/docker-compose-ecs.yml build
  * Push
    * docker-compose -f docker/docker-compose-ecs.yml push
  * Deploy
    * docker context use rasa
    * export $(grep -v '^#' .env | xargs)
    * docker compose -f docker/docker-compose-ecs.yml up


# Model Updates
## Curl Command
export MODEL_FILE=`ls -Art models | tail -n 1`
curl --location --request PUT 'http://localhost:5005/model' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "model_file": "'"$MODEL_FILE"'",
    "remote_storage": "aws"
  }'


# Github Dispatch
curl \
  -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -u USER:TOKEN \
  https://api.github.com/repos/jkelvie/helpdesk-assistant/dispatches \
  -d '{"event_type":"deploy_model"}'