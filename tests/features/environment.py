"""Code to run before and after certain events during testing."""

import time
from typing import Dict

import requests


def before_all(context):
    """Create shortcuts to send requests to the server API."""

    def cookies():
        """Return the cookies."""
        return dict(session_id=context.session_id) if context.session_id else {}

    def get(api, headers=None):
        """Get the resource."""
        if context.report_date:
            api += f"?report_date={context.report_date}"
        context.response = response = requests.get(f"{context.base_api_url}/{api}", headers=headers)
        return response.json() if response.headers.get('Content-Type') == "application/json" else response

    def post(api, json=None):
        """Post the resource."""
        context.response = response = requests.post(f"{context.base_api_url}/{api}", json=json, cookies=cookies())
        if not response.ok:
            return response
        if "session_id" in response.cookies:
            context.session_id = response.cookies["session_id"]
        time.sleep(1)  # Give server and database time to process the previous request
        return response.json()

    def delete(api):
        """Delete the resource."""
        context.response = response = requests.delete(f"{context.base_api_url}/{api}", cookies=cookies())
        time.sleep(1)  # Give server and database time to process the previous request
        return response.json()

    context.base_api_url = "http://localhost:5001/api/v3"
    context.session_id = None
    context.report_date = None
    context.response = None
    context.uuid: Dict[str, str] = {}  # Keep track of the most recent uuid per item type
    context.get = get
    context.post = post
    context.delete = delete


def before_step(context, step):
    """Make the step available in the context."""
    context.step = step
