import pandas as pd
import datetime
from DoiExcelData import DoiExcelData

columns=("Criteria 1",
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

def set_value(dataframe, row_index):
    row = DoiExcelData()
    row._criteria1 = dataframe.iloc[row_index][columns[0]]
    row._criteria2 = dataframe.iloc[row_index][columns[1]]
    row._criteria3 = dataframe.iloc[row_index][columns[2]]
    row._criteria = dataframe.iloc[row_index][columns[3]]
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
    row._name_of_exchange_sec= dataframe.iloc[row_index][columns[18]]
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

if __name__=='__main__':
    with pd.ExcelFile(r'\\PC003428\Greyspark\Kevin\Raw Data\Company Disclosure of Interest - OPGM 20180620_TEST.xls') as xls:
        df_doi = pd.read_excel(xls, 0, index_col=None, header=0, skiprows=2)
    try:
        for i in range(len(df_doi)):
            #print(datetime.date.today().strftime("%Y-%m-%d"))
            row = set_value(df_doi, i)
            print(row._underly_sec_syb)
    except Exception as e:
        print(e)
