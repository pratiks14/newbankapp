import sys

def getTranxid(fromaccount,toaccount,date):
    return hex(int(fromaccount))[2:]+hex(int(toaccount))[:2]+hex(date.replace(':',' ').replace(' ',''))[:2]
