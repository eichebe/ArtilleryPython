import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from . import app 
from fastapi.routing import APIRoute
from email_validator import validate_email  # type: ignore 
def get_all_endpoints():
    """
    Retrieve all endpoints defined in the FastAPI app.
    """
    endpoints = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            endpoint = {
                "path": route.path,
                "methods": list(route.methods - {"HEAD", "OPTIONS"}) 
            }
            endpoints.append(endpoint)
    return endpoints

if __name__ == "__main__":
    all_endpoints = get_all_endpoints()
    for ep in all_endpoints:
        print(ep)
