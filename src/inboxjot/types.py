from typing import Any, Literal, TypedDict

EmailStatus = Literal[
    "scheduled",
    "queued",
    "sending",
    "sent",
    "soft_bounced",
    "delivered",
    "opened",
    "clicked",
    "bounced",
    "rejected",
    "failed",
    "canceled",
    "complained",
]
ContactStatus = Literal["subscribed", "pending", "not_subscribed", "unsubscribed"]
ContactSort = Literal["added", "contact", "last_activity"]
EmailSource = Literal["api", "smtp", "dashboard", "mcp", "campaign", "automation"]
SortDirection = Literal["asc", "desc"]
TopicChoiceStatus = Literal["subscribed", "unsubscribed"]
EmailActor = Literal["human", "apple_mpp", "scanner", "unknown"]
BounceType = Literal["permanent", "transient", "undetermined"]
ComplaintType = Literal["abuse"]
EmailStatusOp = Literal["is", "not"]
EmailSort = Literal["sent", "to"]
CampaignStatus = Literal["draft", "scheduled", "sending", "paused", "failed", "sent", "canceled"]
CampaignPauseReason = Literal[
    "manual",
    "daily_limit",
    "warmup",
    "sending_paused",
    "domain_unverified",
    "no_plan",
    "plan_limit",
]
CampaignSort = Literal["sent", "name"]
VersionFilter = Literal["all", "saved"]
DocumentVersionReason = Literal[
    "checkpoint",
    "manual",
    "before_agent_edit",
    "before_restore",
    "restored",
    "published",
]
DocumentVersionEditorKind = Literal["user", "agent", "api"]
TemplateSort = Literal["updated", "name"]
DomainStatus = Literal["not_started", "pending", "verified", "failed", "temporary_failure"]
RecordKind = Literal["dkim", "return_path", "dmarc", "tracking_cname", "tracking_caa"]
TrackingStatus = Literal["not_started", "pending", "issuing", "verified", "failed"]
ImageType = Literal["png", "jpeg", "gif"]
ImageContentType = Literal["image/png", "image/jpeg", "image/gif"]
SegmentType = Literal["static", "dynamic"]
SegmentSort = Literal["created", "name", "contacts"]
SegmentMatch = Literal["all", "any"]
SegmentOperator = Literal[
    "is",
    "is_not",
    "contains",
    "not_contains",
    "starts_with",
    "ends_with",
    "is_set",
    "is_not_set",
    "equals",
    "not_equals",
    "greater_than",
    "less_than",
    "within",
    "not_within",
    "before",
    "after",
    "in",
    "not_in",
    "at_least",
    "never",
]
TopicVisibility = Literal["public", "private"]
EndpointStatus = Literal["enabled", "disabled"]

ErrorName = Literal[
    "validation_error",
    "not_found",
    "unauthorized",
    "forbidden",
    "internal_server_error",
    "bad_request",
    "user_not_verified",
    "rate_limit_exceeded",
    "conflict",
    "limit_exceeded",
    "reauthentication_required",
    "invalid_idempotency_key",
    "concurrent_idempotent_requests",
    "invalid_idempotent_request",
    "payload_too_large",
    "unsupported_media_type",
    "service_unavailable",
    "unknown_error",
]

Recipients = str | list[str]
ContactPropertyValue = str | float | bool | None


class StatusOk(TypedDict):
    status: str


class ErrorItem(TypedDict):
    location: str
    message: str


class EmailTag(TypedDict):
    name: str
    value: str


class _TemplateRefRequired(TypedDict):
    id: str


class TemplateRef(_TemplateRefRequired, total=False):
    variables: dict[str, Any]


class _AttachmentInputRequired(TypedDict):
    filename: str


class AttachmentInput(_AttachmentInputRequired, total=False):
    content: str | None
    content_id: str | None
    content_type: str | None
    path: str | None


