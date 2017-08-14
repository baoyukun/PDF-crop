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
