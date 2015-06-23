import json
import unicodedata
from collections import defaultdict

chars = json.load(open('unicode_normalization.json'))

resets = defaultdict(lambda: [])

resets['SS'].append({'char': u'\u00df', 'primary': True})

for x in chars:
    char = x['char']
    normalized = x['normalized']
    resets[normalized.upper()].append({'char': char, 'primary': True})

resets = dict(resets)

def val_key(val):
    return val['char']

for key, vals in resets.items():
    lower = dict()
    upper = dict()
    other = dict()

    for val in vals:
        c = val['char']
        l = c.lower()
        u = c.upper()

        if l == u:
            other[c] = val
        elif c == l:
            lower[c] = val
        else:
            upper[c] = val

    new_vals = []

    for val in sorted(upper.values(), key = val_key):
        c = val['char']
        l = c.lower()

        new_vals.append(val)

        if l in lower:
            lower_val = lower[l]
            del lower[l]
            lower_val['primary'] = False
            new_vals.append(lower_val)

    new_vals.extend(sorted(lower.values(), key = val_key))
    new_vals.extend(sorted(other.values(), key = val_key))

    resets[key] = new_vals

with open('collation.xml', 'w') as f:
    w = lambda x: f.write(x.encode('utf8') + '\n')

    w(u'  <collation name="utf8_distinct_ci" id="252">')
    w(u'    <rules>')

    for key, vals in sorted(resets.items()):
        r = key
        if not r.isalnum():
            r = '\\u%.4x' % ord(r)

        w(u'      <reset>%s</reset><!-- %s -->' % (r, key))

        for val in vals:
            escaped = '\\u%.4x' % ord(val['char'])
            tag = 'p' if val['primary'] else 't'
            w(u'      <%s>%s</%s><!-- %s -->' % (tag, escaped, tag, val['char']))

        w(u'')

    w(u'    </rules>')
    w(u'  </collation>')
