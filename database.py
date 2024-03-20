import config
import pymysql.cursors
import time
import datetime
from logger_config import logger
import traceback


class Database:
    def __init__(self):
        try:
            self.con = pymysql.connect(**config.mysql_config)

        except pymysql.err.OperationalError as e:
            logger.error(f"OperationalError: {e}")
            raise e
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)
        self.create_tables()

    def create_tables(self):
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS records (
                id_record INT AUTO_INCREMENT PRIMARY KEY UNIQUE,
                link TEXT,
                chat_id BIGINT,
                created_date TEXT,
                checking_date TEXT,
                params TEXT,
                is_join BOOLEAN
                )
""")
        self.con.commit()

    def get_columns(self, table):
        self.cur.execute(f"SHOW COLUMNS FROM {table}")
        columns_dict = self.cur.fetchall()
        columns = []
        if columns_dict:
            for column in columns_dict:
                columns.append(column.get("Field"))
        return columns

    def refresh(self):
        self.con = pymysql.connect(**config.mysql_config)
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)

    @staticmethod
    def generate_time_now():
        t_time = str(datetime.datetime.now())
        t_time = t_time.split(r'.')[0]
        return t_time

    @staticmethod
    def db_method_wrapper(func):
        def wrapped(self, *args, **kwargs):
            try:
                self.con.ping()
                return func(self, *args, **kwargs)
            except Exception as a:
                traceback.print_exc()
                logger.error(f"Error DB: {a} 1/2")
                try:
                    self.refresh()
                    time.sleep(1)
                    self.refresh()
                    return func(self, *args, **kwargs)
                except Exception as e:
                    logger.error(f"Error DB: {e} 2/2")

        return wrapped

    @db_method_wrapper
    def select_sqlite(self, table, values='*', where='', inserts=(), fetchall=False):
        self.__init__()
        if where != '':
            where = f"WHERE {where}"

        sql = f"SELECT {values} FROM {table} {where}"
        # logger.info(sql)
        self.cur.execute(sql, inserts)
        if fetchall:
            result = self.cur.fetchall()
        else:
            result = self.cur.fetchone()
        return result

    @db_method_wrapper
    def update_sqlite(self, table, column, value, where=''):
        if where != '':
            where = f'WHERE {where}'
        sql = f'UPDATE {table} SET {column} = %s {where}'
        # logger.info(sql, value)
        self.cur.execute(sql, (value,))
        self.con.commit()
        return True

    @db_method_wrapper
    def insert_sqlite(self, table, columns_list, values):
        columns = ', '.join(columns_list)
        placeholders = ', '.join(['%s' for _ in values])
        sql = f'INSERT INTO {table} ({columns}) VALUES({placeholders})'
        logger.info(f"SQL: {sql}\nValues: {values}")
        self.cur.execute(sql, values)
        self.con.commit()
        self.refresh()
        return True

    @db_method_wrapper
    def delete_sqlite(self, table, where=''):
        if where != '':
            where = f'WHERE {where}'
        sql = f'DELETE FROM {table} {where}'
        self.cur.execute(sql)
        self.con.commit()

    @db_method_wrapper
    def get_record(self, invite_link=None, id_record=None):
        if invite_link:
            record = self.select_sqlite(table="records", where=f"link=%s", inserts=(invite_link, ))
        elif id_record:
            record = self.select_sqlite(table="records", where=f"id_record={id_record}")
        else:
            return None
        return record

    @db_method_wrapper
    def save_record(self, invite_link, chat_id, params):
        # invite_link = f'"{invite_link}"'
        created_date = self.generate_time_now()
        checking_date = None
        is_join = None
        columns = ["link", "chat_id", "created_date", "checking_date", "params", "is_join"]
        values = [invite_link, chat_id, created_date, checking_date, params, is_join]
        self.insert_sqlite(table="records", columns_list=columns, values=values)
        record = self.get_record(invite_link=invite_link)
        return record

    @db_method_wrapper
    def set_new_join(self, is_join, id_record):
        self.update_sqlite(table="records", column="is_join", value=is_join, where=f"id_record={id_record}")
        self.update_sqlite(table="records", column="checking_date", value=self.generate_time_now(),
                           where=f"id_record={id_record}")


dbase = Database()
