from fastapi import APIRouter, Depends, Request, status

from app.core.analytics import enqueue_analytics
from app.core.deps import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.schemas.learning_analytics import BrowserEventRequest, PublicBrowserEventRequest
from app.services.learning_analytics import record_learning_event

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.post("/ui", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("60/minute")
async def report_ui_event(
    request: Request,
    body: BrowserEventRequest,
    _user: User = Depends(get_current_user),
) -> None:
    enqueue_analytics(
        request,
        record_learning_event,
        body.event,
        source_id=body.operation_id,
        user_agent=request.headers.get("user-agent", ""),
    )


@router.post("/public", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("30/minute")
async def report_public_event(request: Request, body: PublicBrowserEventRequest) -> None:
    enqueue_analytics(
        request,
        record_learning_event,
        body.event,
        source_id=body.operation_id,
        user_agent=request.headers.get("user-agent", ""),
    )
