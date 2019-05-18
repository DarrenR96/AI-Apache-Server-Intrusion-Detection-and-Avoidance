import pandas as pd


def blacklistAppender(df, confpath, csvpath):
    fileLoc = confpath
    f = open(fileLoc, "r")
    contents = f.readlines()
    f.close()

    f = open(fileLoc, "w")
    for index, row in df.iterrows():
        contents.insert(-2, "deny from "+str(row["Ip"])+"\n")
    contents = "".join(contents)
    f.write(contents)
    f.close()
    ipListCsv = pd.read_csv(csvpath)
    ipListCsv["IPBlack"] = pd.concat(
        [ipListCsv["IPBlack"], df["Ip"]], ignore_index=True)
    ipListCsv.to_csv(csvpath, index=False)
