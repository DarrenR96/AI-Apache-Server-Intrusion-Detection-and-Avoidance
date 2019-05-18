from sklearn.externals import joblib
import numpy as np
import pandas as pd


def encodeLabels(df):
    df = df.drop(columns="RefererGeneral")

    countryEncoder = joblib.load('./MLModel/countryEncoder')
    requestFileTypeEncoder = joblib.load('./MLModel/requestFileTypeEncoder')
    requestTypeEncoder = joblib.load('./MLModel/requestTypeEncoder')

    countryEncoder = dict(zip(countryEncoder.classes_,
                              countryEncoder.transform(countryEncoder.classes_)))
    requestFileTypeEncoder = dict(zip(requestFileTypeEncoder.classes_,
                                      requestFileTypeEncoder.transform(requestFileTypeEncoder.classes_)))
    requestTypeEncoder = dict(zip(requestTypeEncoder.classes_,
                                  requestTypeEncoder.transform(requestTypeEncoder.classes_)))

    for index, row in df.iterrows():
        try:
            if (requestTypeEncoder.get(
                    df.at[index, 'RequestType']) == None):
                df.at[index, 'RequestType'] = 'None'
                df.at[index, 'RequestType'] = requestTypeEncoder.get(
                    df.at[index, 'RequestType'])
            else:
                df.at[index, 'RequestType'] = requestTypeEncoder.get(
                    df.at[index, 'RequestType'])
        except:
            print("Encoding Error")

        try:
            if (countryEncoder.get(
                    df.at[index, 'Country']) == None):
                df.at[index, 'Country'] = 'None'
                df.at[index, 'Country'] = countryEncoder.get(
                    df.at[index, 'Country'])
            else:
                df.at[index, 'Country'] = countryEncoder.get(
                    df.at[index, 'Country'])
        except:
            print("Encoding Error")

        try:
            if (requestFileTypeEncoder.get(
                    df.at[index, 'RequestFileType']) == None):
                df.at[index, 'RequestFileType'] = 'None'
                df.at[index, 'RequestFileType'] = requestFileTypeEncoder.get(
                    df.at[index, 'RequestFileType'])
            else:
                df.at[index, 'RequestFileType'] = requestFileTypeEncoder.get(
                    df.at[index, 'RequestFileType'])
        except:
            print("Encoding Error")

    return(df)


def classification(df):
    clf = joblib.load('./MLModel/apacheDecisionTree')
    dataFeatures = np.array(df.drop(['Ip'], axis=1), dtype=str)
    df["Prediction"] = ""
    try:
        df['Prediction'] = clf.predict(dataFeatures)
    except:
        print('Classification Error')
    return(df)


def apacheMLProcess(df):
    df = encodeLabels(df)
    predDF = classification(df)
    predDF = predDF[['Ip', 'Prediction']]
    predDF['Prediction'] = predDF['Prediction'].astype(int)

    predDF = predDF.groupby(['Ip'], as_index=False).mean()

    return (predDF)
