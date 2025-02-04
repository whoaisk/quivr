import os
import shutil
from tempfile import SpooledTemporaryFile

from auth.auth_bearer import JWTBearer
from crawl.crawler import CrawlWebsite
from fastapi import APIRouter, Depends, Request, UploadFile
from middlewares.cors import add_cors_middleware
from models.users import User
from parsers.github import process_github
from utils.file import convert_bytes
from utils.processors import filter_file
from utils.vectors import CommonsDep

crawl_router = APIRouter()

@crawl_router.post("/crawl/", dependencies=[Depends(JWTBearer())])
async def crawl_endpoint(request: Request,commons: CommonsDep, crawl_website: CrawlWebsite, enable_summarization: bool = False, credentials: dict = Depends(JWTBearer())):
    max_brain_size = os.getenv("MAX_BRAIN_SIZE")
    if request.headers.get('Openai-Api-Key'):
        max_brain_size = os.getenv("MAX_BRAIN_SIZE_WITH_KEY",209715200)

    user = User(email=credentials.get('email', 'none'))
    user_vectors_response = commons['supabase'].table("vectors").select(
        "name:metadata->>file_name, size:metadata->>file_size", count="exact") \
            .filter("user_id", "eq", user.email)\
            .execute()
    documents = user_vectors_response.data  # Access the data from the response
    # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
    user_unique_vectors = [dict(t) for t in set(tuple(d.items()) for d in documents)]

    current_brain_size = sum(float(doc['size']) for doc in user_unique_vectors)

    file_size = 1000000

    remaining_free_space =  float(max_brain_size) - (current_brain_size)

    if remaining_free_space - file_size < 0:
        message = {"message": f"❌ User's brain will exceed maximum capacity with this upload. Maximum file allowed is : {convert_bytes(remaining_free_space)}", "type": "error"}
    else: 
        user = User(email=credentials.get('email', 'none'))
        if not crawl_website.checkGithub():

            file_path, file_name = crawl_website.process()

            # Create a SpooledTemporaryFile from the file_path
            spooled_file = SpooledTemporaryFile()
            with open(file_path, 'rb') as f:
                shutil.copyfileobj(f, spooled_file)

            # Pass the SpooledTemporaryFile to UploadFile
            file = UploadFile(file=spooled_file, filename=file_name)
            message = await filter_file(file, enable_summarization, commons['supabase'], user=user, openai_api_key=request.headers.get('Openai-Api-Key', None))
            return message
        else:
            message = await process_github(crawl_website.url, "false", user=user, supabase=commons['supabase'], user_openai_api_key=request.headers.get('Openai-Api-Key', None))
