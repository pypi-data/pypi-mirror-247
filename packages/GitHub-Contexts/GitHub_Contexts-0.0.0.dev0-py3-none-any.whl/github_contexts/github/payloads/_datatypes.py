from repodynamics.actions.contexts.enums import ActiveLockReason


class IssueData:
    """
    The `issue` object contained in the payload of the `issues` and `issue_comment` events.
    """

    def __init__(self, issue: dict):
        """
        Parameters
        ----------
        issue : dict
            The `issue` dictionary contained in the payload.
        """
        self._issue = issue
        return

    @property
    def active_lock_reason(self) -> ActiveLockReason:
        return ActiveLockReason(self._issue.get("active_lock_reason"))


