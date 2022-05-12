# ある文字列Sが与えられているときに、Sの部分列のAnagramであって辞書に載ってる単語のうちスコアが最大のものを一つ書く
from question1 import search
import numpy as np

# 1.辞書の各単語を{[(aが出現する回数),(bが出現する回数),,,,,]}のリストに書き換える (N✖️(文字列の長さ))
# 2.ターゲットの文字列Sも同じように書き換える (Sの長さ)
# 3.辞書上の各単語について、任意のa~zでそれに該当する登場回数がSより少なくなっている場合は、その登場回数の和を求めて、既存の和より大きい場合は更新する (O(N))
#全部掛け合わせるとO(N):Maxをとるので、これ以上小さくなるアルゴリズムは存在しなさそう

"""
クエリあたりで何もしないと
O(QN)
これより小さくなることある？
"""

#まず、文字列を変換
def string_to_list(S):
    l = [0]*26
    for s in S:
        idx = ord(s)-ord('a')
        l[idx] += 1
    return l

#まず、辞書を一気にファイルから出してリスト化しておく
dict_list = []
dict_words = []
with open("/Users/yamashitashiori/Desktop/Python3/STEP_homework/step2/anagram/words.txt") as f_words:
    line = f_words.readline()
    while line:
        line_mod = line.replace('\n','')
        l = string_to_list(line_mod)
        dict_list.append(l)
        dict_words.append(line_mod)
        line = f_words.readline()

#print(dict_list[0])
def cal_score(l):
    point_list = np.array([1,3,2,2,1,3,3,1,1,4,4,2,2,1,1,3,4,1,1,1,2,3,3,4,3,4])
    l = np.array(l)
    return np.sum(point_list*l)
    

def search_max(S,dict_list):
    s_list = string_to_list(S)
    max_score = 0
    max_idx = 0
    for i,word_list in enumerate(dict_list):
        sub_s = True
        for j in range(26):
            if word_list[j] > s_list[j]:
                sub_s = False
                break
        if sub_s:
            current_score = cal_score(word_list)
            if max_score < current_score:
                max_score = current_score
                max_idx = i

        
    return dict_words[max_idx]

"""
with open("/Users/yamashitashiori/Desktop/Python3/STEP_homework/step2/anagram/small.txt") as f_small:
    line = f_small.readline()
    while line:
        line_mod = line.replace('\n','')
        print(search_max(line_mod,dict_list))
        line = f_small.readline()

"""
"""
path_ans_small = "homework_week1/answer_small.txt"
f_ans_small = open(path_ans_small,"w")
with open("step2/anagram/small.txt") as f_small:
    line = f_small.readline()
    while line:
        line_mod = line.replace('\n','')
        f_ans_small.write(search_max(line_mod,dict_list)+'\n')
        line = f_small.readline()

f_ans_small.close()
#You answer is correct! Your score is 193.

"""
"""
path_ans_medium = "homework_week1/answer_medium.txt"
f_ans_medium = open(path_ans_medium,"w")
with open("step2/anagram/medium.txt") as f_medium:
    line = f_medium.readline()
    while line:
        line_mod = line.replace('\n','')
        f_ans_medium.write(search_max(line_mod,dict_list)+'\n')
        line = f_medium.readline()

f_ans_medium.close()
#You answer is correct! Your score is 18911.


"""
path_ans_large = "homework_week1/answer_large.txt"
f_ans_large = open(path_ans_large,"w")
with open("step2/anagram/large.txt") as f_large:
    line = f_large.readline()
    while line:
        line_mod = line.replace('\n','')
        f_ans_large.write(search_max(line_mod,dict_list)+'\n')
        line = f_large.readline()

f_ans_large.close()

