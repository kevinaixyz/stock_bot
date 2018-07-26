from bs4 import BeautifulSoup
import requests
import pandas
import re
import json

def loadListOfStock(file_path):
    pandas.read_excel(file_path)



if __name__ == "__main__":
    url="https://www1.hkex.com.hk/hkexwidget/data/getequityquote?sym="
    append = "&token=evLtsLsBNAUVTPxtGqVeGxEu1Lw6GUhHTgBujSWIICBHcSJpixVPSjL0FGezYNZM&lang=chi&qid=1532612941779&callback=jQuery3110055439012518593955_1532612939419&_=1532612939420"
    sybs = ['1','2','3']
    for syb in sybs:
        r = requests.get(url+syb+append)
        m = re.search("\{.+\}", r.text)
        res = json.loads(m.group(0))
        stock_quote = res['data']['quote']
        ric = stock_quote['ric']
        ind_class = stock_quote['hsic_ind_classification']
        issuer_name = stock_quote['issuer_name']
        sub_ind_class = stock_quote['hsic_sub_sector_classification']
        print(ric+":"+issuer_name)
