import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Annotated

from database import database as database
from database.database import DrugDB
from model.model import Drug

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.post("/add_drug")
async def add_drug(drug: Drug, db: db_dependency):
    new_drug = DrugDB(**drug.dict())
    db.add(new_drug)
    db.commit()
    db.refresh(new_drug)
    return new_drug


@app.get("/get_drugs")
async def get_drugs(db: db_dependency):
    return db.query(DrugDB).all()


@app.get("/get_drug_by_id")
async def get_drug_by_id(drug_id: int, db: db_dependency):
    drug = db.query(DrugDB).filter(DrugDB.id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return drug


@app.put("/update_drug")
async def update_drug(drug_id: int, drug: Drug, db: db_dependency):
    db_drug = db.query(DrugDB).filter(DrugDB.id == drug_id).first()
    if not db_drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    for var, value in drug.dict(exclude_unset=True).items():
        setattr(db_drug, var, value)
    db.commit()
    db.refresh(db_drug)
    return jsonable_encoder(db_drug)


@app.delete("/delete_drug")
async def delete_drug(drug_id: int, db: db_dependency):
    db_drug = db.query(DrugDB).filter(DrugDB.id == drug_id).first()
    if not db_drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    db.delete(db_drug)
    db.commit()
    return {"message": "Drug deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
