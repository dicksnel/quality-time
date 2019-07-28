"""OpenVAS metric collector."""

from typing import List
from xml.etree.ElementTree import Element  # nosec, Element is not available from defusedxml, but only used as type

from dateutil.parser import isoparse
import requests

from utilities.type import Value, Entities
from utilities.functions import days_ago, parse_source_response_xml
from .source_collector import SourceCollector


class OpenVASSecurityWarnings(SourceCollector):
    """Collector to get security warnings from OpenVAS."""

    def parse_source_responses_value(self, responses: List[requests.Response]) -> Value:
        tree = parse_source_response_xml(responses[0])
        return str(len(self.results(tree)))

    def parse_source_responses_entities(self, responses: List[requests.Response]) -> Entities:
        tree = parse_source_response_xml(responses[0])
        return [dict(key=result.attrib["id"], name=result.findtext("name", default=""),
                     description=result.findtext("description", default=""),
                     host=result.findtext("host", default=""), port=result.findtext("port", default=""),
                     severity=result.findtext("threat", default=""))
                for result in self.results(tree)]

    def results(self, element: Element) -> List[Element]:
        """Return the results that have one of the severities specified in the parameters."""
        severities = self.parameter("severities")
        results = element.findall(".//results/result")
        return [result for result in results if result.findtext("threat", default="").lower() in severities]


class OpenVASSourceUpToDateness(SourceCollector):
    """Collector to collect the OpenVAS report age."""

    def parse_source_responses_value(self, responses: List[requests.Response]) -> Value:
        tree = parse_source_response_xml(responses[0])
        report_datetime = isoparse(tree.findtext("creation_time", default=""))
        return str(days_ago(report_datetime))