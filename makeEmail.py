import xlrd
from xlrd import open_workbook

csv_file_path = '/home/sammy/Desktop/SUTech/StudentUnionPortal/bill/passport.xlsx'


data_reader = open_workbook(csv_file_path).sheet_by_index(1)
for row_index in xrange(1, data_reader.nrows):
    x = data_reader.cell(row_index, 2).value
    temp = x[:4]
    degree = x[4:5].lower()
    if degree != 'h' and degree != 'p':
        degree = 'f'

    if temp == '2017':
        temp = degree + '2017' + x[-5:-1] + '@pilani.bits-pilani.ac.in'

    else:
        temp = degree + temp + x[-4:-1] + '@pilani.bits-pilani.ac.in'

    strx=""
    strx = strx + "," + temp
    print temp + ","
