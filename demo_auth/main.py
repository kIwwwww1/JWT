import uvicorn
from fastapi import FastAPI
from other import router as basic_router

app = FastAPI()
app.include_router(router=basic_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)