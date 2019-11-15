#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from threading import Thread

import timeunit
import bs4
from selenium import webdriver

studyName='办公室管理'


def getAnswerElement(elements,neirong):
    for ele in elements:
        if neirong in ele.text:
            return ele

def getAnswerElementEquals(elements,neirong):
    for ele in elements:
        if "A. "+neirong == ele.text or "B. "+neirong == ele.text or "C. "+neirong == ele.text or "D. "+neirong == ele.text :
            return ele

file=open('key_bangongguanli.txt')
keys=[]
for line in file.readlines():
    keys.append(line.strip())
for i in keys:
    print(i.split("\t"))
