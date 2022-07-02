import requests
import csv
import os
from os import walk

API_ID = "7e1c00d8eb5ab5c54f6729f8b80a502e"
API_PWD = "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"
SHOP_NAME = "dermaskinshop.myshopify.com"

directory = os.getcwd()
filenames = next(walk(directory), (None, None, []))[2]
orderDir = []


def selectionList():
    selectionDir = 0
    for dir in filenames:
        if '.csv' in dir:
            selectionDir += 1
            print(selectionDir, dir.replace(".csv", ""))
            orderDir.append(dir.replace(".csv", ""))


print('Enter Shopify CSV: ')
selectionList()
shopifyCSV = input()
print("You selected: ", orderDir[int(shopifyCSV)-1])
print('\nEnter BillPlz CSV: ')
selectionList()
billPlzCSV = input()
print("You selected: ", orderDir[int(billPlzCSV)-1])
print('\nEnter Final Export CSV: ')
finalExportCSV = input()

ordersShopify = orderDir[int(shopifyCSV)-1] + ".csv"
# Original Billplz CSV
billPlzAccount = orderDir[int(billPlzCSV)-1] + ".csv"

ordersShopifyData = {}
billPlzData = {}

with open(ordersShopify, encoding="utf-8") as ordersFile:
    csvReader = csv.DictReader(ordersFile)
    for count, rows in enumerate(csvReader):
        ordersShopifyData[count] = rows

with open(billPlzAccount, encoding="utf-8") as billPlzFile:
    csvReader = csv.DictReader(billPlzFile)
    for count, rows in enumerate(csvReader):
        billPlzData[count] = rows

with open(finalExportCSV + '.csv', 'w', encoding="utf-8", newline='') as orderTrans_file:
    fieldnames = ['Order Id', 'Order Name', 'CURRENCY', 'COLLECTION ID', 'BILL ID', 'COLLECTION TITLE', 'BILL DESCRIPTION', 'NAME', 'EMAIL', 'MOBILE NUMBER', 'REFERENCE 1',
                  'REFERENCE 2', 'DUE DATE', 'PROCESSOR', 'PAYMENT METHOD', 'TRANSACTION ID', 'TRANSACTION DATE', 'PAYMENT RECEIVED', 'FIXED SPLIT FOR PAYOUT', '% SPLIT FOR PAYOUT', 'PAYOUT']
    writer = csv.DictWriter(orderTrans_file, fieldnames=fieldnames)
    writer.writeheader()
    getBillPlzRefId = []
    a = 0
    for a in range(len(ordersShopifyData)):
        orderUrl = requests.get("https://"+API_ID+":"+API_PWD+"@"+SHOP_NAME +
                                "/admin/api/2021-07/orders/"+ordersShopifyData[a]['Order']+".json")
        orderTransUrl = requests.get("https://"+API_ID+":"+API_PWD+"@"+SHOP_NAME +
                                     "/admin/api/2021-07/orders/"+ordersShopifyData[a]['Order']+"/transactions.json")

        try:
            getOrderData = orderUrl.json()
            getOrderTransData = orderTransUrl.json()
            getGateway = getOrderTransData['transactions'][0]['gateway'].lower(
            )
            if(getGateway == 'billplz'):
                getRefBillPlz = getOrderTransData['transactions'][0]['receipt']['payment_id']
                for b in range(len(billPlzData)):
                    if(getRefBillPlz.lower() == billPlzData[b]['REFERENCE 1'].lower()):

                        print(getRefBillPlz.lower())
            a += 1
            print(a)
            if(a >= 80):

                break

        except:
            pass
print("Export Successfully")
