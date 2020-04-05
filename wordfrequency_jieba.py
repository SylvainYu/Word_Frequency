
#! python3

# -*- coding: utf-8 -*-

import os, codecs

import jieba

from collections import Counter

 

def get_words(txt):

    seg_list = jieba.cut(txt)

    c = Counter()

    for x in seg_list:

        if len(x)>1 and x != '\r\n':

            c[x] += 1

    print('常用词频统计结果')

    print('全文词汇数量：', sum(c.values()))

    for (k,v) in c.most_common(100): 

        # print('%s%s %s  %d' % ('  '*(5-len(k)), k, '*'*int(v/3), v))
        print('%s %s  %d' % (k, '-->', v))

 

if __name__ == '__main__':

    with codecs.open('19d.txt', 'r', 'utf8') as f:

        txt = f.read()

    get_words(txt)

# 后续考虑用户自定义词组添加，停止词去除（多个停止词文件遍历）；
# 还得考虑在全部监督记录中2496个“不符”经常与什么内容搭配在一起出现；
# 3082个“不足”的word2vector？
