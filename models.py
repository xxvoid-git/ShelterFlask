import dataclasses


@dataclasses.dataclass
class Worker:
    fio: str
    login: str
    password: str
    role: str
    account_id: int


@dataclasses.dataclass
class Customer:
    fio: str
    login: str
    password: str
    role: str
    account_id: int
