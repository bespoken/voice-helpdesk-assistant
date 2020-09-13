# Setting up container dev
* Remote containers extension
* Using python image
* Add .devcontainer/devcontainer.json

# For New Developers
* Selected "Remote-Containers: Clone Repository in Container Volume..."
* Selected my repo
* python -m venv venv
* source venv/bin/activate
* Do normal setup:
  * pip install -r requirements.txt
  * pip install -r requirements-dev.txt
  * pre-commit install

# Gotchas
* Rebuild container - lost the installation stuff on the container :-(
  * repo changes were preserved though - what happened?
  * Make sure to use virtual environments
* Did not seem to work well with Python 3.8
* Duckling is in a separate vm, which requires networking between containers :-(