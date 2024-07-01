import os
from fastapi import APIRouter, HTTPException, status

from pipeline import AlgoIn


router = APIRouter()

@router.get("/test", response_model=str, tags=["items"])
def get_tracking(): 
    
    terminal_command = """
    cd ..
    cd cm_pipeline
    python -m main ../api/pipeline.json
    """

    os.system(terminal_command)

    return "Run Pipeline"



@router.post("/pipeline", response_model=AlgoIn, status_code=status.HTTP_201_CREATED, tags=["items"])
def run_pipeline(algoIn: AlgoIn): 
    return algoIn
   