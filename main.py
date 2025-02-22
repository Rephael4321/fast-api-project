import uvicorn
from fastapi import FastAPI, Depends
from controller import router
from StudentManager import StudentManager

def getManager():
    return StudentManager()

app = FastAPI(
    title="College Project",
    description="College Project served by rephael4321",
    version="1.0.0"
)

app.include_router(router, dependencies=[Depends(getManager)])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
