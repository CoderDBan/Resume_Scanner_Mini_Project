from Resume_scanner import validate_and_update
from fastapi import FastAPI, UploadFile, File , Request,Form ,Body
from pdf2image import convert_from_bytes
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import json
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/check_cv")
async def check_cv(name=Form(...),address=Form(...),cv_file: UploadFile = File(...), id_file: UploadFile = File(...)):
    try:
        # Perform your processing logic here with the file contents
        # Call your is_fake function with the file contents
        # Read the uploaded PDF file as bytes
        if not(cv_file.filename.endswith(('pdf','docx'))):
            return {"result": "valid CV format are: pdf or docx"}
        if not(id_file.filename.endswith(('pdf')) or id_file.content_type.startswith('image')):
            return {"result": "valid Id format are: pdf or an image"}
        cv_data =await cv_file.read()
        id_data=await id_file.read()
        details={"name":name,"address":address}
        cv_images=[]
        id_images=[]
        if(cv_file.filename.endswith('.pdf')):
            # Convert PDF to images
            cv_images = convert_from_bytes(cv_data)
        if(id_file.filename.endswith('.pdf')):
            # Convert PDF to images
            id_images = convert_from_bytes(id_data)
        details["cv_data"]=cv_data
        details["id_data"]=id_data
        details["cv_path"]=cv_file
        details["id_path"]=id_file
        details["cv_images"]=cv_images
        details["id_images"]=id_images
        result = validate_and_update(details)
        # Return the result as a response
        return result
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in the request body"}