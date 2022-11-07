import dataclasses


@dataclasses.dataclass
class Worker:
    fio: str
    login: str
    password: str
    account_id: int = dataclasses.field(default=None)
    role: str = dataclasses.field(default='worker')


@dataclasses.dataclass
class Customer:
    fio: str
    login: str
    password: str
    account_id: int = dataclasses.field(default=None)
    role: str = dataclasses.field(default='customer')


@dataclasses.dataclass
class Account:
    login: str
    password: str
    role: str
