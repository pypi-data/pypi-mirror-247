from ruamel.yaml import YAML


class EventPayload:
    """
    The full webhook payload of the triggering event.

    References
    ----------
    - [GitHub Docs](https://docs.github.com/en/webhooks/webhook-events-and-payloads)
    """

    def __init__(self, payload: dict):
        self._payload = dict(sorted(payload.items()))
        return

    def __str__(self):
        return YAML(typ=["rt", "string"]).dumps(self._payload, add_final_eol=True)

    @property
    def action(self) -> WorkflowTriggeringAction | None:
        action = self._payload.get("action")
        if not action:
            return None
        return WorkflowTriggeringAction(action)

    @property
    def repository(self) -> dict:
        """The repository on GitHub where the event occurred."""
        return self._payload["repository"]

    @property
    def sender(self) -> dict:
        """The GitHub user that triggered the event."""
        return self._payload["sender"]

    @property
    def repository_default_branch(self) -> str:
        return self.repository["default_branch"]

    @property
    def sender_username(self) -> str:
        """GitHub username of the user or app that triggered the event."""
        return self.sender["login"]

    @property
    def sender_email(self) -> str:
        return f"{self.sender['id']}+{self.sender_username}@users.noreply.github.com"