from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List, Dict
from pydantic import BaseModel
import uvicorn
import pandas as pd
import io
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

def process_csv_content(content: bytes) -> str:
    """
    Process CSV content and convert it to text format with column names as keys.
    
    Args:
        content: Raw bytes of the CSV file
        
    Returns:
        String containing formatted records separated by '---'
    """
    try:
        # Read CSV content into pandas DataFrame
        df = pd.read_csv(io.BytesIO(content))
        
        # Convert DataFrame to list of dictionaries
        records = df.to_dict('records')
        
        # Format each record with column names as keys
        formatted_records = []
        for record in records:
            formatted_record = []
            for key, value in record.items():
                formatted_record.append(f"{key}: {value}")
            formatted_records.append("\n".join(formatted_record))
        
        # Join records with a more visible separator
        separator = "\n\n" + "="*5 + "\n\n"
        return separator.join(formatted_records)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV file: {str(e)}")

@app.post("/process-text", response_model=RiskResponse)
async def process_text_file(file: UploadFile = File(Ellipsis)):
    """
    Process a text or CSV file and generate risk assessment results.

    Args:
        file: The uploaded text or CSV file

    Returns:
        List of dictionaries containing risk assessment results
    """
    try:
        content = await file.read()
        
        # Check if file is CSV
        if file.filename.endswith('.csv'):
            text_content = process_csv_content(content)
        else:
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
        
        # Check if file is CSV
        if file.filename.endswith('.csv'):
            text_content = process_csv_content(content)
        else:
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
