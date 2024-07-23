from fastapi import FastAPI
from .router import inserter, tables, db, pro, tutorial, restore, qpr
from .database import engine
from .schema import PER, PES

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



@app.get("/")
async def root():
    return {"message": "Hello World"}