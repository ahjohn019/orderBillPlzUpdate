# importing the pandas library
import pandas as pd
import requests

# reading the billplz csv file
bp = pd.read_csv("AS-20220620-20220627-204719.csv")

# reading the shopify csv file
sp = pd.read_csv("transactions_export_1.csv")

# get shopify init database
API_ID = ""
API_PWD = ""
SHOP_NAME = ""

# append billplz ref one into array
getRefBillPlz = []
getTransIdBillPlz = []
for b in range(len(bp)):
    getRefBillPlz.append(bp['REFERENCE 1'][b].lower())
    getTransIdBillPlz.append(bp['TRANSACTION ID'][b].lower())

# get the billplz related result
try:
    for a in range(len(sp)):
        orderNumber = str(sp['Order'][a+1])
        orderUrl = requests.get("https://"+API_ID+":"+API_PWD+"@"+SHOP_NAME +
                                "/admin/api/2021-07/orders/" + orderNumber + ".json")
        orderTransUrl = requests.get("https://"+API_ID+":"+API_PWD+"@"+SHOP_NAME +
                                     "/admin/api/2021-07/orders/" + orderNumber + "/transactions.json")

        orderJson = orderUrl.json()
        transJson = orderTransUrl.json()
        transaction = transJson['transactions'][0]
        gateway = transaction['gateway'].lower()
        getSpecValue = ""

        if(gateway == 'billplz'):
            if('payment_id' in transaction['receipt']):
                getRefApi = transaction['receipt']['payment_id'].lower()
                if getRefApi in getRefBillPlz:
                    getSpecValue = bp.index[bp['REFERENCE 1'].str.lower(
                    ) == getRefApi]

            if('x_gateway_reference' in transaction['receipt']):
                getTransApi = transaction['receipt']['x_gateway_reference'].lower(
                )
                if getTransApi in getTransIdBillPlz:
                    getSpecValue = bp.index[bp['TRANSACTION ID'].str.lower(
                    ) == getTransApi]

            if(len(getSpecValue) > 0):
                bp.loc[getSpecValue[0], 'ORDER ID'] = orderNumber
                bp.loc[getSpecValue[0],
                       'ORDER NUM'] = "#" + str(orderJson['order']['order_number'])
                bp.to_csv("AS-20220620-20220627-204719.csv", index=False)
                print(bp)
except:
    pass
