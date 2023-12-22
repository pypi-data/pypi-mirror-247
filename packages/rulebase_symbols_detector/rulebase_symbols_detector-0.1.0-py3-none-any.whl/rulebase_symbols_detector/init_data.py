import requests
import json
json_data = requests.get('https://services.entrade.com.vn/market-api/tickers?_end=10000').json()
json_data['created_date'] = '2023-12-20'
with open('init_data.json', 'w') as fp:
    json.dump(json_data, fp, ensure_ascii=False)
# print(requests.get('https://services.entrade.com.vn/market-api/tickers?_end=10000').json())
# with open('init_data.json') as fp:
#     print(json.load(fp))