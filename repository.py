import abc
from models import Worker
from models import Customer
import psycopg2


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, obj):
        pass

    @abc.abstractmethod
    def all(self):
        pass

    @abc.abstractmethod
    def get(self, id_obj):
        pass


class ShelterRepository:
    def get_animal_types(self, connection):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM type_animal')

        data = cursor.fetchall()
        cursor.close()
        connection.close()

        return data


# get_workers() -> [Worker]
# delete_worker(id_obj)
class WorkerRepository(AbstractRepository):
    def delete(self, id_obj):
        cursor = self.connection.cursor()
        worker = self.get(id_obj)

        sql = 'DELETE from accounts where account_id = %s'

        cursor.execute(sql, (worker.account_id, ))

        self.connection.commit()

        cursor.close()

    def get(self, id_obj):
        cursor = self.connection.cursor()

        sql = f'select full_name, login, pass, role, w.account_id from workers w ' \
              f'join accounts a on w.account_id = a.account_id ' \
              f'join roles r on r.role_id = a.role_id ' \
              f'where worker_id = %s'

        cursor.execute(sql, (id_obj, ))

        data = cursor.fetchone()

        worker = Worker(fio=data[0], login=data[1], password=data[2], role=data[3], account_id=data[4])

        cursor.close()

        return worker

    def __init__(self, connection):
        self.connection = connection

    def add(self, worker: Worker):
        cursor = self.connection.cursor()

        cursor.execute(f'select role_id from roles where role = \'{worker.role}\'')
        role_id = cursor.fetchall()[0][0]
        cursor.execute(f'INSERT INTO accounts(login, pass, role_id) VALUES (\'{worker.login}\', \'{worker.password}\','
                       f' {role_id})')

        cursor.execute('select max(account_id) from accounts')
        account_id = cursor.fetchall()[0][0]
        cursor.execute(f'insert into workers(full_name, account_id) values (\'{worker.fio}\', {account_id})')

        self.connection.commit()

        cursor.close()

    def all(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT full_name, login, pass, role, a.account_id FROM workers w ' 
                       'join accounts a on a.account_id = w.account_id '
                       'join roles r on r.role_id = a.role_id')

        data = cursor.fetchall()
        data = list(map(self._tuple_worker_to_dataclass_worker, data))

        cursor.close()

        return data

    def is_exists_worker(self, login: str, password: str):
        cursor = self.connection.cursor()

        sql = f'select full_name, login, pass, role from workers w ' \
              f'join accounts a on w.account_id = a.account_id' \
              f'join roles r on r.role_id = a.role_id ' \
              f'where a.login = %s and a.pass = %s;'

        cursor.execute(sql, (login, password))

        data = cursor.fetchall()

        cursor.close()

        return data

    @staticmethod
    def _tuple_worker_to_dataclass_worker(i):
        return Worker(fio=i[0], login=i[1], password=i[2], role=i[3], account_id=i[4])


class CustomerRepository(AbstractRepository):
    def delete(self, id_obj):
        cursor = self.connection.cursor()
        customer = self.get(id_obj)

        sql = 'DELETE from accounts where account_id = %s'

        cursor.execute(sql, (customer.account_id, ))

        self.connection.commit()

        cursor.close()

    def get(self, id_obj):
        cursor = self.connection.cursor()

        sql = f'select full_name, login, pass, role from customers c ' \
              f'join accounts a on c.account_id = a.account_id ' \
              f'join roles r on r.role_id = a.role_id ' \
              f'where customer_id = %s'

        cursor.execute(sql, (id_obj, ))

        data = cursor.fetchone()

        customer = Customer(fio=data[0], login=data[1], password=data[2], role=data[3])

        cursor.close()

        return customer

    def __init__(self, connection):
        self.connection = connection

    def add(self, customer: Customer):
        cursor = self.connection.cursor()

        cursor.execute(f'select role_id from roles where role = \'{customer.role}\'')
        role_id = cursor.fetchall()[0][0]
        cursor.execute(f'INSERT INTO accounts(login, pass, role_id) VALUES (\'{customer.login}\', '
                       f'\'{customer.password}\', \'{role_id}\')')

        cursor.execute('select max(account_id) from accounts')
        account_id = cursor.fetchall()[0][0]
        cursor.execute(f'insert into customers(full_name, account_id) values (\'{customer.fio}\', {account_id})')

        self.connection.commit()

        cursor.close()

    def all(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT full_name, login, pass, role, a.account_id FROM customers c '
                       'join accounts a on a.account_id = c.account_id '
                       'join roles r on r.role_id = a.role_id')

        data = cursor.fetchall()
        data = list(map(self._tuple_customer_to_dataclass_customer, data))

        cursor.close()

        return data

    def is_exists_customer(self, login: str, password: str):
        cursor = self.connection.cursor()

        sql = f'select full_name, login, pass, role from customers c ' \
              f'join accounts a on c.account_id = a.account_id' \
              f'join roles r on r.role_id = a.role_id ' \
              f'where a.login = %s and a.pass = %s;'

        cursor.execute(sql, (login, password))

        data = cursor.fetchall()

        cursor.close()

        return data

    @staticmethod
    def _tuple_customer_to_dataclass_customer(i):
        return Customer(fio=i[0], login=i[1], password=i[2], role=i[3], account_id=i[4])







