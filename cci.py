import csv

#builds the CCI (The Conference Board)

dates = []
CPI2012 = {'01': 61.5, '02': 71.60, '03': 69.50, '04': 68.70,
           '05': 64.40, '06': 62.70, '07': 65.40, '08': 61.30,
           '09': 70.30, '10': 73.10, '11': 71.50,
           '12': 64.60}


if __name__ == "__main__":
    for line in open('SNP5002012Close.txt'):
        row = line.rstrip().split(',')
        date = row[0]
        if date.split('/')[2] == '2012':
            dates.append([row[0], CPI2012[date.split('/')[0]]])

    w2012 = open('CCI2012.txt', 'wb')
    wr = csv.writer(w2012, quoting=csv.QUOTE_NONE)
    wr.writerows(dates)
