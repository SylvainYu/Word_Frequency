from wordcloud import WordCloud
import matplotlib.pyplot as plt
import sys
import jieba
import codecs

filename = "官仙v全集v陈风笑.txt"
text = open(filename).read()

# 去掉Notepad文件头添加的3个不可见字符
if text[:3] == codecs.BOM_UTF8:
    text = text[3:]

# 结巴分词
mytext = jieba.cut(text, cut_all=False) # 精准模式，true为全模式
wt = " /".join(mytext)

# 设置词云
wc = WordCloud(background_color = "black",
                max_words = 100,
                font_path = "simsun.ttf",
                max_font_size = 50,
                random_state = 30,
                )
mycloud = wc.generate(wt)

# wordcloud = WordCloud().generate(mytext)

plt.imshow(mycloud)
plt.axis("off")
plt.show()
