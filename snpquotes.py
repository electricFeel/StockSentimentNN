import urllib
import csv
import time


def get_historical_prices(symbol, start_date, end_date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'

    Returns a nested list.
    """
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(end_date[4:6]) - 1) + \
          'e=%s&' % str(int(end_date[6:8])) + \
          'f=%s&' % str(int(end_date[0:4])) + \
          'g=d&' + \
          'a=%s&' % str(int(start_date[4:6]) - 1) + \
          'b=%s&' % str(int(start_date[6:8])) + \
          'c=%s&' % str(int(start_date[0:4])) + \
          'ignore=.csv'
    days = urllib.urlopen(url).readlines()
    data = [day[:-2].split(',') for day in days]
    
    for i in range(1, len(data)):
        conv = time.strptime(data[i][0], "%Y-%m-%d")
        data[i][0] = time.strftime("%m/%d/%Y", conv)
    print data[0]

    data.reverse()
    change = []

    #compute the daily close change
    for i in range(0, len(data)-1):
        o = 1
        if round(float(data[i][1])-float(data[i][4]), 4) < 0:
            o = 0
        change.append([data[i][0], o])

    return data, change

if __name__ == "__main__":
    #write the SNP numbers
    w2012 = open('SNP5002012.txt', 'w')
    quotes2012, close2012 = get_historical_prices('^GSPC',
                                                  '20120525',
                                                  '20121231')
    wr = csv.writer(w2012, quoting=csv.QUOTE_NONE)
    wr.writerows(quotes2012)
    #write the daily output
    c2012 = open('SNP5002012Close.txt', 'w')
    wr = csv.writer(c2012, quoting=csv.QUOTE_NONE)
    wr.writerows(close2012)

