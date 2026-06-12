from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.core.exceptions import AppBaseException

app = FastAPI()
app.include_router(router)


@app.exception_handler(AppBaseException)
async def app_exception_handler(request : Request , exc : AppBaseException):
    return JSONResponse(
        status_code = exc.status_code,
        content = {"error" : exc.message}
    )