_BatchEmailFields = TypedDict(
    "_BatchEmailFields",
    {
        "from": str | None,
        "cc": Recipients,
        "bcc": Recipients,
        "reply_to": Recipients,
        "subject": str | None,
        "html": str | None,
        "text": str | None,
        "headers": dict[str, str],
        "tags": list[EmailTag],
        "template": TemplateRef | None,
    },
    total=False,
)


class BatchEmailOptions(_BatchEmailFields):
    to: Recipients


class SendEmailOptions(BatchEmailOptions, total=False):
    attachments: list[AttachmentInput]
    scheduled_at: str | None


class SendEmailResponse(TypedDict):
    id: str


class BatchEmailResponse(TypedDict):
    data: list[SendEmailResponse]


Email = TypedDict(
    "Email",
    {
        "id": str,
        "from": str,
        "to": list[str],
        "cc": list[str],
        "bcc": list[str],
        "subject": str,
        "tags": list[EmailTag],
        "status": EmailStatus,
        "source": EmailSource,
        "created_at": str,
        "scheduled_at": str | None,
        "sent_at": str | None,
    },
)


class ListEmailsOptions(TypedDict, total=False):
    query: str
    status: str
    status_op: EmailStatusOp
    source: EmailSource
    sent_after: str
    sent_before: str
    sort: EmailSort
    direction: SortDirection
    after: str | None
    before: str | None
    per_page: int


class EmailPage(TypedDict):
    data: list[Email]
    next_cursor: str | None
    prev_cursor: str | None


class UpdateEmailOptions(TypedDict):
    scheduled_at: str


class UpdateEmailResponse(TypedDict):
    id: str
    scheduled_at: str | None


class CancelEmailResponse(TypedDict):
    id: str
    status: EmailStatus


class Attachment(TypedDict):
    id: str
    filename: str
    content_type: str
    content_disposition: str
    content_id: str | None
    size: int
    download_url: str | None
    expires_at: str | None
    deleted_at: str | None


class AttachmentList(TypedDict):
    data: list[Attachment]


class ContactFields(TypedDict, total=False):
    first_name: str | None
    last_name: str | None
    language: str | None
    notes: str | None
    properties: dict[str, ContactPropertyValue] | None
    segment_ids: list[str] | None
    subscribed: bool | None


class CreateContactOptions(ContactFields):
    email: str


class TopicChoice(TypedDict):
    id: str
    status: TopicChoiceStatus


class UpdateContactOptions(ContactFields, total=False):
    topics: list[TopicChoice] | None


class SegmentRef(TypedDict):
    id: str
    name: str


class ContactTopic(TypedDict):
    id: str
    name: str
    status: ContactStatus | None
    subscribed: bool


class Contact(TypedDict):
    id: str
    email: str
    first_name: str | None
    last_name: str | None
    language: str
    status: ContactStatus
    properties: dict[str, ContactPropertyValue]
    segments: list[SegmentRef]
    topics: list[ContactTopic]
    created_at: str
    updated_at: str


class CreateContactResponse(Contact):
    created: bool


class ListContactsOptions(TypedDict, total=False):
    sort: ContactSort
    direction: SortDirection
    status: ContactStatus
    segment_id: str
    query: str
    after: str | None
    before: str | None
    per_page: int


class ContactLastActivity(TypedDict):
    type: str
    at: str


class ContactListItem(TypedDict):
    id: str
    email: str
    first_name: str | None
    last_name: str | None
    properties: dict[str, ContactPropertyValue]
    status: ContactStatus
    is_suppressed: bool
    segments: list[SegmentRef]
    last_activity: ContactLastActivity | None
    created_at: str


class ContactPage(TypedDict):
    data: list[ContactListItem]
    total: int
    next_cursor: str | None
    prev_cursor: str | None


DeleteContactResponse = StatusOk


class EraseContactOptions(TypedDict):
    email: str


class EraseContactResponse(TypedDict):
    status: Literal["queued"]


class _SendEventRequired(TypedDict):
    name: str
    email: str


class SendEventOptions(_SendEventRequired, total=False):
    data: dict[str, Any]


class SendEventResponse(TypedDict):
    contact_id: str


