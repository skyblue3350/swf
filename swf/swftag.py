# -*- coding: utf-8 -*-
"""
Copyright (c) 2016 skyblue3350
See LICENSE for details.
"""

import zlib
import numpy
from PIL import Image
from StringIO import StringIO

from swf.taglist import TagList


class SWFTag(object):
    def __init__(self, tagtype, raw):
        self.tagtype = tagtype
        self.tagname = TagList(tagtype)
        self.raw = raw

    def isImage(self):
        return self.tagtype in [6, 20, 21, 35, 36, 90]

    def save(self, path):
        resources = StringIO(self.raw)

        if self.tagtype in [6, 21, 35, 90]:
            ext = ".png"
            while True:
                flag = resources.read(2)
                if ["0xff", "0xd8"] == map(hex, map(ord, flag)):
                    resources.seek(resources.tell() - 2)
                    out = open(path + ext, "wb")
                    out.write(resources.read())
                    out.close()
                    break
                resources.seek(resources.tell() - 1)

        elif self.tagtype in [20, 36]:
            from swf.swfparser import SWFParser
            cid = SWFParser.readLittleEndian(resources.read(2))
            cid = int("".join(cid), 16)

            imageformat = ord(resources.read(1))
            width = SWFParser.readLittleEndian(resources.read(2))
            width = int("".join(width), 16)
            height = SWFParser.readLittleEndian(resources.read(2))
            height = int("".join(height), 16)

            imagearray = []

            if self.tagtype == 20:
                tablesize = ord(resources.read(1)) + 1
                bitmap = StringIO(zlib.decompress(resources.read()))
                colortable = [
                    [ord(bitmap.read(1)) for x in range(3)]
                    for i in range(tablesize)]

                w_dummy = 4 - (width % 4)
                for i in range(height):
                    data = SWFParser.readInteger(bitmap.read(width))
                    imagearray.append([colortable[x] for x in data])
                    bitmap.read(w_dummy)

            elif self.tagtype == 36:
                bitmap = StringIO(zlib.decompress(resources.read()))
                for i in range(height):
                    _ = []
                    for j in range(width):
                        rgba = SWFParser.readInteger(bitmap.read(4))
                        rgba.append(rgba.pop(0))
                        _.append(rgba)
                    imagearray.append(_)

            if not len(imagearray) == 0:
                a = numpy.asarray(imagearray, numpy.uint8)
                Image.fromarray(a).convert("RGBA").save(path + ".png")
