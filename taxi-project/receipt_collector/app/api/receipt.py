from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.db.session import SessionLocal
from app.schemas import ReceiptCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/receipt", status_code=201)
async def create_receipt(receipt_in: ReceiptCreate, db: Session = Depends(get_db)):
    print(jsonable_encoder(receipt_in))
    receipt = crud.receipt.create(db=db, obj_in=receipt_in)

    return receipt
