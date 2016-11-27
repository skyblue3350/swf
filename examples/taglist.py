# coding: utf-8

import swf

fp = open("examples/test.swf", "rb")
obj = swf.load(fp)

images = [x for x in obj.tags if x.isImage()]

for i, tag in enumerate(images):
        tag.save("out/" + str(i))
