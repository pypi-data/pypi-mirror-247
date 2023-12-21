class PushPayload(EventPayload):
    def __init__(self, payload: dict):
        super().__init__(payload=payload)
        self._payload = payload
        return

    @property
    def action(
        self,
    ) -> Literal[
        WorkflowTriggeringAction.CREATED, WorkflowTriggeringAction.DELETED, WorkflowTriggeringAction.EDITED
    ]:
        """Push action type."""
        if self._payload["created"]:
            return WorkflowTriggeringAction.CREATED
        if self._payload["deleted"]:
            return WorkflowTriggeringAction.DELETED
        return WorkflowTriggeringAction.EDITED

    @property
    def head_commit(self) -> dict:
        return self._payload["head_commit"]

    @property
    def head_commit_message(self) -> str:
        return self.head_commit["message"]

    @property
    def before(self) -> str:
        """The SHA hash of the most recent commit on the branch before the event."""
        return self._payload["before"]

    @property
    def after(self) -> str:
        """The SHA hash of the most recent commit on the branch after the event."""
        return self._payload["after"]

