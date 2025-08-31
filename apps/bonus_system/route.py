from fastapi import APIRouter
from starlette.responses import StreamingResponse

from ..core import dependencies
from . import services
from .services import iter_progress_csv


router = APIRouter()


@router.post("")
async def level_is_passed(
    player_id: int,
    level_id: int,
    session: dependencies.DBSessionDep,
):
    return await services.level_is_passed(session=session, player_id=player_id, level_id=level_id)


@router.get("/export", response_class=StreamingResponse)
async def export_progress_csv(
    session: dependencies.DBSessionDep,
):
    return StreamingResponse(
        iter_progress_csv(session),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="progress.csv"'},
    )
