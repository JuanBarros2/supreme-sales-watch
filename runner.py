import os
import time
import json
from datetime import datetime
import matplotlib.pyplot

os.chdir(os.path.dirname(os.path.realpath(__file__)))

SCRAPY_FILE = 'scrap_file.json'


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
        new_dict[promo['id']] = {'time': promo['time'], 'temp': promo['temp']}
    return new_dict


promos_history = {}


def add_promo_change(data):
    appended = {}
    altered = {}
    for (k, v) in data.items():
        if k not in promos_history:
            promos_history[k] = [v]
            appended[k] = k
        elif promos_history[k][-1]['temp'] != v['temp']:
            promos_history[k].append(v)
            altered[k] = v
    return appended, altered

try:
    count = 0
    while count < 30:
        open(SCRAPY_FILE, 'w').close()

        os.system('scrapy runspider scraper.py -o ' + SCRAPY_FILE)
        with open(SCRAPY_FILE) as json_file:
            data = json.load(json_file)
            aux = dictfy_promos(set_time(data))
            appended, altered = add_promo_change(aux)
            print("Foram adicionados: " + str(len(appended.keys())) + " promoções")
            print("Foram alteradas: " + str(len(altered.keys())) + " promoções")
        time.sleep(10)
        count += 1
    more = list(promos_history.values())[0]
    time = list(map(lambda x: x['time'], more))
    temp = list(map(lambda x: x['temp'], more))
    print(time, temp)
    matplotlib.pyplot.plot(time, temp)
    matplotlib.pyplot.show()
except SystemExit:
    pass
