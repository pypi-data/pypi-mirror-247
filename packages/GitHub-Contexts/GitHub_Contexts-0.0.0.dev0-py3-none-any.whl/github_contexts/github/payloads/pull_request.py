
class PullRequestPayload(EventPayload):
    def __init__(self, payload: dict):
        super().__init__(payload=payload)
        self._payload = payload
        self._pull_request = payload["pull_request"]
        return

    @property
    def number(self) -> int:
        """Pull-request number, when then event is `pull_request`."""
        return self._payload["number"]

    @property
    def title(self) -> str:
        """Pull request title."""
        return self._pull_request["title"]

    @property
    def body(self) -> str | None:
        """Pull request body."""
        return self._pull_request["body"]

    @property
    def state(self) -> Literal["open", "closed"]:
        """Pull request state; either 'open' or 'closed'."""
        return self._pull_request["state"]

    @property
    def before(self) -> str | None:
        """
        The SHA hash of the most recent commit on the head branch before the synchronization event.

        This is only available for the 'synchronize' action.
        """
        return self._payload.get("before")

    @property
    def after(self) -> str | None:
        """
        The SHA hash of the most recent commit on the head branch after the synchronization event.

        This is only available for the 'synchronize' action.
        """
        return self._payload.get("after")

    @property
    def head(self) -> dict:
        """Pull request's head branch info."""
        return self._pull_request["head"]

    @property
    def base(self) -> dict:
        """Pull request's base branch info."""
        return self._pull_request["base"]

    @property
    def head_sha(self):
        return self.head["sha"]

    @property
    def base_sha(self) -> str:
        return self.base["sha"]

    @property
    def head_repo(self) -> dict:
        return self.head["repo"]

    @property
    def head_repo_fullname(self):
        return self.head_repo["full_name"]

    @property
    def internal(self) -> bool:
        """Whether the pull request is internal, i.e., within the same repository."""
        return self.head_repo_fullname == self.repository["full_name"]

    @property
    def label(self) -> dict | None:
        """
        The label that was added or removed from the issue.

        This is only available for the 'labeled' and 'unlabeled' events.
        """
        return self._payload.get("label")

    @property
    def label_names(self) -> list[str]:
        return [label["name"] for label in self._pull_request["labels"]]

    @property
    def merged(self) -> bool:
        """Whether the pull request is merged."""
        return self.state == "closed" and self._pull_request["merged"]