_EmailEventRequired = TypedDict(
    "_EmailEventRequired",
    {
        "email_id": str,
        "from": str,
        "to": list[str],
        "subject": str,
    },
)


class EmailEventData(_EmailEventRequired, total=False):
    tags: list[EmailTag]


class EmailOpenedData(EmailEventData):
    actor: EmailActor


class EmailClickedData(EmailOpenedData, total=False):
    link: str


class EmailBounce(TypedDict):
    type: BounceType
    message: str


class EmailBouncedData(EmailEventData):
    bounce: EmailBounce


class EmailComplaint(TypedDict):
    type: ComplaintType


class EmailComplainedData(EmailEventData):
    complaint: EmailComplaint


class EmailFailedData(EmailEventData):
    reason: str


class ContactEventData(TypedDict):
    contact_id: str
    email: str
    first_name: str | None
    last_name: str | None
    language: str
    status: ContactStatus
    properties: dict[str, ContactPropertyValue]
    created_at: str
    updated_at: str


class _WebhookEventBase(TypedDict):
    id: str
    created_at: str


class EmailEvent(_WebhookEventBase):
    type: Literal["email.sent", "email.delivered", "email.delivery_delayed", "email.unsubscribed"]
    data: EmailEventData


class EmailOpenedEvent(_WebhookEventBase):
    type: Literal["email.opened"]
    data: EmailOpenedData


class EmailClickedEvent(_WebhookEventBase):
    type: Literal["email.clicked"]
    data: EmailClickedData


class EmailBouncedEvent(_WebhookEventBase):
    type: Literal["email.bounced"]
    data: EmailBouncedData


class EmailComplainedEvent(_WebhookEventBase):
    type: Literal["email.complained"]
    data: EmailComplainedData


class EmailFailedEvent(_WebhookEventBase):
    type: Literal["email.rejected", "email.failed"]
    data: EmailFailedData


class ContactEvent(_WebhookEventBase):
    type: Literal["contact.created", "contact.updated", "contact.deleted"]
    data: ContactEventData


WebhookEvent = (
    EmailEvent
    | EmailOpenedEvent
    | EmailClickedEvent
    | EmailBouncedEvent
    | EmailComplainedEvent
    | EmailFailedEvent
    | ContactEvent
)
WebhookEventType = Literal[
    "email.sent",
    "email.delivered",
    "email.opened",
    "email.clicked",
    "email.bounced",
    "email.complained",
    "email.delivery_delayed",
    "email.rejected",
    "email.failed",
    "email.unsubscribed",
    "contact.created",
    "contact.updated",
    "contact.deleted",
]


class ListWebhooksOptions(TypedDict, total=False):
    after: str | None
    before: str | None
    per_page: int


class UpdateWebhookResponse(TypedDict):
    id: str
    name: str
    url: str
    events: list[WebhookEventType]
    status: EndpointStatus
    disabled_reason: str | None
    created_at: str
    updated_at: str


class WebhookListItem(UpdateWebhookResponse):
    success_rate: float | None
    last_delivery_at: str | None


class WebhookPage(TypedDict):
    data: list[WebhookListItem]
    next_cursor: str | None
    prev_cursor: str | None


class CreateWebhookOptions(TypedDict):
    name: str
    url: str
    events: list[WebhookEventType]


class CreateWebhookResponse(UpdateWebhookResponse):
    secret: str


class WebhookDelivery(TypedDict):
    delivery_id: str
    event_id: str
    event_type: str
    endpoint_id: str
    email_id: str
    status: int
    attempt: int
    duration_ms: int
    created_at: str
    last_attempt_at: str
    next_attempt_at: str | None


class Webhook(UpdateWebhookResponse):
    deliveries_24h: int
    success_rate: float | None
    avg_duration_ms: int | None
    retrying: int
    recent_deliveries: list[WebhookDelivery]


class UpdateWebhookOptions(TypedDict, total=False):
    name: str | None
    url: str | None
    events: list[WebhookEventType] | None
    status: EndpointStatus | None


