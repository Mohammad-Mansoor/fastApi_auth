from enum import Enum


class ReferenceTypeEnum(str, Enum):
    USER = "user"
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
    PRODUCT = "product"
    INVOICE = "invoice"
    PAYMENT = "payment"
    TICKET = "ticket"
    CHAT = "chat"
    OTHER = "other"