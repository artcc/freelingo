from fastapi import APIRouter, BackgroundTasks, Depends, Request, status

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
    background_tasks: BackgroundTasks,
    _user: User = Depends(get_current_user),
) -> None:
    background_tasks.add_task(
        record_learning_event,
        body.event,
        source_id=body.operation_id,
        user_agent=request.headers.get("user-agent", ""),
    )


@router.post("/public", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("30/minute")
async def report_public_event(
    request: Request, body: PublicBrowserEventRequest, background_tasks: BackgroundTasks
) -> None:
    background_tasks.add_task(
        record_learning_event,
        body.event,
        source_id=body.operation_id,
        user_agent=request.headers.get("user-agent", ""),
    )
