# Code
- [X] Twilo-Rasa Connector
- [X] Test Locally
- [X] Create first end-to-end test
- [X] Fix TensorFlow
- [X] Bundle as Docker Compose? Or K3S?
  * Docker Compose I think is a safer choice
- [X] Reduce size of rasa instances
- [ ] Figure out what to do with handoff feature
  * Probably should be removed?
- [ ] Do not use email for username - or remove validation

# DevOps
- [X] Setup github action
  - [X] With auto-update of model
  - [X] With rasa tests
  - [X] With end-to-end test
  - [X] With audo-update of channel - will use docker-compose
- [X] Fix build errors
- [ ] Figure out why docker compose uses public IPs
- [ ] Create example.env file
- [ ] Make sure the python files from the omounted dir are being used in local environment
- [ ] Do workflow triggers to create dependencies between workflows
- [ ] Actions container did not seem to have the latest code?
- [ ] Create unique images that are public on dockerhub

# Blog
- [ ] Write blog post
- [ ] Send to Rasa team

# Docs
- [ ] Explain how to run in dev mode
- [ ] Explain how to train
- [ ] Explain how to deploy

# Testing
- [ ] How do I get the twilio audio recording in the payload