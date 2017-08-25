# PDF-crop

Split pages of pdf files down the middle, useful for scanning work. For more information, please see [the project website](https://blog.baoyukun.win/%E6%8A%80%E6%9C%AF/%E5%B7%A5%E5%85%B7/crop-pdf/).

基于PyPDF2，一个沿中缝批量裁剪PDF的小工具，一页变两页，方便双页快速扫描的后期处理。

## 应用场景

我们经常会扫描书籍到电子设备中，但一页页地扫描不仅效率太低，而且书籍装订中缝旁扫描效果欠佳，尤其是厚书。一个很自然的想法是，将书籍摊开，而后用机器上盖压实，一次扫描两页，最后再将扫描出的PDF沿中缝裁剪开来，一页变两页。

比如拿A4大小的书籍来说，就是按A3大小扫描进电脑，而后将A3的长边从中切开。

首先当然想到PDF的处理神器：**Adobe Acrobat X Pro**。如果去`Tools`-->`Pages`-->`Crop`看一看，或者在页面预览中选中一页单击右键、点击`Crop Pages`，通过设置margin的值将所有Page裁去一半是很容易做到的。然而问题是： **原页面的另一半将丢失！** 倘若将原件复制一份，对原件进行左切割，而对副本进行右切割，最后将两者merge也是可以的，然而新的问题来了： **如何把两份PDF交叉merge，即A-1P, B-1P, A-2P, B-2P...？** 正是因为没有找到第二个问题的解决办法，不得不寻求其他解决方案。

然后想到，PDF、图片和音视频文件的在线解决方案很多，果然找到了一个：[**Sejda**](https://www.sejda.com/)。在它的[`Split PDF pages down the middle`](https://www.sejda.com/split-pdf-down-the-middle)服务中，我们可以达成目的。然而这个工具有两个缺点：

1. 次数限制：免费版每天只可以裁剪3次
2. 中缝内容缺失：由于扫描摆放或者文字本身太靠近中缝等原因，严格由中间切开会导致 **_文字断裂_**

第一个缺点还可以勉强接受（*我们可以将要裁剪的文件合并到一起集中处理*），第二个缺点是致命的，无论对于阅读，还是对于再打印。因此我们希望： **切割得到左页面时，切割线比中线稍微向右去一点；反之同理。**

之后，我按照`Crop pdf pages`、`Split pdf down the middle`等关键字在Google上搜索，都没能得到简洁满意的答案。在GitHub上，也有不少项目关注到了这一需求，然而没找到可以直接使用的产品，大多给出了编程的代码块。

于是，我最终决定：自己动手写一个，一劳永逸！

>值得注意的是，很多有 *split* 字眼的解决方案，都是在分割页与页，即将一个PDF文档分成几个PDF文档。而我们需要的是分割一页得到两页的工具，不要混淆。

## 我的方案

这样的小工具，用Python写最简单了，基于PyPDF2（*a pure-python PDF library*）。

要达成我们的目的，需要深入了解库中的[`RectangleObject class`](https://pythonhosted.org/PyPDF2/RectangleObject.html#PyPDF2.generic.RectangleObject)，但是官方文档太简单，经过探究，下面用图例的方式对其作出详细说明：

```
LL(lowerLeft)     .          UL(upperLeft)
                  |
  ----------------.-------------> Y
  |               |
  |               .
  |               |
  |               .
  |               |
  |               .
  |               |
  |               .
  |               |
  V  X            .
                  |  
LR(lowerRight)    .          UR(upperRight)
                  |          
```

这是我们站在复印机前俯视机器时的效果，书籍竖放摊开，因此 **Y轴方向是A3长边**，我们希望分割的就是Y轴。而文档中所谓的 *upper*、*left* 等方向，是从观察者左侧俯视的结果，或者理解为 **X轴正向为右，Y轴正向为上**。

理解了文档，代码就不难写出了，代码中给出了相应的注释：

```python
#coding=utf-8
from PyPDF2 import PdfFileWriter, PdfFileReader
from copy import copy
from os import listdir

def op(inputFilePath):
    outputFilePath = inputFilePath[:-4]+'-print.pdf'

    inputFile = open(inputFilePath, 'rb')
    inputStream = PdfFileReader(inputFile)
    outputStream = PdfFileWriter()

    for page in [inputStream.getPage(i) for i in range(inputStream.getNumPages())]:
        pageLeft = page
	#注意：简单的assignment会导致左、右切割操作同一页面对象
        pageRight = copy(page)
	#切割得到左页面时，切割线比中线稍微向右去一点
        pageLeft.mediaBox.upperRight = (pageLeft.mediaBox.getUpperRight_x(), pageLeft.mediaBox.getUpperRight_y() * 52/100)
	#切割得到右页面时，切割线比中线稍微向左去一点
        pageRight.mediaBox.lowerRight = (pageRight.mediaBox.getLowerRight_x(), pageRight.mediaBox.getUpperRight_y() * 48/100)
        outputStream.addPage(pageLeft)
        outputStream.addPage(pageRight)

    with open(outputFilePath, "wb") as outputFile:
        outputStream.write(outputFile)

    inputFile.close()

#批量处理当前目录下的所有PDF文件
for file in listdir('.'):
    if file[-4:]=='.pdf' or file[-4:]=='.PDF':
        op(file)
```

最后，可以下载使用发布好的[Windows版本工具](https://raw.githubusercontent.com/baoyukun/PDF-crop/master/tool.exe)，只需轻轻双击，当前目录下的所有PDF文档全搞定！工具只会生成切割后新的`-print.pdf`后缀文件，不会删除或者覆盖原文件，还不快来试试呀(｡･ω･｡)

>对于非双页扫描的普通PDF文件，切割效果是上下分割，这是正常的，原因就藏在上面的图示里咯！
