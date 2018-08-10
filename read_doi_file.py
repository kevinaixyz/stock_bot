import pandas as pd
import numpy as np
import datetime
import os
import os.path
import re
from model.DoiExcelData import DoiExcelData
from model.HoldInfo import HoldInfo
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
import csv

combined_df=None
doi_pair_rdd = None
trade_date_list=[]
hold_dict={}
long_hold = "LONG"
short_hold = "SHORT"
iso_date_format = "%Y-%m-%d"
cal_format = "%Y%m%d"
columns = ("Criteria 1",
           "Criteria 2",
           "Criteria 3",
           "Criteria",
           "Total Issued Shares of the Underlying Company/Corporation",
           "Disclosure %",
           "Is Disclosure 3 pct ?",
           "Is Disclosure 5 pct?",
           "Company Date",
           "Long / Short",
           "Business Unit",
           "Name of the Reporting Entity",
           "The Name of Securities Broker/Dealer",
           "Account Number of the Trading Account",
           "Type of Investment Account",
           "The Nature of Securities",
           "The Name of Securities",
           "Exchange Ticker Symbol of the Securities",
           "Name of Exchange on Which the Securities are, or to be, Listed",
           "ISIN Code of the Securities",
           "Name of the Underlying Securities",
           "Undrly Sec Syb",
           "Name of Exchange on Which the Underlying Securities is, or to be, Listed",
           "ISIN Code of the Underlying Securities",
           "Number of the Underlying Shares being/to-be held Remark",
           "Total Issued Shares of the Underlying Company/Corporation Remark",
           "Number of the Underlying Shares being/to-be held SUM",
           "Total Issued Shares of the Underlying Company/Corporation",
           "MSSE - Issused Shares",
           "Last Report Date",
           "Instrument Display Code",
           "Instrument Name",
           "Market Code",
           "Portfolio",
           "Portfolio Name",
           "Beneficial Eq"
           )


def convertStrToNumber(s):
    try:
        a = int(s)
        if isinstance(s, int):
            return int(s)
        elif isinstance(s, float):
            return float(s)
    except ValueError:
        return 0


def set_value(dataframe, row_index):
    row = DoiExcelData()
    row._criteria1 = str(dataframe.iloc[row_index][columns[0]])
    row._criteria2 = str(dataframe.iloc[row_index][columns[1]])
    row._criteria3 = str(dataframe.iloc[row_index][columns[2]])
    row._criteria = str(dataframe.iloc[row_index][columns[3]])
    row._total_issued_shares_underly_com_ht = dataframe.iloc[row_index][columns[4]]
    row._disclosure = dataframe.iloc[row_index][columns[5]]
    row._is_disclosure_3_pct = dataframe.iloc[row_index][columns[6]]
    row._is_disclosure_5_pct = dataframe.iloc[row_index][columns[7]]
    row._company_date = dataframe.iloc[row_index][columns[8]]
    row._long_short = dataframe.iloc[row_index][columns[9]]
    row._business_unit = dataframe.iloc[row_index][columns[10]]
    row._name_of_report_entity = dataframe.iloc[row_index][columns[11]]
    row._name_of_sec_broker_or_dealer = dataframe.iloc[row_index][columns[12]]
    row._account_num = dataframe.iloc[row_index][columns[13]]
    row._investment_acct_type = dataframe.iloc[row_index][columns[14]]
    row._nature_of_sec = dataframe.iloc[row_index][columns[15]]
    row._name_of_sec = dataframe.iloc[row_index][columns[16]]
    row._exchange_ticker_syb_sec = dataframe.iloc[row_index][columns[17]]
    row._name_of_exchange_sec = dataframe.iloc[row_index][columns[18]]
    row._isin_code_sec = dataframe.iloc[row_index][columns[19]]
    row._underly_sec_name = dataframe.iloc[row_index][columns[20]]
    row._underly_sec_syb = dataframe.iloc[row_index][columns[21]]
    row._name_of_exchange_underly_sec = dataframe.iloc[row_index][columns[22]]
    row._isin_code_underly_sec = dataframe.iloc[row_index][columns[23]]
    row._num_underly_sec_held_remark = dataframe.iloc[row_index][columns[24]]
    row._total_issued_shares_underly_com_remark = dataframe.iloc[row_index][columns[25]]
    row._num_underly_sec_held_sum = dataframe.iloc[row_index][columns[26]]
    row._total_issued_shares_underly_com = dataframe.iloc[row_index][columns[27]]
    row._msse_issued_shares = dataframe.iloc[row_index][columns[28]]
    row._last_report_date = dataframe.iloc[row_index][columns[29]]
    row._instrument_display_code = dataframe.iloc[row_index][columns[30]]
    row._instrument_name = dataframe.iloc[row_index][columns[31]]
    row._market_code = dataframe.iloc[row_index][columns[32]]
    row._portfolio = dataframe.iloc[row_index][columns[33]]
    row._portfolio_name = dataframe.iloc[row_index][columns[34]]
    row._beneficial_eq = dataframe.iloc[row_index][columns[35]]
    return row


