# This Script contains functions that handle the saving of Images
# It uses GridFS from MongoDB
# This is done in order to Save szie as base64 takes up much more amount of size in the Database
# Importing Necessary Libraries
from gridfs import AsyncGridFSBucket
from bson import ObjectId
from db.mongo import db

bucket = AsyncGridFSBucket(db=db)

# Save Images with GridFS
async def save_image(name: str, file_bytes: str) -> str:
    image_id = await bucket.upload_from_stream(filename=name, chunk_size_bytes=file_bytes)
    return str(image_id)

# Get Images with GridFS
async def get_image(id: str) -> bytes:
    stream = await bucket.open_download_stream(ObjectId(id))
    return await stream.read()

# Delete Images with GridFS
async def delete_image(id: str) -> None:
    await bucket.delete(file_id=ObjectId(id))