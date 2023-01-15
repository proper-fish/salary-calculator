import asyncio
import aiomysql
from datetime import datetime
from typing import NamedTuple, List
from config import SALES_DB_HOST, SALES_DB_NAME, SALES_DB_PASS, SALES_DB_USER, SALES_DB_PORT

db_config = {'host': SALES_DB_HOST,
             'port': SALES_DB_PORT,
             'user': SALES_DB_USER,
             'password': SALES_DB_PASS,
             'db': SALES_DB_NAME,
             }


class SaleEntry(NamedTuple):
    green_id: int
    order_status: str
    count: int
    full_sum: int
    vr_code: str
    sale_time: datetime


class Ticket(NamedTuple):
    green_id: int
    order_status: str
    price: int
    vr_code: str
    sale_time: datetime


loop = asyncio.get_event_loop()


class DBConnection:
    def __init__(self, host, port, user, password, db):
        self.conn = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    async def create(self):
        self.conn = await aiomysql.connect(host=self.host, port=self.port, user=self.user,
                                           password=self.password, db=self.db, loop=loop)
        return self.conn

    async def close(self):
        self.conn.close()


class ConnectorSalesBase:
    def __init__(self, db: DBConnection):
        self.db = db

    # Get sales for a set period of time (start & end date inclusively) --by promoter
    async def get_sales_by_promoter(self, vr_code: str, start_date, end_date=None) -> List[SaleEntry]:
        if end_date is None:
            end_date = start_date

        conn = await self.db.create()
        cur = await conn.cursor()

        select_script = '''
            SELECT telegreen_id, order_status, telegreen_total_count, 
            telegreen_total_sum, telegreen_sname, telegreen_approved_date 
            FROM telegreen_direct_orders
            WHERE CAST(telegreen_approved_date AS date) 
            BETWEEN CAST(%s AS date) AND CAST(%s AS date)
            AND telegreen_sname = %s
            AND order_status = 'print';'''

        await cur.execute(select_script, (start_date, end_date, vr_code))
        sale_entries = await cur.fetchall()
        await cur.close()
        return [SaleEntry(*entry) for entry in sale_entries]

    # Get all sales for a set period of time (start & end date inclusively)
    async def get_all_sales(self, start_date, end_date=None) -> List[SaleEntry]:
        if end_date is None:
            end_date = start_date

        conn = await self.db.create()
        cur = await conn.cursor()

        select_script = '''
            SELECT telegreen_id, order_status, telegreen_total_count, 
            telegreen_total_sum, telegreen_sname, telegreen_approved_date 
            FROM telegreen_direct_orders
            WHERE CAST(telegreen_approved_date AS date) 
            BETWEEN CAST(%s AS date) AND CAST(%s AS date)
            AND order_status = 'print';'''

        await cur.execute(select_script, (start_date, end_date))
        sale_entries = await cur.fetchall()
        await cur.close()
        return [SaleEntry(*entry) for entry in sale_entries]