DeleteWebhookResponse = StatusOk


class Named(TypedDict):
    id: str
    name: str


class CampaignSummary(TypedDict):
    delivered: int
    opened: int
    clicked: int


class CampaignListItem(TypedDict):
    id: str
    name: str
    status: CampaignStatus
    subject: str
    include_segments: list[Named]
    exclude_segments: list[Named]
    topic: Named | None
    audience_count: int | None
    queued_count: int
    skipped_count: int
    paused_reason: CampaignPauseReason | None
    scheduled_at: str | None
    started_at: str | None
    completed_at: str | None
    created_at: str
    updated_at: str
    stats: CampaignSummary | None


class CampaignPage(TypedDict):
    data: list[CampaignListItem]
    next_cursor: str | None
    prev_cursor: str | None


class ListCampaignsOptions(TypedDict, total=False):
    query: str
    status: str
    sort: CampaignSort
    direction: SortDirection
    after: str | None
    before: str | None
    per_page: int


CreateCampaignOptions = TypedDict(
    "CreateCampaignOptions",
    {
        "name": str | None,
        "from": str | None,
        "reply_to": str | None,
        "subject": str | None,
        "preheader": str | None,
        "html": str | None,
        "content": dict[str, Any] | None,
        "template_id": str | None,
        "include_segment_ids": list[str] | None,
        "exclude_segment_ids": list[str] | None,
        "topic_id": str | None,
    },
    total=False,
)
UpdateCampaignOptions = CreateCampaignOptions

Campaign = TypedDict(
    "Campaign",
    {
        "id": str,
        "name": str,
        "status": CampaignStatus,
        "from": str,
        "reply_to": str | None,
        "subject": str,
        "preheader": str,
        "html": str | None,
        "text": str | None,
        "template_id": str | None,
        "template": Named | None,
        "include_segment_ids": list[str],
        "include_segments": list[Named],
        "exclude_segment_ids": list[str],
        "exclude_segments": list[Named],
        "topic_id": str,
        "topic": Named | None,
        "audience_count": int | None,
        "queued_count": int,
        "skipped_count": int,
        "paused_reason": CampaignPauseReason | None,
        "failure_reason": str | None,
        "scheduled_at": str | None,
        "started_at": str | None,
        "completed_at": str | None,
        "warmup_next_limit": int | None,
        "created_at": str,
        "updated_at": str,
    },
)
DeleteCampaignResponse = StatusOk


class SendCampaignOptions(TypedDict, total=False):
    scheduled_at: str | None


class SendCampaignTestOptions(TypedDict):
    to: list[str]


class SendCampaignTestResponse(TypedDict):
    ids: list[str]


class ListVersionsOptions(TypedDict, total=False):
    filter: VersionFilter
    after: str | None
    before: str | None
    per_page: int


class DocumentVersionEditor(TypedDict):
    kind: DocumentVersionEditorKind
    id: str
    name: str


class DocumentVersion(TypedDict):
    id: str
    reason: DocumentVersionReason
    name: str | None
    editors: list[DocumentVersionEditor]
    created_at: str


class DocumentVersionPage(TypedDict):
    data: list[DocumentVersion]
    total: int
    next_cursor: str | None
    prev_cursor: str | None


_DocumentVersionContent = TypedDict(
    "_DocumentVersionContent",
    {
        "from": str,
        "reply_to": str | None,
        "subject": str,
        "preheader": str,
        "html": str,
        "text": str,
        "content": dict[str, Any],
    },
)


class DocumentVersionDetail(DocumentVersion, _DocumentVersionContent):
    pass


class CreateVersionOptions(TypedDict):
    name: str


class UpdateVersionOptions(TypedDict):
    name: str | None


ListCampaignVersionsOptions = ListVersionsOptions
CampaignVersionPage = DocumentVersionPage
CampaignVersion = DocumentVersion
CampaignVersionDetail = DocumentVersionDetail
CreateCampaignVersionOptions = CreateVersionOptions
UpdateCampaignVersionOptions = UpdateVersionOptions


