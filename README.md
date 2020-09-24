# Rasa Voice Helpdesk Assistant Example

This is a Rasa example demonstrating how to build a Voice AI assistant for an IT Helpdesk. It uses Twilio Voice as a channel to handle customer support requests. Below is an example conversation, showing the bot helping a user open a support ticket and query its status. You can use this bot as a starting point for building customer service assistants or as a template for collecting required pieces of information from a user before making an API call.

Here is an example of a conversation you can have with this bot:

![Screenshot](./docs/CallFlow.gif?raw=true)


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Setup](#setup)
  - [Create A Twilio Voice Project](#create-a-twilio-voice-project)
  - [Environment Configuration](#environment-configuration)
  - [Running Rasa Locally](#running-rasa-locally)
- [What It Does](#what-it-does)
  - [Trying out the bot](#trying-out-the-bot)
  - [Things you can ask the bot](#things-you-can-ask-the-bot)
  - [Example conversations](#example-conversations)
- [Testing the bot](#testing-the-bot)
- [CI/CD](#cicd)
  - [AWS Deployment](#aws-deployment)
  - [Continuous Integration](#continuous-integration)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Setup
### Create A Twilio Voice Project
Follow the directions in our blog post for setting up a Twilio Voice project:
LINK_TO_BLOG_POST

### Environment Configuration
Make a copy of the file `example.env` and save it as `.env`.

Add the Twilio Account SID and Twilio Auth Token from your Twilio Voice project.

### Running Rasa Locally

In an environment with Docker installed, run:
```
docker compose up
```

This will start the entire environment, which includes the following containers:

| Container | Description |
| *** | *** |
| rasa | The primary Rasa instance, including the custom channel for handling Twilio Voice |
| action | The custom Action handler for the Rasa application |
| duckling | Parses text into structured data |

## What It Does
### Trying out the bot
While the docker compose application is running, run the following:
```
docker exec rasa rasa train
```

Then start and stop the Rasa container to reload the model:
```
docker compose restart
```

To run the shell, enter the following:
```bash
docker compose run rasa shell --debug
```

Note that `--debug` mode will produce a lot of output meant to help you understand how the bot is working
under the hood. You can also add this flag to the action server command. To simply talk to the bot, you can remove this flag.

### Things you can ask the bot

The bot has two main skills:
1. Opening an incident in ServiceNow.
2. Checking the status of incidents in ServiceNow by email address of the caller. It will prompt the user to re-use previously provided (during the chat session) email addresses, if any exist.
For the purposes of illustration, the bot recognizes the following as requests to open an incident:

1. Asking to open an incident directly e.g. "I want to open an incident"
2. Asking about a problem resetting their password e.g. "I can't reset my password"
3. Asking about a problem with outlook/email e.g. "I can't log in to my outlook"

Take a look at `data/nlu.md` to see what the bot is currently trained to recognize.

It can also respond to requests for help (e.g. "help me").

If configured, the bot can also hand off to another bot in response to the user asking for handoff. More [details on handoff](#handoff) below.

### Example conversations

With `localmode=true`:

```
Bot loaded. Type a message and press enter (use '/stop' to exit):
Your input ->  hi
    Hello!
    I can help you open a service request ticket, or check the status of your open incidents.
    You can ask me things like:
    - Open an incident
    - Help me reset my password
    - I'm having a issue with my email
    - What's the status of the ticket I opened?
Your input ->  i have a problem with my email
    What is your email address?
Your input ->  anything@example.com
    ? What is the priority of this issue?
Your input -> 1: low (/inform{"priority":"low"})
    What is the problem description for the issue?
Your input ->  Can't log in to my email
    ? Should I open an incident with the following details?
    email: anything@example.com
    problem description: Can't log in to my email
    title: Problem with email
Your input -> priority: low  1: Yes (/affirm)
    An incident with the following details would be opened if ServiceNow was connected:
    email: anything@example.com
    problem description: Can't log in to my email
    title: Problem with email
    priority: low
Your input ->  thanks. Can i check the status of my other tickets?
    Would you like to use the last email address you used, anything@example.com?
Your input ->  Yes please
    Since ServiceNow isn't connected, I'm making this up!
    The most recent incident for anything@example.com is currently awaiting triage
```

With `localmode=false`:

With a Service Now instance connected, it will check if the email address is in the instance database and provide an incident number for the final response:

```
Your input ->  help me reset my password
    What is your email address?
Your input ->  idontexist@example.com
    Sorry, "idontexist@example.com" isn't in our incident management system. Please try again.
    What is your email address?
Your input ->  abraham.lincoln@example.com
    ? What is the priority of this issue?
Your input -> 3: high (/inform{"priority":"high"})
    What is the problem description for the issue?
Your input ->  Password stuck in a loop
    ? Should I open an incident with the following details?
    email: abraham.lincoln@example.com
    problem description: Password stuck in a loop
    title: Problem resetting password
    priority: high
Your input ->  1: Yes (/affirm)
    Successfully opened up incident INC0010008 for you.  Someone will reach out soon.
Your input ->  Can I check the status of my tickets?
    Would you like to use the last email address you used, abraham.lincoln@example.com?
Your input ->  Yes please
    Incident INC0010002: "Email Log in problem", opened on 2020-05-21 09:57:06 is currently in progress
    Incident INC0010008: "Problem resetting password", opened on 2020-05-21 12:12:49 is currently awaiting triage
Your input ->  thanks
    You're welcome!
```

## Testing the bot

You can test the bot on the test conversations by running  `rasa test`. This will test the core NLU and dialog model for the bot from run the [tests](https://rasa.com/docs/rasa/user-guide/testing-your-assistant/#end-to-end-testing) on the conversations in `tests/conversation_tests.md`.


To run a complete end-to-end test for the bot, install the Bespoken CLI:
```
npm install bespoken-tools -g
```

And run the end-to-end tests with the command:
```
bst test --config tests/testing.json
```

This will run tests [from here](tests/e2e.yml) that do the following:
* Call our Twilio endpoint (just a real person would)
* Interact with our bot via voice
* Capture the audio responses from the bot and compare to expected responses

To learn more about Bespoken IVR testing, [read here](https://bespoken.io/end-to-end/ivr).

## CI/CD
### AWS Deployment
To deploy the bot to AWS, we recommend using the Docker ECS Integration:  
https://docs.docker.com/engine/context/ecs-integration/

Follow the directions to setup the Docker support for ECS, as well as configure the AWS CLI.

Once you have set it up, just run these commands:
```
docker context use <ECS_CONTEXT>
docker compose up
```

That's all there is to it! Your fully configured Rasa instance will be setup and accessible via the new load balance created by Docker Compose.

### Continuous Integration
There are five Github Action workflows configured with this project.

| Workflow | Description | Trigger |
|---|---|---|
| deploy | Automatically deploys to ECS a new version of the Rasa instance, Action server, and Duckling server | Tags with `rasa-*` |
| e2e | Runs Bespoken End-To-End tests | Automatically run after the `train` or `deploy` workflows |
| lint | Lints the custom Python code in our project | With an push that touches *.py files |
| test | Runs the `rasa test` command | Whenever the code or model changes |
| train | Trains the model, and automatically deploys to S3 to be loaded by the running Rasa instance | Whenever the model changes |

