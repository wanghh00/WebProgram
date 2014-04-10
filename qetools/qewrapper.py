#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import logging; LOG = logging.getLogger(__name__)

from utils import comm

from qeutils.tools import CmdChkUrlStatus

    
if __name__ == '__main__':
    logging.basicConfig(format=comm.LOGFMT,datefmt=comm.LOGDATEFMT)
    logging.getLogger().setLevel(logging.ERROR)

    func_name = sys.argv[1]

    func = eval('%s(sys.argv[2:])' % func_name)
    ret = func()
    print json.dumps(ret)
            