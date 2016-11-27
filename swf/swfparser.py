# -*- coding: utf-8 -*-
"""
Copyright (c) 2016 skyblue3350
See LICENSE for details.
"""

from swf.swfobject import SWFObject
from swf.swftag import SWFTag

import zlib
from StringIO import StringIO


class SWFParser(object):
    def __init__(self):
        pass

    def parse(self, fp):
        self.fp = fp
        header = self.readHeader()
        swfobj = SWFObject(**header)
        swfobj.tags = self.readTags()
        return swfobj

    def readHeader(self):
        result = {}
        result["signature"] = self.fp.read(3)
        result["version"] = ord(self.fp.read(1))
        size = self.readLittleEndian(self.fp.read(4))
        result["size"] = int("".join(size), 16)

        if result["signature"] == "CWS":
            self.fp = StringIO(zlib.decompress(self.fp.read()))

        _ = self.readBits(self.fp.read(1))
        nbits = int(_[0][:5], 2)
        rect = _ + self.readBits(self.fp.read((nbits * 4 + 5) / 8))
        rect = "".join(rect)[5:]
        rects = [rect[i: i + nbits] for i in range(0, len(rect), nbits)]

        result["rect"] = {}
        for i, v in enumerate(["xmin", "xmax", "ymin", "ymax"]):
            result["rect"][v] = int(rects[i], 2) / 20

        rate = self.readLittleEndian(self.fp.read(2))
        result["framerate"] = float("{}.{}".format(*[int(x, 16) for x in rate]))
        count = self.readLittleEndian(self.fp.read(2))
        result["framecount"] = int("".join(count), 16)

        return result

    def readTags(self):
        result = []
        while True:
            info = "".join(self.readBits(self.fp.read(2))[::-1])
            tagtype = int(info[:10], 2)
            taglength = int(info[-6:], 2)

            if taglength == 63:
                l = int("".join(self.readLittleEndian(self.fp.read(4))), 16)
                data = self.fp.read(l)
            else:
                data = self.fp.read(taglength)

            tag = SWFTag(tagtype, data)
            result.append(tag)

            if tagtype == 0:
                break

        return result

    @classmethod
    def readLittleEndian(self, bytes):
        return [hex(ord(x))[2:].zfill(2) for x in bytes][::-1]

    @classmethod
    def readBits(self, bytes):
        return [bin(ord(x))[2:].zfill(8) for x in bytes]

    @classmethod
    def readInteger(self, bytes):
        return [ord(x) for x in bytes]
