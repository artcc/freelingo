from pydantic import AwareDatetime, BaseModel, Field, StrictBool


class RevenueCatEvent(BaseModel):
    id: str = Field(min_length=1, max_length=255)
    type: str = Field(min_length=1)
    event_timestamp_ms: int = Field(ge=0, strict=True)
    environment: str | None = None
    app_user_id: str | None = None
    original_app_user_id: str | None = None
    aliases: list[str] | None = None
    transferred_from: list[str] | None = None
    transferred_to: list[str] | None = None
    redeemed_from: list[str] | None = None
    redeemed_by: list[str] | None = None


class RevenueCatWebhook(BaseModel):
    api_version: str
    event: RevenueCatEvent


class RevenueCatEntitlement(BaseModel):
    expires_date: AwareDatetime | None
    grace_period_expires_date: AwareDatetime | None = None
    product_identifier: str = Field(min_length=1)


class RevenueCatSubscription(BaseModel):
    is_sandbox: StrictBool
    period_type: str = "normal"
    unsubscribe_detected_at: AwareDatetime | None = None
    billing_issues_detected_at: AwareDatetime | None = None
    refunded_at: AwareDatetime | None = None


class RevenueCatPurchase(BaseModel):
    is_sandbox: StrictBool


class RevenueCatSubscriber(BaseModel):
    entitlements: dict[str, RevenueCatEntitlement]
    subscriptions: dict[str, RevenueCatSubscription]
    non_subscriptions: dict[str, list[RevenueCatPurchase]] = Field(default_factory=dict)
    management_url: str | None = None


class RevenueCatCustomerInfo(BaseModel):
    request_date_ms: int = Field(ge=0, strict=True)
    subscriber: RevenueCatSubscriber


class RevenueCatSyncRequest(BaseModel):
    import_stripe: bool = False


class BillingStatusResponse(BaseModel):
    subscription_status: str
    subscription_ends_at: AwareDatetime | None
    cancel_at_period_end: bool
