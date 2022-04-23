"""
处理 全国农产品商务信息公共服务平台 爬取的数据
"""
import os
from typing import Dict, Tuple


def process_folder(raw, prefix):
    """
    原始数据会保存在两个表里面
    jd_market_mapping: id, market_name
    jd_price: date, market_id, price
    :param raw: 保存原始数据的文件夹， 里面各种csv文件
    :param prefix 不同的品种，如jd, ap
    :return:
    """

    files = os.listdir(raw)
    all_data = {} # (date, market_name) -> price
    for file in files:
        if file.endswith('.csv'):
            process_file(os.path.join(raw, file), all_data)
    market_set = set()
    for key in all_data.keys():
        market_set.add(key[1])
    id2market = list(market_set)
    id2market = sorted(id2market)
    market2id = {}
    for i, name in enumerate(id2market):
        market2id[name] = i
    with open(os.path.join(raw, prefix + '_market_mapping'), 'w', encoding='utf-8', newline='\n') as fout1:
        for i, name in enumerate(id2market):
            fout1.write('{}\t{}\n'.format(i, name))
    sorted_data = sorted(all_data.items(), key=lambda x: x[0][0]+x[0][1])
    with open(os.path.join(raw, prefix + '_price'), 'w', encoding='utf-8', newline='\n') as fout2:
        for key, value in sorted_data:
            fout2.write('{}\t{}\t{}\n'.format(key[0], market2id[key[1]], value))


def process_file(file, out_data: Dict[Tuple[str, str], float]):
    with open(file, 'r', encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.strip()
            segs = line.split(',')
            key = (segs[0], segs[4])
            value = float(segs[2])
            out_data[key] = value


if __name__ == '__main__':
    raw_folder = r"D:\code\python\every_crawler\data\ap"
    process_folder(raw_folder, 'ap')
