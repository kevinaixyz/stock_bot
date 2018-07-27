from bs4 import BeautifulSoup
import requests
import pandas
import re
import json

quote_urls = {
    "aastock":r"http://www.aastocks.com/en/ltp/RTQuote.aspx?S=Y&Symbol=",
    "bloomberg":r"https://www.bloomberg.com/markets2/api/datastrip/{0}?locale=en&customTickerList=true"
}
patterns = {
    "aastock":r"td.c1 div[class='data-row']"
}
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

def get_stock_hkex(syb):
    """Get securies info from HK exchange"""
    url="https://www1.hkex.com.hk/hkexwidget/data/getequityquote?sym="
    append = "&token=evLtsLsBNAUVTPxtGqVeGxEu1Lw6GUhHTgBujSWIICBHcSJpixVPSjL0FGezYNZM&lang=chi&qid=1532612941779&callback=jQuery3110055439012518593955_1532612939419&_=1532612939420"
    #sybs = ['1','2','3']
    r = requests.get(url+syb+append)
    m = re.search(r"\{.+\}", r.text)
    res = json.loads(m.group(0))
    stock_quote = res['data']['quote']
    ric = stock_quote['ric']
    ind_class = stock_quote['hsic_ind_classification']
    issuer_name = stock_quote['issuer_name']
    sub_ind_class = stock_quote['hsic_sub_sector_classification']
    high = stock_quote['hi']
    low = stock_quote['lo']
    print(ric+":"+issuer_name+":"+ind_class)

def get_stock_aastock(syb):
    url = "http://www.aastocks.com/en/stocks/analysis/company-fundamental/company-profile?symbol="
    quote_url = ""
    r = requests.get(url+syb)
    bs = BeautifulSoup(r.text,"lxml")
    indust = bs.select('table[class="cnhk-cf tblM s4 s5 mar15T"] tr:nth-of-type(5) > td')
    label = indust[0].text
    value = indust[1].text
    print(price_range)

def get_stock_bloomberg(syb):
    url = quote_urls["bloomberg"]
    url = url.replace(r"{0}",syb)
    r = requests.get(url).text
    cookies = {}
    print(r)
    qoute = json.loads(r)
    print(quote)

    
if __name__ == "__main__":
    #get_stock_aastock("3")
    get_stock_bloomberg("1:HK")
    #print(len(sybs))
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