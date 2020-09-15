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
  * Build
    * docker context use default
    * docker-compose -f docker/docker-compose.yml build
  * Push
    * docker-compose -f docker/docker-compose.yml push
  * Deploy
    * docker compose -f docker/docker-compose.yml up