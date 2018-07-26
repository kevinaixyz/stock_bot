from bs4 import BeautifulSoup
import requests
import pandas
import re
import json

def load_securities(file_path):
    """Get all securities symbol from excel"""
    df = pandas.read_excel(file_path,sheet_name=0,skiprows=2)
    syb_list=[]
    for i in range(len(df)):
        syb = str(df.iloc[i]['股份代號'])
        syb_list.append(syb)
        #print(df.iloc[i]['股份代號'])
        #get_stock_info(syb)
    return syb_list   

def cal_industry_pct():
    map={}
    return 0

def write_file(file_path):
    """write info to file"""

def get_stock_info(syb):
    """Get securies info from HK exchange"""
    url="https://www1.hkex.com.hk/hkexwidget/data/getequityquote?sym="
    append = "&token=evLtsLsBNAUVTPxtGqVeGxEu1Lw6GUhHTgBujSWIICBHcSJpixVPSjL0FGezYNZM&lang=chi&qid=1532612941779&callback=jQuery3110055439012518593955_1532612939419&_=1532612939420"
    #sybs = ['1','2','3']
    r = requests.get(url+syb+append)
    m = re.search("\{.+\}", r.text)
    res = json.loads(m.group(0))
    stock_quote = res['data']['quote']
    ric = stock_quote['ric']
    ind_class = stock_quote['hsic_ind_classification']
    issuer_name = stock_quote['issuer_name']
    sub_ind_class = stock_quote['hsic_sub_sector_classification']
    high = stock_quote['hi']
    low = stock_quote['lo']
    print(ric+":"+issuer_name+":"+ind_class)

if __name__ == "__main__":
    sybs = load_securities("F:\Downloads\ListOfSecurities_c.xlsx")
    print(len(sybs))
    # url="https://www1.hkex.com.hk/hkexwidget/data/getequityquote?sym="
    # append = "&token=evLtsLsBNAUVTPxtGqVeGxEu1Lw6GUhHTgBujSWIICBHcSJpixVPSjL0FGezYNZM&lang=chi&qid=1532612941779&callback=jQuery3110055439012518593955_1532612939419&_=1532612939420"
    # sybs = ['1','2','3']
    # for syb in sybs:
    #     r = requests.get(url+syb+append)
    #     m = re.search("\{.+\}", r.text)
    #     res = json.loads(m.group(0))
    #     stock_quote = res['data']['quote']
    #     ric = stock_quote['ric']
    #     ind_class = stock_quote['hsic_ind_classification']
    #     issuer_name = stock_quote['issuer_name']
    #     sub_ind_class = stock_quote['hsic_sub_sector_classification']
    #     print(ric+":"+issuer_name)
