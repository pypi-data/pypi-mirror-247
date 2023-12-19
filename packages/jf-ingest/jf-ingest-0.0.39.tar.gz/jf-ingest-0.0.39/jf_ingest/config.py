import enum
import tempfile
from dataclasses import dataclass, field
from datetime import datetime

from dateutil import parser

from jf_ingest.utils import format_datetime_to_ingest_timestamp

JELLYFISH_API_BASE = "https://app.jellyfish.co"


class JiraAuthMethod(enum.Enum):
    BasicAuth = 1
    AtlassianConnect = 2


# Needs to subclass str to be serializable
class IngestionType(str, enum.Enum):
    AGENT = "AGENT"
    DIRECT_CONNECT = "DIRECT_CONNECT"


@dataclass
class IssueMetadata:
    id: str
    key: str
    updated: datetime
    project_id: str = (
        None  # NOTE: This field is optionally set, and generally only used for detected re-keys
    )
    # The following fields are used for detecting redownloads
    epic_link_field_issue_key: str = None
    parent_field_issue_key: str = None
    parent_id: str = None

    def __post_init__(self):
        """Post Init is called here to properly type everything by doing typecasts"""
        self.id = str(self.id)
        self.key = str(self.key)
        self.updated = (
            self.updated if isinstance(self.updated, datetime) else parser.parse(self.updated)
        )

        # Sanity recasts to make sure everything is a string
        if self.project_id:
            self.project_id = str(self.project_id)
        if self.epic_link_field_issue_key:
            self.epic_link_field_issue_key = str(self.epic_link_field_issue_key)
        if self.parent_field_issue_key:
            self.parent_field_issue_key = str(self.parent_field_issue_key)
        if self.parent_id:
            self.parent_id = str(self.parent_id)

    @staticmethod
    def init_from_jira_issue(issue: dict, project_id: str = None, skip_parent_data: bool = False):
        fields: dict = issue.get("fields", {})
        return IssueMetadata(
            id=issue["id"],
            key=issue["key"],
            project_id=project_id,
            updated=parser.parse(fields.get("updated")) if fields.get("updated") else None,
            parent_id=fields.get("parent", {}).get("id") if not skip_parent_data else None,
            parent_field_issue_key=fields.get("parent", {}).get("key")
            if not skip_parent_data
            else None,
        )

    @staticmethod
    def init_from_jira_issues(issues=list[dict], skip_parent_data: bool = False):
        return [
            IssueMetadata.init_from_jira_issue(issue, skip_parent_data=skip_parent_data)
            for issue in issues
        ]

    # Define a hashing function so that we can find uniqueness
    # easily using sets
    def __hash__(self) -> str:
        return hash(self.id)

    def __eq__(self, __o) -> bool:
        return hash(self) == hash(__o)


@dataclass
class JiraConfig:
    company_slug: str = None
    url: str = None
    # NOTE: Used in the User-Agent header. Not related
    # to the Jellyfish Agent
    user_agent: str = "jellyfish/1.0"
    # Used for Basic Auth
    user: str = None
    password: str = None
    personal_access_token: str = None
    # Used for Atlassian Direct Connect
    jwt_attributes: dict[str, str] = field(default_factory=dict)
    bypass_ssl_verification: bool = False
    required_email_domains: bool = False
    is_email_required: bool = False
    available_auth_methods: list[JiraAuthMethod] = field(default_factory=list)
    connect_app_active: bool = False
    # Jira Server Information
    gdpr_active: bool = None

    include_fields: list[str] = None
    exclude_fields: list[str] = None
    # User information
    force_search_users_by_letter: bool = False
    search_users_by_letter_email_domain: str = None

    # Projects information
    include_projects: list[str] = None
    exclude_projects: list[str] = None
    include_project_categories: list[str] = None
    exclude_project_categories: list[str] = None

    # Boards/Sprints
    download_sprints: bool = False

    # Issues
    skip_issues: bool = False
    only_issues: bool = False
    full_redownload: bool = False
    earliest_issue_dt: datetime = datetime.min
    issue_download_concurrent_threads: int = 1
    # Dict of Issue ID (str) to IssueMetadata Object
    jellyfish_issue_metadata: list[IssueMetadata] = None
    jellyfish_project_ids_to_keys: dict = None

    # worklogs
    download_worklogs: bool = False
    # Potentially solidify this with the issues date, or pull from
    work_logs_pull_from: datetime = datetime.min

    # Jira Ingest Feature Flags
    feature_flags: dict = field(default_factory=dict)


@dataclass
class IngestionConfig:
    # upload info
    upload_to_s3: bool = False
    local_file_path: str = None
    company_slug: str = None
    timestamp: str = None

    # Jira Auth Info
    jira_config: JiraConfig = None

    # JF specific config
    jellyfish_api_token: str = None
    jellyfish_api_base: str = JELLYFISH_API_BASE
    ingest_type: IngestionType = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = format_datetime_to_ingest_timestamp(datetime.utcnow())

        if not self.local_file_path:
            self.local_file_path = f"{tempfile.TemporaryDirectory().name}/{self.timestamp}"
