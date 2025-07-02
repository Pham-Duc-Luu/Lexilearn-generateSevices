

from fastapi import APIRouter


router = APIRouter(
    prefix="/key-word-capture",
    tags=["words"],
    responses={404: {"description": "Not found"}},
)


## TODO: Implement keyword capture logic
@router.get("")
async def get_keyword_in_para():
    return
