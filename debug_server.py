import uvicorn

# Importing app here makes the syntax cleaner as it will be picked up by refactors
from main import app

if __name__ == "__main__":
    uvicorn.run("debug_server:app", host="0.0.0.0", port=80, reload=True)
