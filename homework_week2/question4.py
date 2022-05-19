# 宿題3を実装していく

# 構造:{A:[B], B:[A,C], C:[B,D], D:[C,E], E:[D,F] F:[E]}と、(A,F)
"""
何ができればいいか
1. 検索がO(1)でできればいい
2. 新しい入力を追加するとき、
・既に辞書のキーの中にその入力と同じものがある場合(例えばCとする)
 (1) まず、そのキーのvalueにアクセスして、入力ページが隣り合ってるノードを見つけてくる(今回ならB,D) 
  さらに、隣り合ってるノードが一つしかなくて、そのノードの値がリストの2番目の値と同じならば構造はそのまま変えない
  また、隣り合ってるノードが一つしかなくて、そのノードの値がリストの1番目の値と同じならば(2)の2行目の処理を行う

  ・そのvalueが空なら？
   変えない
 (2) それぞれのノード(ここではB,D)に対応するvalueのリストから、入力値に対応するものを削除し、代わりにお互いを付け足す(B:[A,D],D:[B,E]になる)
  もし、リストの1番目の値と入力値が同じならば、上のvalueのリストから入力値に対応するものを削除し、リストの1番目の値を書き換える
 (3) 入力に対応するvalueを[(リストの2番目に入ってる値)]に差し替える(C:[B,D]→C:[F])
 (4) (リストの2番目に入ってる値)に対応するvalueのリストに新しい入力値を付け加える
 (5) リストの2番目を入力値に書き換える((A,F)→(A,C))

 これで、新しいデータ構造は{A:[B], B:[A,D], C:[F], D:[B,E], E:[D,F] F:[C,E]}と、(A,C)

・既に辞書のキーの中にその入力と同じものがない場合(例えばGとする)
 (1) ・既に元がX個ある場合
      (リストの1番目に入ってる値)のキーに対応するvalueの元(一点集合になってるはず)を見つけてきて、それに対応するvalueのリストから(リストの1番目に入ってる値)を削除する(今回はB:[C])になる)
     ・元が1個以上X-1個以下の場合
      (4)まで飛ぶ
     ・元が0個の時
      辞書に(入力値):[]を追加して、リストを(入力値,入力値)にする

 (2) (1)で保持したvalueの元で、リストの1番目の値を書き換える((A,C)→(B,C))
 (3) (元々リストの1番目に入ってた値)のキー,valueを削除する
 (4) (リストの2番目に入ってる値)のキーに対応するvalueのリストに、新しい入力値を追加する(今回なら、F:[E,G]になる)
 (5) 辞書に、(入力値):[(リストの2番目に入ってる値)]を追加する(今回なら、G:[F]になる)
 (6) リストの2番目の値を入力値に書き換える((B,C)→(B,G))

3. 特殊な場合は？
・元が0個(空集合)の時
・元が1個の時
・元がX-1個以下の時

4. 改善点
・後から、最初と最後に固定ノードを付け足しておけば場合分けが不要になることがわかった(が、実装をやり直している時間はなかった)
・リンクが2つ伸びてる時と1つ伸びてる時で場合分けするのが面倒な時には、Noneを足しとくと数が揃っていいらしい
・prev dict とnext dict に分けてもよかったかも

"""

import sys

# 保持できる元の個数がXのキャッシュを作る
class Cache:
    def __init__(self,X): #インスタンスを保持
        self.X = X
        self.dictionary = {}
        self.edges = [None,None]

    # キャッシュの中に何があるかを表示する
    def show(self):
        return self.dictionary.keys()

    # 新しい入力を追加する
    def add_input(self,new_input):

        #既に入力と同じ値が保持されている場合
        if new_input in self.dictionary:

            #まず、(1)(2)を実装
            # self.dictionary[new_input]の長さで場合分け
            if len(self.dictionary[new_input]) == 0:
                return
            
            elif len(self.dictionary[new_input]) == 1:
                next_page = self.dictionary[new_input][0]

                # new_inputの値がedgesの最初の値と同じなら、valueのリストから入力値に対応するものを削除し、リストの1番目の値を書き換える
                if new_input == self.edges[0]:
                    self.dictionary[next_page].remove(new_input)
                    self.edges[0] = next_page

                # new_inputの値がedgesの最後の値と同じなら、何もしない
                if new_input == self.edges[1]:
                    return
                    
            elif len(self.dictionary[new_input]) == 2:
                prev_page, next_page = self.dictionary[new_input]

                #入力値に対応するものを削除し、代わりにお互いを付け足す
                for i,page in enumerate([prev_page, next_page]):
                    self.dictionary[page].remove(new_input)
                    self.dictionary[page].append([prev_page, next_page][1-i])

            
            #(3)を実装
            self.dictionary[new_input] = [self.edges[1]]

            #(4)を実装
            self.dictionary[self.edges[1]].append(new_input)

            #(5)を実装
            self.edges[1] = new_input


        #まだ入力と同じ値が保持されてない場合
        else:
            # dictの長さで場合分け
            if len(self.dictionary) == 0:
                self.dictionary[new_input] = []
                self.edges = [new_input,new_input]
                return

            elif self.X>=2 and (1 <= len(self.dictionary)) and (len(self.dictionary) <= self.X-1):
                #(4)を実装
                self.dictionary[self.edges[1]].append(new_input)

                #(5)を実装
                self.dictionary[new_input] = [self.edges[1]]

                #(6)を実装
                self.edges[1] = new_input


            elif len(self.dictionary) == self.X:
                first_page = self.edges[0]
                if self.X == 1:
                    #(2)(3)を実装
                    self.edges[0] = new_input
                    self.dictionary.pop(first_page)

                    #(6)を実装
                    self.edges[1] = new_input

                    #(5)を実装
                    self.dictionary[new_input] = []



                elif self.X >= 2:
                    #(1)(2)(3)を実装
                    second_page = self.dictionary[first_page][0]
                    self.dictionary[second_page].remove(first_page)
                    
                    self.edges[0] = second_page

                    self.dictionary.pop(first_page)

                    #(4)を実装
                    self.dictionary[self.edges[1]].append(new_input)

                    #(5)を実装
                    self.dictionary[new_input] = [self.edges[1]]

                    #(6)を実装
                    self.edges[1] = new_input

"""
x = 2
cache = Cache(x)
cache.add_input("A")
cache.add_input("B")
cache.add_input("C")
print(cache.show())
"""





                    
            



           