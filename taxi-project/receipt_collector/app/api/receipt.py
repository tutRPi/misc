import logging

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.db.session import SessionLocal
from app.rabbitmq.producer import publish
from app.schemas import ReceiptCreate, Receipt
from app.schemas.receipt import ReceiptForwardMessage

router = APIRouter()

logger = logging.getLogger("api")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/receipt", status_code=201, response_model=Receipt)
async def create_receipt(receipt_in: ReceiptCreate, db: Session = Depends(get_db)):
    receipt = crud.receipt.create(db=db, obj_in=receipt_in)

    logger.info("Receipt saved, send now to queue")

    receipt_forward_message = ReceiptForwardMessage.from_orm(receipt)
    publish("Receipt", jsonable_encoder(receipt_forward_message))

    return receipt
