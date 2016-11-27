# -*- coding: utf-8 -*-
"""
Copyright (c) 2016 skyblue3350
Released under the MIT license
See LICENSE for details.
"""

from swf.swfparser import SWFParser


def load(fp):
    parser = SWFParser()
    return parser.parse(fp)
