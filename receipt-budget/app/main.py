from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from app.ocr import run_ocr
from app.parser import parse_receipt_text
from app.categorizer import categorize_items
from app.db import init_db, insert_receipt_with_items
from app.recommender import suggest_savings

app = FastAPI()
init_db()

@app.post("/upload-receipt/")
async def upload_receipt(file: UploadFile = File(...)):
    contents = await file.read()
    raw_text = run_ocr(contents)
    items = parse_receipt_text(raw_text)
    categorized = categorize_items(items)
    receipt_id = insert_receipt_with_items(file.filename, categorized)
    recs = suggest_savings(receipt_id)

    return JSONResponse({
        "receipt_id": receipt_id,
        "items": categorized,
        "recommendations": recs
    })