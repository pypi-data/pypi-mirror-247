from ruamel.yaml import YAML

from repodynamics.actions.contexts.enums import RefType


class GitHubContext:
    """
    The 'github' context of the workflow run.

    It contains information about the workflow run and the event that triggered the run.

    References
    ----------
    - [GitHub Docs](https://docs.github.com/en/actions/learn-github-actions/contexts#github-context)
    """

    def __init__(self, context: dict):
        self._token = context.pop("token")
        self._context = dict(sorted(context.items()))
        return

    def __str__(self):
        return YAML(typ=["rt", "string"]).dumps(self._context, add_final_eol=True)

    @property
    def event_name(self) -> str:
        """The name of the triggering event, e.g. 'push', 'pull_request' etc."""
        return self._context["event_name"]

    @property
    def ref(self) -> str:
        """
        The fully formed reference of the branch or tag that triggered the workflow run,
        e.g. 'refs/heads/main', 'refs/tags/v1.0' etc.

        Notes
        -----
        For workflows triggered by push, this is the branch or tag ref that was pushed.
        For workflows triggered by pull_request, this is the pull request merge branch.
        For workflows triggered by release, this is the release tag created.
        For other triggers, this is the branch or tag ref that triggered the workflow run.
        This is only set if a branch or tag is available for the event type.
        The ref given is fully-formed, meaning that for branches the format is refs/heads/<branch_name>,
        for pull requests it is refs/pull/<pr_number>/merge,
        and for tags it is refs/tags/<tag_name>.
        """
        return self._context["ref"]

    @property
    def ref_name(self) -> str:
        """The short reference name of the branch or tag that triggered the event, e.g. 'main', 'dev/1' etc."""
        return self._context["ref_name"]

    @property
    def ref_type(self) -> RefType:
        """The type of the ref that triggered the event, either 'branch' or 'tag'."""
        return RefType(self._context["ref_type"])

    @property
    def base_ref(self):
        return self._context["base_ref"]

    @property
    def head_ref(self):
        return self._context["head_ref"]

    @property
    def repo_fullname(self) -> str:
        """Full name of the repository, i.e. <owner_username>/<repo_name>, e.g., 'RepoDynamics/RepoDynamics'"""
        return self._context["repository"]

    @property
    def repo_name(self) -> str:
        """Name of the repository, e.g., 'RepoDynamics'."""
        return self.repo_fullname.removeprefix(f"{self.repo_owner}/")

    @property
    def repo_owner(self) -> str:
        """GitHub username of the repository owner."""
        return self._context["repository_owner"]

    @property
    def sha(self) -> str:
        """The SHA hash of the most recent commit on the branch that triggered the workflow.

        The value of this commit SHA depends on the event that triggered the workflow.
        For more information, see References.

        References
        ----------
        - [GitHub Docs: Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
        """
        return self._context["sha"]

    @property
    def token(self) -> str:
        """
        A token to authenticate on behalf of the GitHub App installed on your repository.

        This is functionally equivalent to the GITHUB_TOKEN secret.
        """
        return self._token



class ContextManager:
    def __init__(self, github_context: dict):
        payload_manager = {
            "issues": IssuesPayload,
            "push": PushPayload,
            "issue_comment": IssueCommentPayload,
            "pull_request": PullRequestPayload,
        }
        payload = github_context.pop("event")
        self._github = GitHubContext(context=github_context)
        event_name = self.github.event_name
        if event_name not in payload_manager:
            raise ValueError(f"Unsupported event name: {event_name}")
        self._payload = payload_manager[event_name](payload=payload)
        return

    @property
    def github(self) -> GitHubContext:
        """The 'github' context of the workflow run."""
        return self._github

    @property
    def payload(self) -> EventPayload:
        """The full webhook payload of the triggering event."""
        return self._payload

    @property
    def target_repo_fullname(self) -> str:
        return (
            self.payload.head_repo_fullname
            if self.github.event_name == "pull_request"
            else self.github.repo_fullname
        )

    @property
    def target_branch_name(self) -> str:
        return self.github.base_ref if self.github.event_name == "pull_request" else self.github.ref_name

    @property
    def ref_is_main(self) -> bool:
        return self.github.ref == f"refs/heads/{self.payload.repository_default_branch}"

    @property
    def hash_before(self) -> str:
        """The SHA hash of the most recent commit on the branch before the event."""
        if self.github.event_name == "push":
            return self.payload.before
        if self.github.event_name == "pull_request":
            return self.payload.before or self.payload.base_sha
        return self.github.sha

    @property
    def hash_after(self) -> str:
        """The SHA hash of the most recent commit on the branch after the event."""
        if self.github.event_name == "push":
            return self.payload.after
        if self.github.event_name == "pull_request":
            return self.payload.after or self.payload.head_sha
        return self.github.sha
