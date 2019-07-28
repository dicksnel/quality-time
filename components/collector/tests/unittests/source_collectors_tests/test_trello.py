"""Unit tests for the Trello metric source."""

from datetime import datetime

from .source_collector_test_case import SourceCollectorTestCase


class TrelloTestCase(SourceCollectorTestCase):
    """Base class for testing Trello collectors."""

    def setUp(self) -> None:
        super().setUp()
        self.sources = dict(
            source_id=dict(
                type="trello",
                parameters=dict(
                    url="http://trello",
                    board="board1",
                    api_key="abcdef123",
                    token="4533dea",
                    inactive_days="30",
                    lists_to_ignore=[])))


class TrelloIssuesTest(TrelloTestCase):
    """Unit tests for the Trello issue metric."""

    def setUp(self):
        super().setUp()
        self.metric = dict(type="issues", addition="sum", sources=self.sources)

    def test_issues(self):
        """Test that the number of issues and the individual issues are returned."""
        cards = dict(
            id="board1", url="http://trello/board1",
            cards=[
                dict(
                    id="card1", name="Card 1", idList="list1", due=None, dateLastActivity="2019-01-01",
                    url="http://trello/card1")],
            lists=[dict(id="list1", name="List 1")])
        json = [[dict(id="board1", name="Board1")], cards, cards, cards]
        response = self.collect(self.metric, get_request_json_side_effect=json)
        self.assert_value("1", response)
        self.assert_entities(
            [dict(
                key="card1", url="http://trello/card1", title="Card 1", list="List 1", due_date=None,
                date_last_activity="2019-01-01")],
            response)

    def test_issues_with_ignored_list(self):
        """Test that lists can be ignored when counting issues."""
        self.metric["sources"]["source_id"]["parameters"]["lists_to_ignore"] = ["list1"]
        cards = dict(
            id="board1", url="http://trello/board1",
            cards=[
                dict(
                    id="card1", name="Card 1", idList="list1", due=None, dateLastActivity="2019-01-01",
                    url="http://trello/card1"),
                dict(
                    id="card2", name="Card 2", idList="list2", due=None, dateLastActivity="2019-01-01",
                    url="http://trello/card2")],
            lists=[dict(id="list1", name="List 1"), dict(id="list2", name="List 2")])
        json = [[dict(id="board1", name="Board1")], cards, cards, cards]
        response = self.collect(self.metric, get_request_json_side_effect=json)
        self.assert_value("1", response)
        self.assert_entities(
            [dict(key="card2", url="http://trello/card2", title="Card 2", list="List 2",
                  due_date=None, date_last_activity="2019-01-01")],
            response)

    def test_overdue_issues(self):
        """Test overdue issues."""
        self.metric["sources"]["source_id"]["parameters"]["cards_to_count"] = ["overdue"]
        cards = dict(
            id="board1", url="http://trello/board1",
            cards=[
                dict(
                    id="card1", name="Card 1", idList="list1", due=None, dateLastActivity="2019-01-01",
                    url="http://trello/card1"),
                dict(
                    id="card2", name="Card 2", idList="list1", due="2019-01-01", dateLastActivity="2019-01-01",
                    url="http://trello/card2")],
            lists=[dict(id="list1", name="List 1")])
        json = [[dict(id="board1", name="Board1")], cards, cards, cards]
        response = self.collect(self.metric, get_request_json_side_effect=json)
        self.assert_value("1", response)
        self.assert_entities(
            [dict(key="card2", url="http://trello/card2", title="Card 2", list="List 1",
                  due_date="2019-01-01", date_last_activity="2019-01-01")],
            response)

    def test_inactive_issues(self):
        """Test inactive issues."""
        self.metric["sources"]["source_id"]["parameters"]["cards_to_count"] = ["inactive"]
        cards = dict(
            id="board1", url="http://trello/board1",
            cards=[
                dict(
                    id="card1", name="Card 1", idList="list1", due=None,
                    dateLastActivity=datetime.now().isoformat(), url="http://trello/card1"),
                dict(
                    id="card2", name="Card 2", idList="list1", due=None, dateLastActivity="2019-01-01",
                    url="http://trello/card2")],
            lists=[dict(id="list1", name="List 1")])
        json = [[dict(id="board1", name="Board1")], cards, cards, cards]
        response = self.collect(self.metric, get_request_json_side_effect=json)
        self.assert_value("1", response)
        self.assert_entities(
            [dict(key="card2", url="http://trello/card2", title="Card 2", list="List 1", due_date=None,
                  date_last_activity="2019-01-01")],
            response)


class TrelloSourceUpToDatenessTest(TrelloTestCase):
    """Unit tests for the Trello source up-to-dateness metric."""

    def setUp(self):
        super().setUp()
        self.metric = dict(type="source_up_to_dateness", addition="max", sources=self.sources)
        self.cards = dict(
            id="board1", url="http://trello/board1",
            dateLastActivity="2019-02-10",
            cards=[
                dict(id="card1", name="Card 1", idList="list1", dateLastActivity="2019-03-03"),
                dict(id="card2", name="Card 2", idList="list2", dateLastActivity="2019-01-01")],
            lists=[dict(id="list1", name="List 1"), dict(id="list2", name="List 2")])
        self.side_effect = [[dict(id="board1", name="Board1")], self.cards, self.cards]

    def test_age(self):
        """Test that the source up to dateness is the number of days since the most recent change."""
        response = self.collect(self.metric, get_request_json_side_effect=self.side_effect)
        self.assert_value(str((datetime.now() - datetime(2019, 3, 3)).days), response)

    def test_age_with_ignored_lists(self):
        """Test that lists can be ignored when measuring the source up to dateness."""
        self.metric["sources"]["source_id"]["parameters"]["lists_to_ignore"] = ["list1"]
        response = self.collect(self.metric, get_request_json_side_effect=self.side_effect)
        self.assert_value(str((datetime.now() - datetime(2019, 2, 10)).days), response)