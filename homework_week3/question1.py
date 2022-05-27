# modularized_calculator.pyを改変して乗除もできるようにする

# 最初はmodularized_calculator.pyのコピペ(後でディレクトリ動かすかもなので、一応importの形ではなくてコピペにしている)
def read_number(line, index): # 小数はここで読む
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    decimal = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * decimal
      decimal /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def read_plus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def read_minus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1

def read_asterisk(line,index):
  token = {'type': 'ASTERISK'}
  return token, index + 1

def read_slash(line,index):
  token = {'type': 'SLASH'}
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
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens


def evaluate_only_multidiv(tokens): # 先に乗除だけ計算する
    """
    [{'type': 'NUMBER', 'number': 3.0}, {'type': 'PLUS'}, {'type':'NUMBER','number':4},
    {'type': 'ASTERISK'},{'type': 'NUMBER', 'number': 2},{'type': 'MINUS'},{'type':'NUMBER','number':1},{'type':'SLASH'},{'type':'NUMBER','number':5}] 
    を
    [{'type': 'NUMBER', 'number': 3.0}], {'type': 'PLUS'}, [{'type':'NUMBER','number':8},
    {'type': 'MINUS'},{'type':'NUMBER','number':0.2}]
    にする
    """

    #末尾に"END"を付け足す
    tokens.append({"type":"END"})
    # print(tokens)
    brackets_added_tokens = []
    index = 0
    index_start = 0
    while index < len(tokens):
      if tokens[index]["type"] == "PLUS" or tokens[index]["type"] == "MINUS" or tokens[index]["type"] == "END":
        answer = evaluate_multidiv(tokens[index_start:index])
        brackets_added_tokens.append({'type':'NUMBER','number':answer})

        if tokens[index]["type"] == "PLUS" or tokens[index]["type"] == "MINUS":
          brackets_added_tokens.append({'type':tokens[index]["type"]})

        index_start = index + 1
      index += 1

    # print("brackets_added_tokens:",brackets_added_tokens)
    return brackets_added_tokens
        


def evaluate_plusminus(tokens): # tokensを受け取って足し算と掛け算だけ計算し、値(int)または"Invalid Syntax"を返す
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
      if tokens[index]['type'] == 'NUMBER':
        if tokens[index - 1]['type'] == 'PLUS':
          answer += tokens[index]['number']
        elif tokens[index - 1]['type'] == 'MINUS':
          answer -= tokens[index]['number']
        else:
          print('Invalid syntax')
          exit(1)
      index += 1
    return answer

def evaluate_multidiv(tokens): # 字句を受け取って乗除だけ計算し、値(int)または"Invalid Syntax"を返す
  answer = 1
  tokens.insert(0, {'type': 'ASTERISK'}) # Insert a dummy '+' token
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'ASTERISK':
        answer *= tokens[index]['number']
      elif tokens[index - 1]['type'] == 'SLASH':
        answer /= tokens[index]['number']
      else:
        print('Invalid syntax')
        exit(1)
    index += 1
  return answer

def evaluate_arithmeticoperations(tokens): # 字句を受け取って四則演算を行い、(int)または"Invalid Syntax"を返す
  #まず、掛け算と割り算を計算し、その結果を{'type':'NUMBER','number':answer}に入れる
  tokens = evaluate_only_multidiv(tokens)
  answer = evaluate_plusminus(tokens)
  return answer
  


def test(line):
  tokens = tokenize(line)
  # print("tokens:",tokens)
  actual_answer = evaluate_arithmeticoperations(tokens)
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
  print("==== Test finished! ====\n")

run_test()
print(evaluate_plusminus([{'type': 'NUMBER', 'number': 1}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 2}]))



if __name__ == "__main__":
  run_test()
  print(evaluate_plusminus([{'type': 'NUMBER', 'number': 1}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 2}]))
  while True:
    print('> ', end="")
    line = input() # 式を文字列として入力
    tokens = tokenize(line) # 文字列を字句に分割
    answer = evaluate_arithmeticoperations(tokens)
    print("answer = %f\n" % answer)



"""
Question1 のドキュメント

・方針
乗除→加減の順に計算していくので、
1.tokenを受け取り、乗除部分だけ計算して新しいtokenを返す
 1-1. 数字と乗除しか入ってないtokenを受け取り、それを計算してanswer(int)を返す --- multidiv
 1-2. それらのanswerを受け取り、{"tyoe":"NUMBER,"number":answer} なるtokenを生成して、そこに既存の{"tyoe":"PLUS"},{"type":"MINUS}を付け足した新しいtokenを返す --- evaluate_only_multidiv

2.既存関数を使って加減を計算する

で実装しました


・改善点
1. 多分evaluate_only_multidivにもSyntax errorするべきとこがあるはず(?)
2. 0除算がraiseExceptionでケアされてない

時間があれば実装します……


"""