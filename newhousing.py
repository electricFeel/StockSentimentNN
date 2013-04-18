import csv

#builds the New Privately-Owned Housing units

dates = []
newHousing = {'01': 87.6, '02': 80.60, '03': 87.6, '04': 80.0,
           '05': 85.8, '06': 84.7, '07': 87.5, '08': 94.5,
           '09': 93.30, '10': 89.90, '11': 90.1,
           '12': 92.5}


if __name__ == "__main__":
    for line in open('SNP5002012Close.txt'):
        row = line.rstrip().split(',')
        print row
        date = row[0]
        if date.split('/')[2] == '2012':
            dates.append([row[0], newHousing[date.split('/')[0]]])

    w2012 = open('NewHousing2012.txt', 'wb')
    wr = csv.writer(w2012, quoting=csv.QUOTE_NONE)
    wr.writerows(dates)
