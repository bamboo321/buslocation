import requests
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup


# busstop_multi_res = requests.get('https://www2.city.kyoto.lg.jp/kotsu/webguide/xml/busstop_multi.xml')


class Busstop:
    busstop_multi = None

    def __init__(self):
        Busstop_multi_res = requests.get('https://www2.city.kyoto.lg.jp/kotsu/webguide/xml/busstop_multi.xml')
        Busstop.busstop_multi = ET.fromstring(Busstop_multi_res.content)
        print(Busstop_multi_res)
        print(Busstop.busstop_multi)

    def retrieve_bcode(self, stname: str):
        for stop in Busstop.busstop_multi:
            if stop.find('kanji').text == stname:
                return stop.find('bcode').text


class Destination:
    baseURL = 'http://blsetup.city.kyoto.jp/blsp/step3.php'

    def __init__(self, bcode):
        self.bcode = bcode
        self.destlist = self.fetch_destlist()
        self.choosed_destlist = []

    def fetch_destlist(self):
        params = {'id': self.bcode}
        res = requests.get(Destination.baseURL, params=params)
        soup = BeautifulSoup(res.content, "html.parser")

        destlist = []
        for dest in soup.find_all("li", class_="list-group-item bls-keitou-list"):
            di = dict()
            di['dist'] = dest.get_text().strip()
            # keitou -> ktocdに変換したほうがよいかも
            di['keitou'] = dest.find("img")['alt']
            di['name'] = dest.find("input")['name']
            di['value'] = dest.find("input")['value']

            destlist.append(di)

        return destlist

    def choose_dest(self, *destsname):
        print(destsname)
        self.choosed_destlist = [destdict for destdict in self.destlist if destdict.get('dist') in destsname]


class Location:
    baseURL = ''

    def __init__(self):
        pass



if __name__ == '__main__':
    # テスト用
    b = Busstop()
    kyotost = b.retrieve_bcode('京都駅前')

    d = Destination(kyotost)
