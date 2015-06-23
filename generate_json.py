# pip install pymysql

import json
import unicodedata
import pymysql.cursors

connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

sql = u"SELECT %s = %s COLLATE utf8_unicode_ci AS `x`"

chars = []

for i in range(0x00A0, 0x10000):
    char = ('\u%.4x' % i).decode('unicode-escape')

    for j in range(0x0020, 0x007F):
        normalized = ('\u%.4x' % j).decode('unicode-escape')

        cursor.execute(sql, (char, normalized,))

        if cursor.fetchone()['x']:
            chars.append({'char': char, 'normalized': normalized})
            print u'%s (\\u%.4x) == %s (\\u%.4x) %s' % (char, i, normalized, j, unicodedata.category(char))
            break

with open('unicode_normalization.json', 'w') as f:
    json.dump(chars, f, sort_keys=True, indent=4, separators=(',', ': '))
