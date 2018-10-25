from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import json
import os

dirname = os.path.dirname(__file__)
quote_urls = {
    "aastock":r"http://www.aastocks.com/en/ltp/RTQuote.aspx?S=Y&Symbol=",
    "bloomberg":r"https://www.bloomberg.com/markets2/api/datastrip/{0}?locale=en&customTickerList=true"
}
patterns = {
    "aastock":r"td.c1 div[class='data-row']"
}

bloomberg_cookies={
    "MARKETS_AP":"J15",
    "SRV":"JPX02",
    "bdfpc":"004.2883739252.1532703166495",
    "agent_id":"e2744694-3dbb-4217-affa-8091ac7da145",
    "session_id":"20d14ac3-8521-466c-b2fc-3250a5dbb877",
    "session_key":"b5864f697e1e81aaaeca9a9c6598b5c7a417e9b7",
    "_user-status":"anonymous",
    "_user-ip":"112.119.149.53",
    "_ga":"GA1.2.1556701290.1532703167",
    "_gid":"GA1.2.29481693.1532703167",
    "_pxvid":"ba9ffe10-91ac-11e8-9563-c7b30a9b3501",
    "_user_newsletters":[],
    "notice_behavior":"none",
    "_tb_sess_r":"https://www.google.com.hk/",
    "_tb_t_ppg":"https://www.bloomberg.com/quote/{0}",
    "bb_geo_info":{"country":"HK","region":"Asia"},
    "_px3":r"622d8f00f613a1b36d128e77ee1bc3b48755014d90a3b435820c49401d839916:7aquRWcip2lhULufckqr/dO0NngBd/a9ksAluGIWbRi9lyPs2GzpyuuyBBphooTwVdyz447dsBfNrKiGVOyDoQ==:1000:ECHIoaaG/M/uif0fLJIZNX1i0350O+i85KYuogRIKurEp9OQom/QVpmQ6IPJPA5vzbDwfFjd8LifmI0c17shsIqOvU7EUPNgGzRchkq4m479bE/i5Mi3hmFwd9dNAk/BRJVrFGoK4OkhcsNs3wwzqEa6rYv54vJZ0B/yTip1Fc4=",
    "trc_cookie_storage":r"taboola%20global%3Auser-id=c98f9f30-5ffb-4ab7-81ef-dbbf46f18239-tuctd23412",
    "__tbc":r"{jzx}t_3qvTkEkvt3AGEeiiNNgEUwq1Wa50L-9W-qEBAFLiXX6ImMfj6RJ5WZs7Gs-s8ZrZavqsDSvGtboukHRXGxj0biWeev1NT8D1fDKoymQHr0Ixwz-I6_Gq2sTZb72KJ_jylU0Z664w9lha1BgkmqDg",
    "__pat":-14400000,
    "__pvi":{"id":"v-2018-07-27-22-52-51-316-NkFrHma8H5TIbYxR-3279770e5bb5b6b58ffd9d4d2bf22512","domain":".bloomberg.com","time":1532703172446},
    "xbc":r"{jzx}cbwt6j_j5JxcwUp-SOL92rStUmEJuzikU__7Gyq87c3cLFiVS_NGXYewzJl2xdEQse6f3G6Ae33WrsLGbUA3aw1a7IyRGlPPIlPAfrC-vj94PgRN19ossJB62GkG-rxGH7Mw94kOkavo4PIUH998VuFP9LxhQq-LAHuDoaL-_W-L6LScr1b0LKCvroB344Wf0KrFBlUO7doBB-d3vQUFNf3XTPBFSyyz3CWLJ0HnBd5WwI5vN7F6b-d699Pz6KCxnIdmI4SwtrYGc4N88dct1i3d43QktVDaaMCS97q_CDr9KGErIT6DOnboIHr2ug8vXR1reNgt87ePiSqNwV_-VfgurxXkKnSsmmlfc497PNmru1haicyyYYZMqPM1bplun69-d0QTr9mlB4DUqWLsVA",
    "__gads":r"ID=6372132c8af19200:T=1532703175:S=ALNI_Mbvlml3jPIPLOkDle85_19LUAlVeg"
    }

