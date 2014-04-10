#!/usr/bin/env python
# -*- coding: utf-8  -*-

import os

LstEnvVars = ['ENV', 'HTML_REPORT_VERSIONING', 'JOBNAME']

fd = open('.save_env_vars', 'w')

for k,v in os.environ.iteritems():
    if k not in LstEnvVars: continue
    fd.write('export %s=%s\n' % (k,v))