class TemplateStats(TypedDict):
    sent: int
    opened: int
    clicked: int


class UsedCampaign(TypedDict):
    id: str
    name: str


class UsedIn(TypedDict):
    count: int
    first: UsedCampaign | None


TemplateListItem = TypedDict(
    "TemplateListItem",
    {
        "id": str,
        "name": str,
        "from": str,
        "subject": str,
        "preheader": str,
        "stats": TemplateStats,
        "used_in": UsedIn,
        "created_at": str,
        "updated_at": str,
    },
)


class TemplatePage(TypedDict):
    data: list[TemplateListItem]
    next_cursor: str | None
    prev_cursor: str | None


class ListTemplatesOptions(TypedDict, total=False):
    query: str
    sort: TemplateSort
    direction: SortDirection
    after: str | None
    before: str | None
    per_page: int


_TemplateFields = TypedDict(
    "_TemplateFields",
    {
        "from": str | None,
        "reply_to": str | None,
        "subject": str | None,
        "preheader": str | None,
        "html": str | None,
        "content": dict[str, Any] | None,
    },
    total=False,
)


class UpdateTemplateOptions(_TemplateFields, total=False):
    name: str | None


class _CreateTemplateRequired(_TemplateFields):
    name: str


class CreateTemplateOptions(_CreateTemplateRequired, total=False):
    starter_id: str | None


Template = TypedDict(
    "Template",
    {
        "id": str,
        "name": str,
        "from": str,
        "reply_to": str | None,
        "subject": str,
        "preheader": str,
        "html": str,
        "text": str,
        "published_version_id": str | None,
        "has_unpublished_changes": bool,
        "created_at": str,
        "updated_at": str,
    },
)
DeleteTemplateResponse = StatusOk
ListTemplateVersionsOptions = ListVersionsOptions
TemplateVersionPage = DocumentVersionPage
TemplateVersion = DocumentVersion
TemplateVersionDetail = DocumentVersionDetail
CreateTemplateVersionOptions = CreateVersionOptions
UpdateTemplateVersionOptions = UpdateVersionOptions


class ListDomainsOptions(TypedDict, total=False):
    after: str | None
    before: str | None
    per_page: int


class DomainListItem(TypedDict):
    id: str
    name: str
    status: DomainStatus
    pending_record_kinds: list[RecordKind]
    region: str
    is_default: bool
    open_tracking: bool
    click_tracking: bool
    sent_last_30_days: int
    verified_at: str | None
    created_at: str


class DomainPage(TypedDict):
    data: list[DomainListItem]
    next_cursor: str | None
    prev_cursor: str | None


class _CreateDomainRequired(TypedDict):
    name: str


class CreateDomainOptions(_CreateDomainRequired, total=False):
    region: str | None
    return_path: str | None


class _DomainRecordRequired(TypedDict):
    kind: RecordKind
    type: str
    name: str
    value: str
    status: DomainStatus


class DomainRecord(_DomainRecordRequired, total=False):
    priority: int


class DomainReceiving(TypedDict):
    host: str
    mx: str
    shared_address: str | None


class DomainWarmup(TypedDict):
    enabled: bool
    started_on: str | None
    day: int | None
    limit: int | None
    next_limit: int | None
    sent_today: int
    full_volume_on: str | None


class Domain(TypedDict):
    id: str
    name: str
    mail_from_domain: str
    status: DomainStatus
    records: list[DomainRecord]
    region: str
    tls_policy: str
    receiving_enabled: bool
    receiving_target: str
    receiving_status: DomainStatus
    receiving_found_mx: str | None
    receiving_checked_at: str | None
    receiving_verified_at: str | None
    open_tracking: bool
    click_tracking: bool
    tracking_domain: str | None
    tracking_status: TrackingStatus
    tracking_records: list[DomainRecord]
    tracking_verified_at: str | None
    mailing_address: str | None
    verified_at: str | None
    created_at: str
    updated_at: str
    sent_last_30_days: int
    bounced_last_30_days: int
    is_default: bool
    receiving: DomainReceiving
    warmup: DomainWarmup


