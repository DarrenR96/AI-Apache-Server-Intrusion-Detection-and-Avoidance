import pandas as pd
import pythonApacheLibrary.apacheLogs as apl
import pythonApacheLibrary.apacheML as aml
import pythonApacheLibrary.blacklistHandler as blh
accessLogPath = ''
ipBlackListCsv = ""
ipDBkey = ""
ipBlackListConf = ""

# Read in access_log file & Parse File to return relevant columns
accessLog = apl.accessLogInit(accessLogPath).head(10)

# Compare list of Ips to current blacklisted DB
ipList = pd.read_csv(ipBlackListCsv)

# Drop Rows where there is overlap
accessLog = accessLog[~accessLog['Ip'].isin(ipList["IPBlack"])]


# Perform IP Lookup funciton
accessLog = apl.reverseIpLookup(accessLog, ipDBkey)


# Perform Label Encoding
# Run each new row through decision tree
predictedDF = aml.apacheMLProcess(accessLog)
predictedDF = predictedDF[predictedDF['Prediction'] == 3]

# If flagged as bad, append IPs to blacklist in APACHE
blh.blacklistAppender(predictedDF, ipBlackListConf, ipBlackListCsv)
