"""Unit tests for the changelog routes."""

import unittest
from unittest.mock import Mock

from routes.changelog import get_report_changelog, get_subject_changelog, get_metric_changelog, get_source_changelog


class ChangeLogTest(unittest.TestCase):
    """Unit tests for getting the changelog."""

    def setUp(self):
        self.database = Mock()
        self.database.sessions.find_one.return_value = dict(user="Jenny")

    def test_get_changelog(self):
        """Test that the changelog is returned."""
        report1 = dict(timestamp="1", delta=dict(description="delta1"))
        report2 = dict(timestamp="2", delta=dict(description="delta2"))
        self.database.reports.find.return_value = [report2, report1]
        self.database.measurements.find.return_value = []
        self.assertEqual(
            dict(changelog=[dict(delta="delta2", timestamp="2"), dict(delta="delta1", timestamp="1")]),
            get_report_changelog("report_uuid", "10", self.database))

    def test_get_changelog_with_measurements(self):
        """Test that the changelog is returned."""
        report1 = dict(timestamp="1", delta=dict(description="delta1"))
        measurement2 = dict(delta="delta2", start="2")
        report3 = dict(timestamp="3", delta=dict(description="delta3"))
        self.database.reports.find.return_value = [report3, report1]
        self.database.measurements.find.return_value = [measurement2]
        self.assertEqual(
            dict(
                changelog=[
                    dict(delta="delta3", timestamp="3"), dict(delta="delta2", timestamp="2"),
                    dict(delta="delta1", timestamp="1")]),
            get_report_changelog("report_uuid", "10", self.database))

    def test_get_subject_changelog(self):
        """Test that the changelog can be limited to a specific subject."""
        report1 = dict(timestamp="1", delta=dict(description="delta1"))
        report2 = dict(timestamp="2", delta=dict(description="delta2"))
        self.database.reports.find.return_value = [report2, report1]
        self.database.measurements.find.return_value = []
        self.assertEqual(
            dict(changelog=[dict(delta="delta2", timestamp="2"), dict(delta="delta1", timestamp="1")]),
            get_subject_changelog("report_uuid", "subject_uuid", "10", self.database))

    def test_get_metric_changelog(self):
        """Test that the changelog can be limited to a specific metric."""
        report1 = dict(timestamp="1", delta=dict(description="delta1"))
        report2 = dict(timestamp="2", delta=dict(description="delta2"))
        self.database.reports.find.return_value = [report2, report1]
        self.database.measurements.find.return_value = []
        self.assertEqual(
            dict(changelog=[dict(delta="delta2", timestamp="2"), dict(delta="delta1", timestamp="1")]),
            get_metric_changelog("report_uuid", "metric_uuid", "10", self.database))

    def test_get_source_changelog(self):
        """Test that the changelog can be limited to a specific source."""
        report1 = dict(timestamp="1", delta=dict(description="delta1"))
        report2 = dict(timestamp="2", delta=dict(description="delta2"))
        self.database.reports.find.return_value = [report2, report1]
        self.database.measurements.find.return_value = []
        self.assertEqual(
            dict(changelog=[dict(delta="delta2", timestamp="2"), dict(delta="delta1", timestamp="1")]),
            get_source_changelog("report_uuid", "metric_uuid", "10", self.database))
