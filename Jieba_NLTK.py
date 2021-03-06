# coding=utf-8
# -*- coding: cp936 -*-

# This whole script is from https://www.jianshu.com/p/aea87adee163, on 2020-4-10

import jieba
import jieba.posseg as pseg     # 词性标注分词器，jieba.posseg.dt，200421
import codecs
import re
import os
import time
import string
from nltk.probability import FreqDist
open=codecs.open

#jieba 分词可以将我们的自定义词典导入，格式 “词” “词性” “词频”
jieba.load_userdict('data/userdict.txt')

#定义一个keyword类
class keyword(object):
    def Chinese_Stopwords(self):          #导入停用词库
        stopword=[]
        cfp=open('data/stopWord.txt','r+','utf-8')   #停用词的txt文件
        for line in cfp:
            for word in line.split():
                stopword.append(word)
        cfp.close()
        return stopword

    def Word_cut_list(self,word_str):
        #利用正则表达式去掉一些一些标点符号之类的符号。
        word_str = re.sub(r'\s+', ' ', word_str)  # trans 多空格 to空格
        word_str = re.sub(r'\n+', ' ', word_str)  # trans 换行 to空格
        word_str = re.sub(r'\t+', ' ', word_str)  # trans Tab to空格
        word_str = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——；！，”。《》，。：“？、~@#￥%……&*（）1234567①②③④)]+".\
                          decode("utf8"), "".decode("utf8"), word_str)
  
        wordlist = list(jieba.cut(word_str))#jieba.cut  把字符串切割成词并添加至一个列表
        wordlist_N = []
        chinese_stopwords=self.Chinese_Stopwords()
        for word in wordlist:
            if word not in chinese_stopwords:#词语的清洗：去停用词
                if word != '\r\n'  and word!=' ' and word != '\u3000'.decode('unicode_escape') \
                        and word!='\xa0'.decode('unicode_escape'):#词语的清洗：去全角空格。不过全角字符较多，为啥光去一个全角空格？？？200421
                    wordlist_N.append(word)
        return wordlist_N

    def Word_pseg(self,word_str):  # 名词提取函数
        words = pseg.cut(word_str)
        word_list = []
        for wds in words:
            # 筛选自定义词典中的词，和各类名词，自定义词库的词在没设置词性的情况下默认为x词性，即词的flag词性为x
            if wds.flag == 'x' and wds.word != ' ' and wds.word != 'ns' \
                    or re.match(r'^n', wds.flag) != None \
                            and re.match(r'^nr', wds.flag) == None:
                word_list.append(wds.word)
        return word_list

    def sort_item(self,item):#排序函数，正序排序
        vocab=[]
        for k,v in item:
            vocab.append((k,v))
        List=list(sorted(vocab,key=lambda v:v[1],reverse=1))    # 用到lambda了！！！200421
        return List

    def Run(self):
        Apage=open(self.filename,'r+','utf-8')
        Word=Apage.read()                       #先读取整篇文章
        Wordp=self.Word_pseg(Word)              #对整篇文章进行词性的挑选
        New_str=''.join(Wordp)
        Wordlist=self.Word_cut_list(New_str)    #对挑选后的文章进行分词
        Apage.close()
        return  Wordlist

    def __init__(self, filename):
        self.filename = filename

if __name__=='__main__':        # 用到__init__，在一个自定义类中；也用到__name__和__main__，在主程序中。200421
    b_path = 'data/all'
    a_path = 'data/Result'
    roots = os.listdir(b_path)
    alltime_s = time.time()
    for filename in roots:
        starttime = time.time()
        kw = keyword(b_path + '/' + filename)
        wl = kw.Run()
        fdist = FreqDist(wl)    # NLTK的频率函数？和手写的词频函数有啥区别？200421
        Sum = len(wl)
        pre = 0
        fn = open(a_path + '/' + filename, 'w+', 'utf-8')
        fn.write('sum:' + str(Sum) + '\r\n')
        for (s, n) in kw.sort_item(fdist.items()):
            fn.write(s + str(float(n) / Sum)+"      " +str(n)+ '\r\n')
            pre = pre + float(n) / Sum
            if pre > 0.5:
                fn.write(str(pre))
                fn.close()
                break
        endtime = time.time()
        print filename + '       完成时间：' + str(endtime - starttime)

    print "总用时：" + str(time.time() - alltime_s)


