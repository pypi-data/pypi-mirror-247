from enum import Enum


class ActiveLockReason(Enum):
    RESOLVED = "resolved"
    OFF_TOPIC = "off-topic"
    TOO_HEATED = "too heated"
    SPAM = "spam"
    OTHER = None


class AuthorAssociation(Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"
    CONTRIBUTOR = "CONTRIBUTOR"
    COLLABORATOR = "COLLABORATOR"
    FIRST_TIME_CONTRIBUTOR = "FIRST_TIME_CONTRIBUTOR"
    FIRST_TIMER = "FIRST_TIMER"
    MANNEQUIN = "MANNEQUIN"
    NONE = "NONE"


class State(Enum):
    OPEN = "open"
    CLOSED = "closed"


class RefType(Enum):
    BRANCH = "branch"
    TAG = "tag"