cookies_str=r"MARKETS_AP=J15; SRV=JPX02; bdfpc=004.2883739252.1532703166495; agent_id=e2744694-3dbb-4217-affa-8091ac7da145; session_id=20d14ac3-8521-466c-b2fc-3250a5dbb877; session_key=b5864f697e1e81aaaeca9a9c6598b5c7a417e9b7; _user-status=anonymous; _user-ip=112.119.149.53; _ga=GA1.2.1556701290.1532703167; _gid=GA1.2.29481693.1532703167; _pxvid=ba9ffe10-91ac-11e8-9563-c7b30a9b3501; _user_newsletters=[]; notice_behavior=none; _tb_sess_r=https%3A//www.google.com.hk/; _tb_t_ppg=https%3A//www.bloomberg.com/quote/1%3AHK; bb_geo_info={\"country\":\"HK\",\"region\":\"Asia\"}|1533307969659; _px3=622d8f00f613a1b36d128e77ee1bc3b48755014d90a3b435820c49401d839916:7aquRWcip2lhULufckqr/dO0NngBd/a9ksAluGIWbRi9lyPs2GzpyuuyBBphooTwVdyz447dsBfNrKiGVOyDoQ==:1000:ECHIoaaG/M/uif0fLJIZNX1i0350O+i85KYuogRIKurEp9OQom/QVpmQ6IPJPA5vzbDwfFjd8LifmI0c17shsIqOvU7EUPNgGzRchkq4m479bE/i5Mi3hmFwd9dNAk/BRJVrFGoK4OkhcsNs3wwzqEa6rYv54vJZ0B/yTip1Fc4=; trc_cookie_storage=taboola%2520global%253Auser-id%3Dc98f9f30-5ffb-4ab7-81ef-dbbf46f18239-tuctd23412; __tbc=%7Bjzx%7Dt_3qvTkEkvt3AGEeiiNNgEUwq1Wa50L-9W-qEBAFLiXX6ImMfj6RJ5WZs7Gs-s8ZrZavqsDSvGtboukHRXGxj0biWeev1NT8D1fDKoymQHr0Ixwz-I6_Gq2sTZb72KJ_jylU0Z664w9lha1BgkmqDg; __pat=-14400000; __pvi=%7B%22id%22%3A%22v-2018-07-27-22-52-51-316-NkFrHma8H5TIbYxR-3279770e5bb5b6b58ffd9d4d2bf22512%22%2C%22domain%22%3A%22.bloomberg.com%22%2C%22time%22%3A1532703172446%7D; xbc=%7Bjzx%7Dcbwt6j_j5JxcwUp-SOL92rStUmEJuzikU__7Gyq87c3cLFiVS_NGXYewzJl2xdEQse6f3G6Ae33WrsLGbUA3aw1a7IyRGlPPIlPAfrC-vj94PgRN19ossJB62GkG-rxGH7Mw94kOkavo4PIUH998VuFP9LxhQq-LAHuDoaL-_W-L6LScr1b0LKCvroB344Wf0KrFBlUO7doBB-d3vQUFNf3XTPBFSyyz3CWLJ0HnBd5WwI5vN7F6b-d699Pz6KCxnIdmI4SwtrYGc4N88dct1i3d43QktVDaaMCS97q_CDr9KGErIT6DOnboIHr2ug8vXR1reNgt87ePiSqNwV_-VfgurxXkKnSsmmlfc497PNmru1haicyyYYZMqPM1bplun69-d0QTr9mlB4DUqWLsVA; __gads=ID=6372132c8af19200:T=1532703175:S=ALNI_Mbvlml3jPIPLOkDle85_19LUAlVeg"
begin_index = 0
def load_securities(file_path):
    """Get all securities symbol from excel"""
    df = pd.read_excel(file_path,sheet_name=0,skiprows=2)
    syb_list=[]
    global begin_index
    for i in range(len(df)):
        syb = str(df.iloc[i]['股份代號'])
        syb_list.append(syb)
        if(syb=='05519' or syb=='5519'):
            begin_index = i
            print("================>begin_index:"+str(begin_index))
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
    url=r"https://www1.hkex.com.hk/hkexwidget/data/getequityquote?sym={0}&token=evLtsLsBNAUVTPxtGqVeG6Bdzbrr1hMJeHi67j97RODZ0%2fXyBAIyDuHfHLT5syF3&lang=chi&qid=1532790676100&callback=jQuery31106431252646402639_1532790674347&_=1532790674348"
    #sybs = ['1','2','3']
    url = url.replace(r"{0}",syb)
    r = requests.get(url)
    try:
        print(1)
        m = re.search(r"\{.+\}", r.text)
        if(m is None):
            return
        print(2)    
        resp = json.loads(m.group(0))
        if('data' in resp):
            print(3)
            if('quote' in resp['data']):
                print(4)
                quote = resp['data']['quote']
                content = json.dumps(quote)
                print("===>"+syb)
                with open(dirname+r'/resources/data.json', 'ab') as writer:
                    writer.write(bytes(content+'\n','UTF-8'))
    except:
        print("Error for symbol:"+syb)
    # res = json.loads(m.group(0))
    # stock_quote = res['data']['quote']
    # ric = stock_quote['ric']
    # ind_class = stock_quote['hsic_ind_classification']
    # issuer_name = stock_quote['issuer_name']
    # sub_ind_class = stock_quote['hsic_sub_sector_classification']
    # high = stock_quote['hi']
    # low = stock_quote['lo']
    # print()

def get_stock_aastock(syb):
    url = "http://www.aastocks.com/en/stocks/analysis/company-fundamental/company-profile?symbol="
    quote_url = ""
    r = requests.get(url+syb)
    bs = BeautifulSoup(r.text,"lxml")
    indust = bs.select('table[class="cnhk-cf tblM s4 s5 mar15T"] tr:nth-of-type(5) > td')
    label = indust[0].text
    value = indust[1].text
    print("")

def get_stock_bloomberg(syb):
    url = quote_urls["bloomberg"]
    url = url.replace(r"{0}",syb)
    #cookie = json.loads(cookies_str)
    cookies_str.replace(r"{0}",syb)
    #print(cookies_str)
    cookie_1={"cookie":cookies_str}
    r = requests.get(url, cookies=cookie_1).text
    print(r)

if __name__ == "__main__":
    #get_stock_aastock("3")
    print(dirname)
    sec_list = load_securities(dirname+"/resources/ListOfSecurities_c.xlsx")
    print(begin_index)
    for j in range(len(sec_list)):
        if(j>begin_index):
            get_stock_hkex(sec_list[j])
    # get_stock_hkex('1')
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