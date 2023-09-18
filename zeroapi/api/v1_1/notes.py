from fastapi import APIRouter, Response
import json

from models.pydantic.requests import GetNotesRequest, SaveNoteRequest
from config.db import session
from services.notes import NoteService


note_router = APIRouter(prefix="/note")
service = NoteService(session=session)


@note_router.post("/get", tags=["notes"], deprecated=True)
async def get_note(request: GetNotesRequest):
    if request.note_id:
        note = await service.get_one_by_id(id=request.note_id)
    else:
        note = await service.get_by_owner(
            owner_id=request.owner_id,
            owner_login=request.owner_login,
            count=1
        )
    if note:
        return Response(
            content=json.dumps(note.__dict__),
            status_code=200
        )


@note_router.post("/save", tags=["notes"], deprecated=True)
async def save_note(request: SaveNoteRequest):
    await service.save(request)
    return Response(
        content=json.dumps({"message": "success"}),
        status_code=201
    )