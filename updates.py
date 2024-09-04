from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .router import inserter, tables, db, pro, tutorial, restore, qpr, report
from .database import engine
from .schema import PER, PES
from .exception.equiv_error import EquivalenceError

PER.Base.metadata.create_all(bind=engine)
PES.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(inserter.router)
app.include_router(tables.router)
app.include_router(db.router)
app.include_router(pro.router)
app.include_router(tutorial.router)
app.include_router(restore.router)
app.include_router(qpr.router)
app.include_router(report.router)

@app.exception_handler(EquivalenceError)
async def unicorn_exception_handler(request: Request, exc: EquivalenceError):
    return JSONResponse(
        status_code=418,
        content={
            "ERROR" : str(exc),
            exc.name : exc.not_found
        } ,
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}