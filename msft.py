#!/usr/bin/python3
import urllib.request
import os
from pathlib import Path

csv_url = 'https://download.microsoft.com/download/B/2/A/B2AB28E1-DAE1-44E8-A867-4987FE089EBE/msft-public-ips.csv'

tmp_csv_path = Path('/opt/.../tmp_msft_csv.csv')
#tmp_csv_path = Path('D:\\...\\tmp_msft_csv.csv')

table_path = Path('/opt/.../msft_table.txt')
#table_path = Path('D:\\...\\msft.txt')

urllib.request.urlretrieve(csv_url, str(tmp_csv_path))

raw_ip_list = []

with open(str(tmp_csv_path), 'r') as fin:
    for row in fin:
        raw_ip_list.append(row.split()[0].replace("'", "").replace("Prefix,Type", "").replace(",",""))

with open(str(table_path), 'w') as fin:
    fin.write('\n'.join(sorted(set([ip for ip in raw_ip_list]))))

os.remove(str(tmp_csv_path))