DeleteDomainResponse = StatusOk


class ListImagesOptions(TypedDict, total=False):
    query: str
    type: ImageType
    direction: SortDirection
    after: str | None
    before: str | None
    per_page: int


class _UploadImageRequired(TypedDict):
    file: bytes


class UploadImageOptions(_UploadImageRequired, total=False):
    file_name: str


class Image(TypedDict):
    id: str
    file_name: str
    url: str | None
    content_type: str
    size_bytes: int
    width: int
    height: int
    creator_name: str | None
    created_at: str


class ImagePage(TypedDict):
    data: list[Image]
    total: int
    next_cursor: str | None
    prev_cursor: str | None


DeleteImageResponse = StatusOk


class RuleWindow(TypedDict):
    count: float
    days: float


RuleValue = str | float | bool | RuleWindow


class _SegmentRuleRequired(TypedDict):
    field: str
    operator: SegmentOperator


class SegmentRule(_SegmentRuleRequired, total=False):
    value: RuleValue


class SegmentConditions(TypedDict):
    match: SegmentMatch
    rules: list[SegmentRule]


class ListSegmentsOptions(TypedDict, total=False):
    type: SegmentType
    query: str
    sort: SegmentSort
    direction: SortDirection
    after: str | None
    before: str | None
    per_page: int


class SegmentListItem(TypedDict):
    id: str
    name: str
    description: str | None
    type: SegmentType
    contact_count: int | None
    counted_at: str | None
    created_at: str
    updated_at: str


class SegmentPage(TypedDict):
    data: list[SegmentListItem]
    total: int
    next_cursor: str | None
    prev_cursor: str | None


class _CreateSegmentRequired(TypedDict):
    name: str
    type: SegmentType


class CreateSegmentOptions(_CreateSegmentRequired, total=False):
    description: str | None
    conditions: SegmentConditions | None


class Segment(SegmentListItem):
    conditions: SegmentConditions | None


class UpdateSegmentOptions(TypedDict, total=False):
    name: str | None
    description: str | None
    conditions: SegmentConditions | None


DeleteSegmentResponse = StatusOk


class ListSegmentMembersOptions(TypedDict, total=False):
    query: str
    after: str | None
    before: str | None
    per_page: int


class SegmentMember(TypedDict):
    id: str
    email: str
    first_name: str | None
    last_name: str | None
    status: ContactStatus
    joined_at: str


class SegmentMemberPage(TypedDict):
    data: list[SegmentMember]
    next_cursor: str | None
    prev_cursor: str | None


class SegmentMembersOptions(TypedDict):
    contact_ids: list[str]


class AddSegmentMembersResponse(TypedDict):
    added: int


class RemoveSegmentMembersResponse(TypedDict):
    removed: int


class ListTopicsOptions(TypedDict, total=False):
    after: str | None
    before: str | None
    per_page: int


class TopicCounts(TypedDict):
    subscribed: int
    pending: int
    unsubscribed: int


class Topic(TypedDict):
    id: str
    name: str
    description: str | None
    default_subscribed: bool
    visibility: TopicVisibility
    double_opt_in: bool
    form_enabled: bool
    sender_name: str | None
    sender_email: str | None
    redirect_url: str | None
    is_default: bool
    counts: TopicCounts
    created_at: str
    updated_at: str


class TopicPage(TypedDict):
    data: list[Topic]
    next_cursor: str | None
    prev_cursor: str | None


class _TopicFields(TypedDict, total=False):
    description: str | None
    default_subscribed: bool | None
    visibility: TopicVisibility | None
    double_opt_in: bool | None
    form_enabled: bool | None
    sender_name: str | None
    sender_email: str | None
    redirect_url: str | None


class CreateTopicOptions(_TopicFields):
    name: str


class UpdateTopicOptions(_TopicFields, total=False):
    name: str | None


DeleteTopicResponse = StatusOk
