"""Pyup.io Safety metrics collector."""

from typing import List

import requests

from utilities.type import Entities, Value
from .source_collector import SourceCollector


class PyupioSafetySecurityWarnings(SourceCollector):
    """Pyup.io Safety collector for security warnings."""
    PACKAGE, AFFECTED, INSTALLED, VULNERABILITY, KEY = range(5)

    def parse_source_responses_value(self, responses: List[requests.Response]) -> Value:
        return str(len(responses[0].json()))

    def parse_source_responses_entities(self, responses: List[requests.Response]) -> Entities:
        """Return a list of warnings."""
        return [
            dict(key=warning[self.KEY], package=warning[self.PACKAGE], installed=warning[self.INSTALLED],
                 affected=warning[self.AFFECTED], vulnerability=warning[self.VULNERABILITY])
            for warning in responses[0].json()]