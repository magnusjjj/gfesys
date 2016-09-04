#!/usr/bin/python

# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:

# This is a bleeding test

import sys
import random
import string
import os

#this... seems to work, which it didnt before. DARK MAGIC AND CTHUHLU.
#todo: make it work on anything else than windows :P
del os.environ["PYTHONUNBUFFERED"]
os.system('start cmd /K ')# + os.environ['VIRTUAL_ENV'] + '\scripts\activate.bat')