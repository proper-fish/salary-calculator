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


loop = asyncio.get_event_loop()


# Get sales for a set period of time (start & end date inclusively) --by promoter
async def get_sales_by_promoter(vr_code: str, start_date, end_date=None) -> List[SaleEntry]:
    if end_date is None:
        end_date = start_date

    conn = await aiomysql.connect(**db_config, loop=loop)
    cur = await conn.cursor()

    select_script = '''
        SELECT telegreen_id, order_status, telegreen_total_count, 
        telegreen_total_sum, telegreen_sname, telegreen_approved_date 
        FROM telegreen_direct_orders
        WHERE CAST(telegreen_approved_date AS date) 
        BETWEEN CAST(%s AS date) AND CAST(%s AS datetime)
        AND telegreen_sname = %s;'''

    await cur.execute(select_script, (start_date, end_date, vr_code))
    sale_entries = await cur.fetchall()
    await cur.close()
    conn.close()
    return [SaleEntry(*entry) for entry in sale_entries]


# Get all sales for a set period of time (start & end date inclusively)
async def get_all_sales(start_date, end_date=None) -> List[SaleEntry]:
    if end_date is None:
        end_date = start_date

    conn = await aiomysql.connect(**db_config, loop=loop)
    cur = await conn.cursor()

    select_script = '''
        SELECT telegreen_id, order_status, telegreen_total_count, 
        telegreen_total_sum, telegreen_sname, telegreen_approved_date 
        FROM telegreen_direct_orders
        WHERE CAST(telegreen_approved_date AS date) 
        BETWEEN CAST(%s AS date) AND CAST(%s AS datetime);'''

    await cur.execute(select_script, (start_date, end_date))
    sale_entries = await cur.fetchall()
    await cur.close()
    conn.close()
    return [SaleEntry(*entry) for entry in sale_entries]


# a = loop.run_until_complete(get_sales_by_promoter('vr96935', datetime(2022, 12, 1), '2022-12-01'))
# b = loop.run_until_complete(get_sales_by_promoter('vr96935', datetime(2022, 12, 1)))
# print(a == b)

test = loop.run_until_complete(get_sales_by_promoter('vr119787', datetime(2022, 12, 2), datetime(2022, 12, 3)))
print(test)

test_all = loop.run_until_complete(get_all_sales(datetime(2022, 12, 3), datetime(2022, 12, 3)))
print(test_all)
