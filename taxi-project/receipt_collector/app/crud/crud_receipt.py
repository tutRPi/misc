from app.crud.base import CRUDBase
from app.models.receipt import Receipt
from app.schemas.receipt import ReceiptCreate


class CRUDRReceipt(CRUDBase[Receipt, ReceiptCreate, None]):
    pass


receipt = CRUDRReceipt(Receipt)
