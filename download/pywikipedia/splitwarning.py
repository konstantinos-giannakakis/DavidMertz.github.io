# -*- coding: utf-8  -*-
"""Splits a interwiki.log file into chunks of warnings separated by language"""
#
# (C) Rob W.W. Hooft, 2003
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id: splitwarning.py,v 1.12 2005/12/21 17:51:26 wikipedian Exp $'
#

import wikipedia
import codecs
import re

wikipedia.stopme() # No need to have me on the stack - I don't contact the wiki
files={}
count={}

# TODO: Variable log filename
logFile = codecs.open('logs/interwiki.log', 'r', 'utf-8')
rWarning = re.compile('WARNING: (?P<family>.+?): \[\[(?P<code>.+?):.*')
for line in logFile:
    m = rWarning.match(line)
    if m:
        family = m.group('family')
        code = m.group('code')
        if code in wikipedia.getSite().languages():
            if not files.has_key(code):
                files[code] = codecs.open('logs/warning-%s-%s.log' % (family, code), 'w', 'utf-8')
                count[code] = 0
            files[code].write(line)
            count[code] += 1
for code in files.keys():
    print '*%s (%d)' % (code, count[code])
