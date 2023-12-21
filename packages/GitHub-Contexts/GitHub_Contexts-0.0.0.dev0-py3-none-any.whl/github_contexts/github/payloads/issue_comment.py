
class IssueCommentPayload(EventPayload):
    def __init__(self, payload: dict):
        super().__init__(payload=payload)
        return

    @property
    def action(self) -> Literal[
        WorkflowTriggeringAction.CREATED, WorkflowTriggeringAction.EDITED, WorkflowTriggeringAction.DELETED
    ]:
        """Comment action type that triggered the event."""
        return WorkflowTriggeringAction(self._payload["action"])

    @property
    def comment(self) -> dict:
        """Comment data."""
        return self._payload["comment"]

    @property
    def issue(self) -> dict:
        """Issue data."""
        return self._payload["issue"]

    @property
    def author_association(
        self,
    ) -> Literal[
        "COLLABORATOR",
        "CONTRIBUTOR",
        "FIRST_TIMER",
        "FIRST_TIME_CONTRIBUTOR",
        "MANNEQUIN",
        "MEMBER",
        "NONE",
        "OWNER",
    ]:
        return self.comment["author_association"]

    @property
    def body(self) -> str:
        """Contents of the issue comment."""
        return self.comment["body"]

    @property
    def id(self) -> int:
        """Unique identifier of the comment."""
        return self.comment["id"]

    @property
    def commenter_username(self) -> str:
        """Commenter username."""
        return self.comment["user"]["login"]

    @property
    def is_pull_comment(self) -> bool:
        """Whether the comment is on a pull request (True) or an issue (False)."""
        return bool(self.comment.get("pull_request"))