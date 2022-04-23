
import pymysql
import time


def insert_market_mapping():
    conn = pymysql.connect('106.12.204.53', 'hhkhan', 'Anker61#$', 'farm_products', 3306, charset='utf8')
    file = "../data/ap/ap_market_mapping"
    cursor = conn.cursor()
    with open(file, 'r', encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.strip()
            segs = line.split('\t')
            sql = 'insert into `ap_mapping` (`id`, `market_name`) values ({}, "{}")'.format(segs[0], segs[1])
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                conn.rollback()
    cursor.close()
    conn.close()


def insert_price():
    conn = pymysql.connect('106.12.204.53', 'hhkhan', 'Anker61#$', 'farm_products', 3306, charset='utf8')
    file = "../data/ap/ap_price"
    cursor = conn.cursor()
    with open(file, 'r', encoding='utf-8') as fin:
        for line in fin.readlines():
            time.sleep(0.001)
            line = line.strip()
            segs = line.split('\t')
            sql = 'insert into `ap_price` (`date`, `mid`, `price`) values ("{}", {}, {})'\
                .format(segs[0], segs[1], segs[2])
            print(sql)
            cursor.execute(sql)
            conn.commit()
            conn.rollback()
    cursor.close()
    conn.close()


def 


if __name__ == '__main__':
    # insert_market_mapping()
    insert_price()

