#ある文字列Sがあったときに、そのAnagramであって辞書のリストに属してるものを全て書き出す

#まず、辞書を一気にファイルから出してリスト化しておく
dict_list = []
with open("/Users/yamashitashiori/Desktop/Python3/STEP_homework/step2/anagram/words.txt") as f_words:
    line = f_words.readline()
    while line:
        line_mod = line.replace('\n','')
        dict_list.append(line_mod)
        line = f_words.readline()

#次に、{(ソートした文字列):[(元の文字列),(元の文字列),,,,]}みたいなやつを作る？
d = {}

#辞書をソート
dict_list_sorted = []
for word in dict_list:
    word_sorted = "".join(sorted(word))

    #並べ替えた文字列が既にキーにある場合はそのvalueのリストに元の文字列を付け足す
    if word_sorted in d:
        d[word_sorted].append(word)
    #入ってない場合は(word_sorted:[word])を付け足す
    else:
        d[word_sorted] = [word]
        dict_list_sorted.append(word_sorted)

dict_list_sorted = sorted(dict_list_sorted)
#print(dict_list_sorted)


def search(S,d):
    #文字列をソート
    S_sorted = "".join(sorted(S))
    if S_sorted in d:
        print(" ".join(d[S_sorted]))
    else:
        print("")    

#small.txtについて検証
with open("/Users/yamashitashiori/Desktop/Python3/STEP_homework/step2/anagram/small.txt") as f_small:
    line = f_small.readline()
    while line:
        line = line.replace("\n","")
        search(line,d)
        line = f_small.readline()






