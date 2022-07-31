#encoding: utf-8
"""
从北京市住建委爬取网签数据
"""
from lxml import etree
from datetime import date
from utils import get_html, save_html
from db.config import create_connect


BASE_URL = 'http://zjw.beijing.gov.cn/bjjs/fwgl/index.shtml#cxfw1'
today = date.today().strftime('%Y-%m-%d')


def _parse_table(table: etree.Element):
    trs = table.xpath('.//tr')
    res = {}
    pre_key = None
    for i, tr in enumerate(trs):
        if i == 0:
            # 第一行是标题
            title = tr.xpath('./td[1]/text()')[0].replace(' ', '').replace('\r\n', '')
        else:
            # 只关心前10行，都是2列的
            tds = tr.xpath('./td')
            if len(tds) < 2:
                break
            key = tds[0].xpath('./text()')[0]
            if key.find('其中'):
                key = key.replace('\xa0', '').replace('其中', '')
            key = key.replace('：', '').replace(' ', '').replace('\r\n', '')

            value = tds[1].xpath('./text()')[0].replace(' ', '').replace('\r\n', '')
            
            if i % 2 == 1:
                res[key] = [value, '']
                pre_key = key
            else:
                res[pre_key][1] = value
    return title, res

def _parse_commercial_table(td: etree.Element):
    """
    解析一个小的td包围的列, 商品房
    Args:
        td (etree.Element): _description_
    """
    table = td.xpath('./table')[0]
    return _parse_table(table)

def _parse_stock_table(table: etree.Element):
    """
    存量房解析，在第二列
    """
    td = table.xpath('./tr/td')[1]
    table = td.xpath('.//table')[0]
    title, res = _parse_table(table)
    return title, res

def _parse_detail(ehtml):
    div = ehtml.xpath('//div/title[text()="商品房数据统计"]/..')
    tables = div[0].xpath('./table')
    commercial_table = tables[1]
    res = {}
    for tr in commercial_table:
        tds = tr.xpath('./td')
        for td in tds:
            title, dict_stat = _parse_commercial_table(td)
            res[title] = dict_stat
    
    div = ehtml.xpath('//div/title[text()="存量房网上签约统计"]/..')
    tables = div[0].xpath('./table')
    stock_table = tables[1]
    title, dict_stat = _parse_stock_table(stock_table)
    res[title] = dict_stat
    return res


def gen_sql(format_day, dict_val, conf):
    table_name = conf['table']
    mapping = conf['columns_mapping']

    fix_mapping = {
        '住宅套数': 'residential',
        '商业单元': 'commertial',
        '办公单元': 'office',
        '车位个数': 'parking'
    }
    mapping.update(fix_mapping)

    slots = {}
    for zh_name, lst_val in dict_val.items():
        if zh_name in mapping:
            prefix = mapping[zh_name]
            slots[f'{prefix}_number'] = lst_val[0]
            slots[f'{prefix}_area'] = lst_val[1]
    
    sql_data = slots.items()
    sql_cols = ['day'] + [pair[0] for pair in sql_data]
    sql_vals = [format_day] + [pair[1] for pair in sql_data]
    cols = ','.join([f'`{c}`' for c in sql_cols])
    vals = ','.join([f'\'{c}\'' for c in sql_vals])

    sql = f'insert into {table_name} ({cols}) values ({vals})' + \
        f' on duplicate key update day=\'{format_day}\';'
    print(sql)
    return sql


def save_to_mysql(data):
    """
    保存到mysql中
    """
    conn = create_connect('bj_house')
    cursor = conn.cursor()
    cursor.execute('show tables;')
    result = cursor.fetchall()
    print('tables:', result)

    table_mapping = {
        "可售期房统计": {
            'table': 'future_stat',
            'columns_mapping': {
                '可售房屋套数': 'total',
            }
        },
        "期房网上签约": {
            'table': 'future_deal',
            'columns_mapping': {
                '网上签约套数': 'total',
            }
        },
        "未签约现房统计": {
            'table': 'completed_stat',
            'columns_mapping': {
                '未签约套数': 'total',
            }
        },
        "现房网上签约": {
            'table': 'completed_deal',
            'columns_mapping': {
                '网上签约套数': 'total',
            }
        },
        "存量房网上签约": {
            'table': 'stock_deal',
            'columns_mapping': {
                '网上签约套数': 'total',
                '住宅签约套数': 'residential'
            }
        },
    }
    
    data_day = ''
    for key in data:
        if key.find('期房网上签约') >= 0:
            data_day = key.replace('期房网上签约', '')
    
    items = data_day.split('/')
    format_day = date(*[int(v) for v in items]).strftime('%Y%m%d')
    print(f'format_day={format_day}')
    
    for key, dict_val in data.items():
        if key.startswith(data_day) >= 0:
            key = key.replace(data_day, '')
        if key in table_mapping:
            conf = table_mapping[key]
            sql = gen_sql(format_day, dict_val, conf)
            cursor.execute(sql)
    
    conn.commit()
    cursor.close()
    conn.close()

def get_data():
    """
    获取数据
    """
    base_html = get_html(BASE_URL)
    ehtml = etree.HTML(base_html)
    lst_href = ehtml.xpath('//div[@id="fwgl_con5"]//a[@title="更多"]/@href')
    detail_url = lst_href[0]
    print(f'[{today}] detail_url={detail_url}')
    detail_html = get_html(detail_url)
    save_html(detail_html, f'./data/house.{today}.html')
    
    ehtml = etree.HTML(detail_html)
    data = _parse_detail(ehtml)
    return data
    

def main():
    data = get_data()
    print(data)
    save_to_mysql(data)

if __name__ == '__main__':
    main()