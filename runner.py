import os
import time
import json
from datetime import datetime
import matplotlib.pyplot
from functools import reduce
import pandas as pd

os.chdir(os.path.dirname(os.path.realpath(__file__)))

SCRAPY_FILE = 'scrap_file.json'
PROMO_FILE = 'promo_file.csv'

promos_history = {}
promos_info = {}


def set_time(data):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    with open(SCRAPY_FILE) as json_file:
        data = json.load(json_file)
        for promo in data:
            promo['time'] = current_time
        return data
    return []


def dictfy_promos(data):
    new_dict = {}
    for promo in data:
        new_dict[promo['id']] = promo
    return new_dict


def add_promo_change(data):
    appended = {}
    altered = {}
    for (k, v) in data.items():
        if k not in promos_history:
            promos_history[k] = [{'time': v['time'], 'temp': v['temp']}]
            promos_info[k] = v
            appended[k] = v
        elif promos_history[k][-1]['temp'] != v['temp']:
            promos_history[k].append({'time': v['time'], 'temp': v['temp']})
            altered[k] = v
    return appended, altered


try:
    count = 0
    while count < 2:
        open(SCRAPY_FILE, 'w').close()

        os.system('scrapy runspider scraper.py -o ' + SCRAPY_FILE)
        with open(SCRAPY_FILE) as json_file:
            data = json.load(json_file)
            aux = dictfy_promos(set_time(data))
            appended, altered = add_promo_change(aux)
            print("Foram adicionados: " +
                  str(len(appended.keys())) + " promoções")
            print("Foram alteradas: " + str(len(altered.keys())) + " promoções")

        time.sleep(10)
        count += 1
    df = pd.DataFrame(data={key: [value[key] for value in list(promos_info.values(
    ))] for key in list(promos_info.values())[0].keys()})
    df.to_csv(PROMO_FILE, index=False)

except SystemExit:
    pass
