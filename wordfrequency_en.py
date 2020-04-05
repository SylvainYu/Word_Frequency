from wordcloud import WordCloud
import matplotlib.pyplot as plt
import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

filename = "WildCherylStrayed.txt"
mytext = open(filename, encoding="utf-8").read()

wordcloud = WordCloud().generate(mytext)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

plt.show()
