import pandas as pd
import re
import time
import requests


def dataframeLog(logfile):
    file = open(logfile, 'r')
    dataList = []
    columnList = ["Ip", "Request Line", "Status", "Referer"]
    for line in file:
        try:
            matches = None
            pattern = re.compile(
                r'([A-Za-z0-9\.-_]+)\s(?:-|.+)\s(?:-|.+)\s(?:\[.+\])\s\"(.+)\"\s(-|\d+)\s(?:-|\d+)\s\"(-|.*)\"\s\"(?:-|.*)\"')
            matches = tuple(pattern.findall(line))[0]
            dataList.append(matches)
        except:
            print(line)
    df = pd.DataFrame(dataList, columns=columnList)
    return(df)


def requestSplitter(logfile, typeOfData):
    df = None
    if (typeOfData == 'CSV'):
        df = pd.read_csv(logfile)
    elif(typeOfData == 'dataframe'):
        df = logfile
    df["RequestType"] = None
    df["RequestLink"] = None
    pattern = re.compile(
        r'([A-Z]+|-)\s*\**\s*(.*)\s*')
    for index, row in df.iterrows():
        try:
            combinedResult = tuple(pattern.findall(row["Request Line"]))[0]
            df.at[index, "RequestType"] = combinedResult[0]
            df.at[index, "RequestLink"] = combinedResult[1]
        except:
            df.at[index, "RequestType"] = "Unk"
            df.at[index, "RequestLink"] = row["Request Line"]

    df = df[['Ip', 'RequestType', 'RequestLink', 'Status',
             'Referer']]
    return(df)


def requestLineFileSplit(df):
    df["RequestFileType"] = ""
    pattern = re.compile(
        r'\.(\w{2,3}|(?:[/?{}]+(\/)\s))')
    for index, row in df.iterrows():
        try:
            combinedResult = tuple(pattern.findall(row["RequestLink"]))[0]
            df.at[index, "RequestFileType"] = combinedResult[0]
        except:
            df.at[index, "RequestFileType"] = "Unk"

    df = df[['Ip', 'RequestType', 'RequestFileType', 'Status',
             'Referer']]
    return(df)


def refererPreprocess(df):
    df["RefererGeneral"] = ""
    pattern = re.compile(
        r'(\w*\.\w*)')
    for index, row in df.iterrows():
        try:
            combinedResult = tuple(pattern.findall(row["Referer"]))[0]
            df.at[index, "RefererGeneral"] = combinedResult
        except:
            df.at[index, "RefererGeneral"] = "Unk"

    df = df[['Ip', 'RequestType', 'RequestFileType', 'Status',
             'RefererGeneral']]
    return(df)


def returnCountryCode(apiKey, ipAddr):
    try:
        data = requests.get(
            "http://api.ipinfodb.com/v3/ip-country/?key="+apiKey+"&ip="+ipAddr+"&format=json").json()
        if (data['statusCode'] == "OK"):
            return(data['countryCode'])
        else:
            return("None")
    except:
        return("None")


def reverseIpLookup(df, key):
    ipDict = {}
    df["Country"] = ''
    for index, row in df.iterrows():
        if row["Ip"] in ipDict:
            row["Country"] = ipDict[row["Ip"]]
        else:
            print(str(row["Ip"]))
            time.sleep(0.65)  # Comment if Paid key is given
            countryCode = returnCountryCode(
                key, row["Ip"])
            ipDict[row["Ip"]] = countryCode
            row["Country"] = countryCode
    return(df)


def accessLogInit(logfile):
    dataFrame = dataframeLog(logfile)
    dataFrame = requestSplitter(dataFrame, 'dataframe')
    dataFrame = requestLineFileSplit(dataFrame)
    dataFrame = refererPreprocess(dataFrame)
    dataFrame = dataFrame.replace(r'\s+', '-', regex=True).replace('', '-')
    return(dataFrame)
