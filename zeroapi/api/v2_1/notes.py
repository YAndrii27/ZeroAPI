from quart import Blueprint, Response
from quart_schema import validate_request
import json

from models.pydantic.requests import GetNotesRequest, SaveNoteRequest
from config.db import session
from services.notes import NoteService

note_blueprint = Blueprint(
    name="note",
    import_name=__name__,
    url_prefix="/note"
)
service = NoteService(session=session)


@note_blueprint.post("/get")
@validate_request(GetNotesRequest)
async def get_note(request: GetNotesRequest):
    """Get note(s) by one of two params: note ID or by owner ID/login"""
    if request.note_id:
        note = await service.get_one_by_id(id=request.note_id)
    else:
        note = await service.get_by_owner(
            owner_id=request.owner_id,
            owner_login=request.owner_login,
        )
    if note:
        return Response(
            response=note.__dict__,
            status=200
        )
    return Response(
        response={"message": "could not find requested notes"},
        status=404
    )


@note_blueprint.post("/save")
@validate_request(SaveNoteRequest)
async def save_note(request: SaveNoteRequest):
    """Save or update note data to database.
    Accepts only data which has to be updated"""
    await service.save(request)
    return Response(
        response=json.dumps({"message": "success"}),
        status=201
    )
