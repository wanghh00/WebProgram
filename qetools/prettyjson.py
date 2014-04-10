#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput
import json
import re

jsonSearcher=re.compile('({.+})')

def prettyJson(dct):
    return json.dumps(dct, sort_keys=True, indent=4, separators=(',', ': '))

for line in fileinput.input():
    print prettyJson(json.loads(jsonSearcher.search(line).group(1)))
