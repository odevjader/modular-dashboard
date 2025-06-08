# backend/app/api_router.py
from fastapi import APIRouter

# Create the main API router - this router will be prefixed by /api from main.py
api_router = APIRouter()

# All module routing (core and pluggable) will be added to this api_router instance
# by the load_and_register_modules function called from main.py.
# Example of a static route if needed (though ideally everything is a module):
# @api_router.get("/ping", tags=["API System"])
# async def ping():
#     return {"message": "pong from api_router"}