def getFileNames(start_date_str, end_date_str):
    list = []
    holiday_list = ["20180101", "20180102", "20180216", "20180217", "20180218", "20180219", "20180220", "20180330", "20180331",
                    "20180401", "20180402", "20180403", "20180405", "20180406", "20180501", "20180502", "20180522", "20180523", "20180618", "20180619"]
    if type(start_date_str) is str and type(end_date_str) is str:
        try:
            temp = datetime.date.fromisoformat(start_date_str)
            end_date = datetime.date.fromisoformat(end_date_str)
            while temp <= end_date and temp.weekday is not 5 and temp.weekday is not 6 and (not temp.strftime(cal_format) in list):
                date_str = temp.strftime(iso_date_format)
                list.append(date_str)
                ++temp
        except Exception as e:
            print(e)
    return list


def create_pair(row):
    global trade_date_list
    hold = HoldInfo()
    key = row["Undrly Sec Syb"]
    hold._underly_sec_syb = row["Undrly Sec Syb"]
    hold._trade_date = row["Company Date"].strftime(iso_date_format)
    if row["Long / Short"].upper() == "LONG":
        hold._num_shares_hold_long = row["Number of the Underlying Shares being/to-be held SUM"]
    elif row["Long / Short"].upper() == "SHORT":
        hold._num_shares_hold_short = row["Number of the Underlying Shares being/to-be held SUM"]
    hold._total_issued_shares = row["MSSE - Issused Shares"]
    if hold._total_issued_shares == 0:
        hold._total_issued_shares = row["Total Issued Shares of the Underlying Company/Corporation"]
    holdDict = {}
    holdDict[hold._trade_date]=hold
    return (key, holdDict)


def reduce_key(v1, v2):
    global hold_dict
    holdDict = v1
    for trade_date in v2:
        if trade_date in holdDict:    
            holdDict[trade_date]._num_shares_hold_long = holdDict[trade_date]._num_shares_hold_long+v2[trade_date]._num_shares_hold_long
            holdDict[trade_date]._num_shares_hold_short = holdDict[trade_date]._num_shares_hold_short+v2[trade_date]._num_shares_hold_short
        else:
            holdDict[trade_date] = v2[trade_date]    
        if holdDict[trade_date]._total_issued_shares == 0 or holdDict[trade_date]._total_issued_shares < v2[trade_date]._total_issued_shares:
            holdDict[trade_date]._total_issued_shares = v2[trade_date]._total_issued_shares
    hold_dict = holdDict
    print("+++++++++++++++++++++++++++++++++++")
    print(list(holdDict.keys()))
    print("+++++++++++++++++++++++++++++++++++")
    return holdDict

def calPctLong(holdDict):
    pct_list=[]
    if holdDict is not None and len(holdDict)>0:
        for trade_date in holdDict:
            hold = holdDict[trade_date]
            if hold._total_issued_shares > 0:
                hold._pct_long = hold._num_shares_hold_long/hold._total_issued_shares*100
            else:
                hold._pct_long = 0    
            pct_list.append(str(hold._pct_long))
        pct_list.insert(0,hold._underly_sec_syb)
    return pct_list

