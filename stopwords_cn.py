import sys
import codecs
import jieba

# 创建停用词列表
def stopwordslist():
    csdn_stopwords = [line.strip() for line in open('CSDN_stopwords.txt',encoding='UTF-8').readlines()]
    return csdn_stopwords

def drop_stopwords(words_in):
    
    # word_lst = []
    # for line in words_in:
    #     item = line.strip('\n\r').split('\t')
    #     tags = jieba.analyse.extract_tags(item[0])
    #     for t in tags:
    #        word_lst.append(t) # word_lst是词语列表，不像text是单字列表
    
    jieba.load_userdict(open('userdict.txt', encoding='UTF-8'))
    
    word_lst = jieba.cut(words_in) # 先jieba分词，再去停止词。不过去了停止词后全文单词数缩减
    
    csdn_stopwords = stopwordslist()

    outstr = []

    for word in word_lst:
        if word not in csdn_stopwords:
            if word != '\t':
                outstr.append(word)

    wt = " /".join(outstr)

    return wt


