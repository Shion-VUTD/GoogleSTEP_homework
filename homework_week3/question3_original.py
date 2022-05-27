from question1 import read_number, read_plus, read_minus, read_asterisk, read_slash, evaluate_multidiv, evaluate_only_multidiv,evaluate_plusminus,evaluate_arithmeticoperations
import sys

# 左かっこと右かっこを読み込む
def read_left_parenthesis(line,index):
  token = {'type': 'LEFT_PARENTHESIS'}
  return token, index + 1

def read_right_parenthesis(line,index):
  token = {'type': 'RIGHT_PARENTHESIS'}
  return token, index + 1

def tokenize(line): # 入力文字列を受け取って、字句を表すtokenのリストを返す　("1+2" --> [{'type': 'NUMBER', 'number': 1}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 2}])
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = read_number(line, index)
    elif line[index] == '+':
      (token, index) = read_plus(line, index)
    elif line[index] == '-':
      (token, index) = read_minus(line, index)
    elif line[index] == '*':
      (token, index) = read_asterisk(line, index)
    elif line[index] == '/':
      (token, index) = read_slash(line, index)
    elif line[index] == '(':
      (token, index) = read_left_parenthesis(line, index)
    elif line[index] == ')':
      (token, index) = read_right_parenthesis(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens


def evaluate_with_parenthesis(tokens): # かっこ付きの計算を行う

    parenthesis_processed_tokens = []
    index = 0
    parenthesis_depth = 0
    # print(tokens)
    
    # 内側のかっこを抽出して、その中の計算を内側のevaluate_parenthesisに預ける
    while index < len(tokens):

        if tokens[index]["type"] == "LEFT_PARENTHESIS":
            if parenthesis_depth == 0:
                index_start = index + 1
            parenthesis_depth += 1

        elif tokens[index]["type"] == "RIGHT_PARENTHESIS":

            parenthesis_depth -= 1
            # print("DEPTH:",parenthesis_depth)

            # 右かっこの方が多いやつをケア
            if parenthesis_depth == -1:
              print("SyntaxError: The number of ( is smaller than the number of )")
              break

            if parenthesis_depth == 0:
                in_parenthesis_tokens = tokens[index_start:index]

                # ()みたいなやつをケア
                if len(in_parenthesis_tokens) == 0:
                  print("SyntaxError: This formula is including ()")
                  break
          
                # print(in_parenthesis_tokens)
                in_parenthesis_answer = evaluate_with_parenthesis(in_parenthesis_tokens)
                parenthesis_processed_tokens.append({"type":"NUMBER","number":in_parenthesis_answer})

        else:
            if parenthesis_depth == 0:
                parenthesis_processed_tokens.append(tokens[index])
        
        index += 1


    # 左かっこの方が多いやつをケア
    if parenthesis_depth > 0:
      print("SyntaxError: The number of ) is smaller than the number of (")
  
    
    else:
      #print("parenthesis_processed_tokens:",parenthesis_processed_tokens)
      answer = evaluate_arithmeticoperations(parenthesis_processed_tokens)
      return answer



def test(line):
  tokens = tokenize(line)
  # print("tokens:",tokens)
  actual_answer = evaluate_with_parenthesis(tokens)
  # print("actual answer is", actual_answer)
  expected_answer = eval(line) # eval:pythonの組み込み関数で、"2+3"(文字列)を5(int)にしてくれるやつ
  if abs(actual_answer - expected_answer) < 1e-8: # 誤差のケア
    print("PASS! (%s = %f)" % (line, expected_answer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  test("3.0+4*2-1/5")
  test("0.0*1.0-5.0/1.0*2.0")
  test("((1+2)+3)+(4+5)")
  test("(1.0+2.0)*3+((1*3*2+4)/2)")
  test("(((1.0+2.0)*3)/2+1)+((1*3*2+4)/2)")
  test("1")
  test("((1))")
  # test("(1+2)+3+4)") # ちゃんとSyntaxError: The number of ( is smaller than the number of )が出ることを確認する
  # test("((1+2)+3)+(4+(2+3)") # ちゃんとSyntaxError: The number of ) is smaller than the number of (が出ることを確認する
  # test("()+2") # ちゃんとSyntaxError: This formula is including ()が出ることを確認する
  # test("(1+2)+(3)(4)") # 前のquestionでのSyntax Eoorでケアされる

  # ここ、本当は「エラー吐いたらeval()も実行しない」みたいな仕様に出来ればよかったんだけど、時間がありませんでした。
  print("==== Test finished! ====\n")


run_test()


"""
while True:
  print('> ', end="")
  line = input() # 式を文字列として入力
  tokens = tokenize(line) # 文字列を字句に分割
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)

"""

"""
Question3 のドキュメント

・方針
Question1は2種類の演算に順番をつけて計算をするようなプログラムであったが、今回はそれがn個あるので、同じことを再帰に当てはめて実装する

(例)
( ( 1 + 2 ) + 3 ) + ( 4 + 5 )

1.tokenを受け取り、最も外側のかっこを探す
 1-1. かっこがあれば、その中で同じ処理を行う
 1-2. かっこがなければ、普通に四則演算をする
   終了してない関数がないなら、値のみを返す
   終了してない関数があるなら、{"tyoe":"NUMBER,"number":answer} なるtokenを生成して、そこに既存の{"tyoe":"PLUS"},{"type":"MINUS}を付け足した新しいtokenを保持する


で実装しました


・エラーについて
ここで扱ってる「正しい式」とは何か？

 再帰の骨格によると
 ( ( 1 + 2 ) + 3 ) + ( 4 + 5 )
 
 最終的に想定されてる初期値は{数字をn(nは0以上の整数)回四則演算させたやつ}なので、

 正しい式 := {数字と、その間に0個以上の+-を含む列} or {(正しい式)と、その間に0個以上の+-を含む列}

 よって、これ以外のやつはSyntax Errorで落としていけばいい

・改善点
1. 再帰のくせにwhile使ってるのが気持ち悪すぎる
・今回は、「一番外側のかっこを見つけたら、その中で同じ処理を行う」という方針で実装し、その「一番外のかっこを見つける」という処理にwhileとか
  parenthesis_depthとかを使ってしまっている
・これを、「左かっこが現れれば再帰処理を開始し、右かっこが現れればその再帰処理を終了する」という方針に変更すると…?
  --> 時間があれば実装します……

2. 方針の1-2の内部でやってる、「値を返すか、tokenとして保持しておくか」の場合分けは本当に必要なのか？
・うまくやれば全部 return 値　でいける気がする
  --> 時間があれば実装します……


"""