def calPctShort(holdDict):
    pct_list=[]
    if holdDict is not None and len(holdDict)>0:
        for trade_date in holdDict:
            hold = holdDict[trade_date]
            if hold._total_issued_shares > 0:
                hold._pct_short = hold._num_shares_hold_short/hold._total_issued_shares*100
            else:
                hold._pct_short = 0
            pct_list.append(str(hold._pct_short))
        pct_list.insert(0,hold._underly_sec_syb)
    return pct_list

def consolidate_doi_file(df_doi):
    try:
        sparkDF = spark.createDataFrame(df_doi)
        pairRDD = sparkDF.rdd.map(create_pair)
        mergedRdd = pairRDD.reduceByKey(reduce_key)
        writeRecords(mergedRdd)
        # temp_df.coalesce(1).write.format("csv").save("file:///C:/kevin/test.csv")
        # for i in range(len(df_doi)):
        #     #print(datetime.date.today().strftime("%Y-%m-%d"))
        #     row = set_value(df_doi, i)
        #     print(row._underly_sec_syb)
    except Exception as e:
        print("Exception in consolidate_doi_file:==============>")
        print(e)


def writeRecords(rdd):
    global trade_date_list
    global hold_dict
    if rdd is None:
        return
    trade_date_list.insert(0,"underly_sec_syb")
    print("===============>")
    print(trade_date_list)
    print(hold_dict)

    tempList = rdd.values().map(calPctLong).collect()
    tempList2 = rdd.values().map(calPctShort).collect()

    temp_df = pd.DataFrame(tempList, columns=trade_date_list)
    temp_df.to_csv("C:/kevin/test_long.csv", index=False)

    temp_df2 = pd.DataFrame(tempList2, columns=trade_date_list)
    temp_df2.to_csv("C:/kevin/test_short.csv", index=False)

def parseColumns(fname):
    global combined_df
    use_cols = "I,J,V,AA,AB,AC"
    with pd.ExcelFile(fname) as xls:
        df_doi = pd.read_excel(xls, 0, index_col=None,
                               header=0, skiprows=2, usecols=use_cols)
        trade_date=df_doi.iloc[0][columns[8]].strftime(iso_date_format)
        trade_date_list.append(trade_date)
        df_doi[columns[21]] = df_doi[columns[21]].apply(lambda v: "'"+str(v))
        df_doi[columns[26]] = df_doi[columns[26]].apply(convertStrToNumber)
        df_doi[columns[27]] = df_doi[columns[27]].apply(convertStrToNumber)
        df_doi[columns[28]] = df_doi[columns[28]].apply(convertStrToNumber)
        df_doi[columns[21]].astype(str)
        df_doi[columns[26]].astype(int)
        df_doi[columns[27]].astype(int)
        df_doi[columns[28]].astype(int)
        if combined_df is None:
            combined_df = df_doi
        else:
            combined_df = combined_df.append(df_doi)

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("Test") \
        .getOrCreate()
    # conf = SparkConf().setMaster("local").setAppName("My App")
    # sc = SparkContext(conf = conf)
    # file_path = r"\\PC003428\Greyspark\Kevin\\Raw Data\\"
    # file_name = r"Company Disclosure of Interest - OPGM {0}.xls"
    # date_list = getFileNames("2018-02-12", "2018-05-31")
    # if date_list is not None and len(date_list) > 0:
    #     for date in date_list:
    #         file = file_path+file_name.replace(r"{0}", date)
    #         with pd.ExcelFile(file) as xls:
    #             df_doi = pd.read_excel(
    #                 xls, 0, index_col=None, header=0, skiprows=2)

    file_path = r"\\PC003428\Greyspark\Kevin\Raw Data"
    file_name_pattern = "Company Disclosure of Interest(\s*)-(\s*)OPGM(\s*)\d{8}.xls$"
    files = [f for f in os.listdir(file_path) if re.match(file_name_pattern, f)]
    print(files)
    try:
        for fname in files:
            parseColumns(os.path.join(file_path,fname))
        consolidate_doi_file(combined_df)
    except Exception as e:
        print("Exception in main:==============>")
        print(e)
