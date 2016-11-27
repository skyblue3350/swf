# -*- coding: utf-8 -*-
"""
Copyright (c) 2016 skyblue3350
See LICENSE for details.
"""


class SWFObject(object):
    def __init__(self, signature, version, size, rect, framerate, framecount):
        self.signature = signature
        self.version = version
        self.size = size
        self.rect = rect
        self.framerate = framerate
        self.framecount = framecount
        self.tags = []
