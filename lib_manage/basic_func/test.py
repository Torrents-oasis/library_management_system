# -*- coding:utf-8 -*-
# 防止中文注释报错
"""
author: GuoMinghao
date:   2022-05-18
"""
import pandas as pd
path = r'./static/file/book_info.xlsx'
info = pd.read_excel(path)   # 直接使用 read_excel() 方法读取
print(info)
print(type(info))

for item in info.index:
    # for attr in range(8):
    print(info.loc[item].values[0])
