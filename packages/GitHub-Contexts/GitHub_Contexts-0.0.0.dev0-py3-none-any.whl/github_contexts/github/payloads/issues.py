class IssuesPayload(EventPayload):
    def __init__(self, payload: dict):
        super().__init__(payload=payload)
        self._payload = payload
        self._issue = payload["issue"]
        return

    @property
    def author(self) -> dict:
        return self._issue["user"]

    @property
    def author_association(
        self,
    ) -> Literal[
        "OWNER",
        "MEMBER",
        "COLLABORATOR",
        "CONTRIBUTOR",
        "FIRST_TIMER",
        "FIRST_TIME_CONTRIBUTOR",
        "MANNEQUIN",
        "NONE",
    ]:
        return self._issue["author_association"]

    @property
    def author_username(self) -> str:
        return self.author["login"]

    @property
    def title(self) -> str:
        """Title of the issue."""
        return self._issue["title"]

    @property
    def body(self) -> str | None:
        """Contents of the issue."""
        return self._issue["body"]

    @property
    def comments_count(self) -> int:
        return self._issue["comments"]

    @property
    def label(self) -> dict | None:
        """
        The label that was added or removed from the issue.

        This is only available for the 'labeled' and 'unlabeled' events.
        """
        return self._payload.get("label")

    @property
    def labels(self) -> list[dict]:
        return self._issue["labels"]

    @property
    def label_names(self) -> list[str]:
        return [label["name"] for label in self.labels]

    @property
    def node_id(self) -> str:
        return self._issue["node_id"]

    @property
    def number(self) -> int:
        return self._issue["number"]

    @property
    def state(self) -> Literal["open", "closed"]:
        return self._issue["state"]
