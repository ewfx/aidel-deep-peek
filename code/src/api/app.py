from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List, Dict
from pydantic import BaseModel
import uvicorn
from main import RiskJSONGenerator
import json

app = FastAPI(
    title="DeepPeek API",
    description="API for processing text files and generating risk assessments",
    version="1.0.0"
)


class RiskResponse(BaseModel):
    results: List[Dict]

class ReportResponse(BaseModel):
    results: str


@app.post("/process-text", response_model=RiskResponse)
async def process_text_file(file: UploadFile = File(Ellipsis)):
    """
    Process a text file and generate risk assessment results.

    Args:
        file: The uploaded text file

    Returns:
        List of dictionaries containing risk assessment results
    """
    try:
        content = await file.read()
        text_content = content.decode('utf-8')
        risk_generator = RiskJSONGenerator(query=text_content)
        results = risk_generator.process()
        return RiskResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/generate-report")
async def generate_report(file: UploadFile = File(Ellipsis)):
    """
    Generate risk assessment results report.
    """
    try:
        content = await file.read()
        text_content = content.decode('utf-8')
        risk_generator = RiskJSONGenerator(query=text_content)
        results = risk_generator.process()
        pdf = risk_generator.generate_process(results)
        
        return ReportResponse(results=json.dumps({"results":results,"pdf":pdf}))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
