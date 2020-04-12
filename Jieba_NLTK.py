# coding=utf-8
# -*- coding: cp936 -*-

# This whole script is from https://www.jianshu.com/p/aea87adee163, on 2020-4-10

import jieba
import jieba.posseg as pseg
import codecs
import re # ������ʽģ�飬Python����ģ��
import os
import time
import string
from nltk.probability import FreqDist
open=codecs.open

#jieba �ִʿ��Խ����ǵ��Զ���ʵ䵼�룬��ʽ ���ʡ� �����ԡ� ����Ƶ��
jieba.load_userdict('data/userdict.txt')

#����һ��keyword��
class keyword(object):
    def Chinese_Stopwords(self):          #����ͣ�ôʿ�
        stopword=[]
        cfp=open('data/stopWord.txt','r+','utf-8')   #ͣ�ôʵ�txt�ļ�
        for line in cfp:
            for word in line.split():
                stopword.append(word)
        cfp.close()
        return stopword

    def Word_cut_list(self,word_str):
        #����������ʽȥ��һЩһЩ������֮��ķ��š�
        word_str = re.sub(r'\s+', ' ', word_str)  # trans ��ո� to�ո�
        word_str = re.sub(r'\n+', ' ', word_str)  # trans ���� to�ո�
        word_str = re.sub(r'\t+', ' ', word_str)  # trans Tab to�ո�
        word_str = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+������������������������������~@#��%����&*����1234567�٢ڢۢ�)]+".\
                          decode("utf8"), "".decode("utf8"), word_str)
  
        wordlist = list(jieba.cut(word_str))#jieba.cut  ���ַ����и�ɴʲ������һ���б�
        wordlist_N = []
        chinese_stopwords=self.Chinese_Stopwords()
        for word in wordlist:
            if word not in chinese_stopwords:#�������ϴ��ȥͣ�ô�
                if word != '\r\n'  and word!=' ' and word != '\u3000'.decode('unicode_escape') \
                        and word!='\xa0'.decode('unicode_escape'):#�������ϴ��ȥȫ�ǿո�
                    wordlist_N.append(word)
        return wordlist_N

    def Word_pseg(self,word_str):  # ������ȡ����
        words = pseg.cut(word_str)
        word_list = []
        for wds in words:
            # ɸѡ�Զ���ʵ��еĴʣ��͸������ʣ��Զ���ʿ�Ĵ���û���ô��Ե������Ĭ��Ϊx���ԣ����ʵ�flag����Ϊx
            if wds.flag == 'x' and wds.word != ' ' and wds.word != 'ns' \
                    or re.match(r'^n', wds.flag) != None \
                            and re.match(r'^nr', wds.flag) == None:
                word_list.append(wds.word)
        return word_list

    def sort_item(self,item):#����������������
        vocab=[]
        for k,v in item:
            vocab.append((k,v))
        List=list(sorted(vocab,key=lambda v:v[1],reverse=1))
        return List

    def Run(self):
        Apage=open(self.filename,'r+','utf-8')
        Word=Apage.read()                       #�ȶ�ȡ��ƪ����
        Wordp=self.Word_pseg(Word)              #����ƪ���½��д��Ե���ѡ
        New_str=''.join(Wordp)
        Wordlist=self.Word_cut_list(New_str)    #����ѡ������½��зִ�
        Apage.close()
        return  Wordlist

    def __init__(self, filename):
        self.filename = filename

if __name__=='__main__':
    b_path = 'data/all'
    a_path = 'data/Result'
    roots = os.listdir(b_path)
    alltime_s = time.time()
    for filename in roots:
        starttime = time.time()
        kw = keyword(b_path + '/' + filename)
        wl = kw.Run()
        fdist = FreqDist(wl)
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
        print filename + '       ���ʱ�䣺' + str(endtime - starttime)

    print "����ʱ��" + str(time.time() - alltime_s)


