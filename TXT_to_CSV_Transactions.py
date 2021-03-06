# TEXT TO CSV CONVERSION/PREP AUTOMATION
#
# DIRECTIONS:
# -- Input month digit, day digit, and year that is appended on report name.
# -- Input current location of report.
# -- Input desired location of CSV extract.

MonthDigit = 1
DayDigit = 1
Year = 2020
CurrentReportLocation = 'C:\\Users\\jacobhauter\\Desktop'
DesiredReportLocation = 'C:\\Users\\jacobhauter\\Desktop'

import pandas as pd
import numpy as np

col_breaks = [
    (0,19),
    (20,23),
    (24,35),
    (36,71),
    (72,83)
]

col_names = [
    "Card_Number",
    "Remove_1",
    "Transaction_Date",
    "Remove_2",
    "Transaction_Net_Amount"
]

col_types = {
    "Card_Number": np.object,
    "Remove_1": np.object,
    "Transaction_Date": np.object,
    "Remove_2": np.object,
    "Transaction_Net_Amount": np.object
}

df = pd.read_fwf(
    str(CurrentReportLocation) + "\\Terminal Transaction Detail Report - "
    + str(MonthDigit) + "-" + str(DayDigit) + "-" + str(Year) + ".txt",
    colspecs = col_breaks,
    names = col_names,
    dtype = col_types
)

df = df.dropna(how='all')
df = df[df.Remove_1 != '---']
df = df.dropna(axis=0, subset=['Transaction_Date'])
df = df.dropna(axis=0, subset=['Transaction_Net_Amount'])
df = df.dropna(axis=0, subset=['Remove_1'])
df = df[~df.Card_Number.str.contains("\*")]
df = df.drop(['Remove_1', 'Remove_2'], axis=1)

df['Terminal_ID'] = np.where(df.Card_Number.str[:9] == '0TERMINAL',df.Card_Number,'')

df.Terminal_ID[df['Terminal_ID']==""] = np.NaN
df.Terminal_ID = df.Terminal_ID.fillna(method='ffill')

df = df[df['Card_Number'] != df['Terminal_ID']]
df.Terminal_ID = str("'") + df.Terminal_ID.str[-8:] + str("'")
df.Card_Number = str("'") + df.Card_Number + str("'")
df = df.replace(',','',regex=True)

df = df.rename(columns={'Card_Number': 'Card Number',
                   'Transaction_Date': 'Transaction Date',
                   'Transaction_Net_Amount': 'Transaction Net Amount',
                   'Terminal_ID': 'Terminal ID'
                   })

df = df[['Transaction Date',
         'Card Number',
         'Terminal ID',
         'Transaction Net Amount']]

df.to_csv(
    str(DesiredReportLocation) +
    '\\Terminal Transactions ' +
    str(Year) + '-' + str(MonthDigit) + "-" + str(DayDigit) +
    '.csv', index=None)
