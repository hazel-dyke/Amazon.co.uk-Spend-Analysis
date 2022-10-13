#   Python3 program to analyse spending on your personal Amazon.co.uk account
#   Your order data first needs to be scraped from Amazon.co.uk using an open source chrome extension.
#   Chrome extension is called: "Amazon Order History Reporter", August 2022 version was used with this python script.
#   Chrome webstore url: https://chrome.google.com/webstore/detail/amazon-order-history-repo/mgkilgclilajckgnedgjgnfdokkgnibi
#   Github url: https://github.com/philipmulcahy/azad
#   This chrome extension allows you to download a csv for each year you are interested in.
#   Place all csv's in the same folder for this script to work.

import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate data file paths.
csv_paths = []
path = r"C:\Users\Hazel Sindall\Documents\Amazon Order History data"
extension = 'csv'
os.chdir(path)
result = glob.glob('*.{}'.format(extension))
print(result)

for extension in result:
    full_path = os.path.join(path, extension)
    csv_paths.append(full_path)


#  Data frame population and manipulation.
df = pd.concat(map(pd.read_csv, csv_paths), ignore_index=True)
df = df[["date", "total"]]      #   Retain only order-date and total-order-cost columns
total_orders = len(df)
df = df[["date", "total"]]      #   Only keep the purchase date and purchase cost columns
df = df.dropna()                #   drop any purchase records with incomplete cost and date information
complete_orders = len(df)
df = df.reset_index()           #   re-set the indexing of the dataframe
df["date"] = pd.to_datetime(df["date"])
df["total"] = pd.to_numeric(df["total"])

#   Populate a dictionary with year and total spend.
dict_ = {}
value = 0
for i in range(len(df)):
    if df.at[i,"date"].year not in dict_.keys():
        dict_[df.at[i, "date"].year] = df.at[i, "total"]
    else:
        dict_[df.at[i,"date"].year] += df.at[i,"total"]

#   Plot a bar chart and print some summary information
print("Number of orders imported = ", total_orders)
print("Number of complete orders = ", complete_orders)
print("Number of orders with missing date or cost info = ", (total_orders-complete_orders))
print("The first purchase was on : ", min(df["date"]).date())
print("The last purchase was on : ", max(df["date"]).date())
total_spend = sum(df["total"])
print("The total expenditure on Amazon.co.uk between ", min(df["date"]).date(), " and ", max(df["date"]).date(), " was ", f"£{int(total_spend):,}"+"!", "\n")
plt.bar(*zip(*dict_.items()))
plt.title('Spending on Amazon.co.uk by year since signing up')
plt.xlabel("Year")
plt.ylabel("Spend [£]")
plt.show()
