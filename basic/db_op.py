import pymysql

from basic.customer import Customer
from basic.funder import Founder


def build_customers_data(funders_map, cfg):
    customers = []  # 用户集合
    funders_customers_map = {}  # 每个资方对应的用户
    # 打开数据库连接
    db = pymysql.connect(host=cfg.db_items['host'],
                         user=cfg.db_items['user'],
                         password=cfg.db_items['pwd'],
                         database=cfg.db_items['db'])

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * FROM customers"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            funds = row[11]
            customer = Customer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            [customer.funders.append(funders_map[f]) for f in funds.split(',')]
            customers.append(customer)

            for f in funds.split(','):
                if f not in funders_customers_map:
                    funders_customers_map[f] = [customer]
                else:
                    funders_customers_map[f].append(customer)
            # 打印结果
            print(customer)
    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()

    return customers, funders_customers_map


def build_funders_data(cfg):
    funders_map = {}
    # 打开数据库连接
    db = pymysql.connect(host=cfg.db_items['host'],
                         user=cfg.db_items['user'],
                         password=cfg.db_items['pwd'],
                         database=cfg.db_items['db'])

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * FROM funders"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            funder = Founder(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                             row[11])
            funders_map[str(funder.id)] = funder
            # 打印结果
            print(funder)
    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()

    return funders_map
