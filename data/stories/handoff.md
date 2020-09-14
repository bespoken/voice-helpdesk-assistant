## handoff
* human_handoff
  - utter_ask_handoff
  - action_handoff_options
* trigger_handoff
  - action_handoff

## handoff
* human_handoff
  - utter_ask_handoff
  - action_handoff_options
* trigger_handoff{"handoff_to":"financial_demo"}
  - action_handoff

## handoff deny
* human_handoff
  - utter_ask_handoff
  - action_handoff_options
* deny
  - utter_ask_whatelse

## New Story

* greet
    - utter_greet
    - utter_help
* open_incident
    - open_incident_form
    - form{"name":"open_incident_form"}
    - slot{"requested_slot":"email"}
* problem_email{"email":"jpk@bespoken.io"}
    - slot{"email":"jpk@bespoken.io"}
    - open_incident_form
    - slot{"email":"jpk@bespoken.io"}
    - slot{"requested_slot":"priority"}
* inform{"priority":"medium"}
    - slot{"priority":"medium"}
    - open_incident_form
    - slot{"priority":"medium"}
    - slot{"requested_slot":"problem_description"}
* deny{"priority":"flow"}
    - slot{"priority":"flow"}
    - open_incident_form
    - slot{"priority":null}
    - slot{"requested_slot":"priority"}
* inform{"priority":"high"}
    - slot{"priority":"high"}
    - open_incident_form
    - slot{"priority":"high"}
    - slot{"requested_slot":"problem_description"}
* deny
    - action_default_fallback
* out_of_scope
    - open_incident_form
    - slot{"problem_description":"there is a problem"}
    - slot{"requested_slot":"incident_title"}
* open_incident
    - open_incident_form
    - slot{"incident_title":"Bad problem"}
    - slot{"requested_slot":"confirm"}
* affirm
    - open_incident_form
    - slot{"confirm":true}
    - slot{"previous_email":"jpk@bespoken.io"}
    - form{"name":null}
    - slot{"requested_slot":null}
