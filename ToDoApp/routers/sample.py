from fastapi import APIRouter

router=APIRouter()

@router.get('/')
async def sample():
    return {"message":"This is from sample.py"}