# SWFParser
勉強ついでに書いてみたSWFパーサ
一部フォーマットだけ画像書き出し実装済み

# サンプル
## 画像書き出し
```
# coding: utf-8

import swf

fp = open("examples/test.swf", "rb")
obj = swf.load(fp)

images = [x for x in obj.tags if x.isImage()]

for i, tag in enumerate(images):
        tag.save("examples/out/" + str(i))
```

## tag名一覧
```
# coding: utf-8

import swf

fp = open("examples/test.swf", "rb")
obj = swf.load(fp)

for tag in obj.tags:
    print tag.tagname
```
