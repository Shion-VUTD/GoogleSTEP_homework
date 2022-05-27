from question1 import read_number, read_plus, read_minus, read_asterisk, read_slash
from question3_original import read_left_parenthesis, read_right_parenthesis, tokenize
import sys

def consume_expr(tokens,index): # 式を読み込む関数
    #最小単位（初期値）は数字
    if tokens[index]['type'] == 'NUMBER':
        ans = tokens[index]['number']
        return tokens,index+1,ans


    # 左かっこが出た場合
    elif tokens[index]['type'] == 'LEFT_PARENTHESIS':
        tokens, new_index, ans = consume_operative_expr(tokens,index+1)
        print(new_index)
        print("index:",new_index,tokens[new_index]['type'])
        if tokens[new_index]['type'] == 'RIGHT_PARENTHESIS':
            return tokens, new_index+1 , ans

    else:
        print('SyntaxError')


def consume_operative_expr(tokens,index):
    tokens, new_index, ans = consume_expr(tokens,index)
    print('new_index2',new_index)
    while True:
        if new_index >= len(tokens):
            break
        if tokens[new_index]["type"] not in ('PLUS','MINUS','ASTERISK','SLASH'):
            break
        if tokens[new_index]["type"] in ('PLUS','MINUS'):
            token, new_index, ans2 = consume_multidiv_expr(tokens,new_index+1)
            print('waiwai',new_index)

        elif tokens[new_index]["type"] in ('ASTERISK','SLASH'):
            token, new_index, ans2 = consume_expr(tokens,new_index+1)

        ans += ans2


    return tokens, new_index , ans

def consume_multidiv_expr(tokens,index):
    tokens, new_index, ans = consume_expr(tokens,index)
    print('new_index',new_index)
    while True:
        if new_index >= len(tokens):
            break
        if tokens[new_index]["type"] not in ('ASTERISK','SLASH'):
            break
        
        token, new_index, ans2 = consume_expr(tokens,new_index+1)
        ans *= ans2

    print(new_index)
    return tokens, new_index, ans


def test(line):
  tokens = tokenize(line)
  tokens = [{"type":"LEFT_PARENTHESIS"}] + tokens + [{"type":"RIGHT_PARENTHESIS"}]
  # print("tokens:",tokens)
  tokens, index, actual_answer = consume_expr(tokens,index=0)
  # print("actual answer is", actual_answer)
  expected_answer = eval(line) # eval:pythonの組み込み関数で、"2+3"(文字列)を5(int)にしてくれるやつ
  print("expected_answer" ,expected_answer)
  if abs(actual_answer - expected_answer) < 1e-8: # 誤差のケア
    print("PASS! (%s = %f)" % (line, expected_answer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))

def run_test():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1+3")
  test("3.0+4*2+1*5")
  test("0.0*1.0+5.0*1.0*2.0") #なんか答え間違えられてて草
  test("((1+2)+3)+(4+5)")
  test("(1.0+2.0)*3+((1*3*2+4)*2)")
  test("(((1.0+2.0)*3)/2+1)+((1*3*2+4)/2)")
  test("1")
  test("((1))")
  # test("(1+2)+3+4)") # ちゃんとSyntaxError: The number of ( is smaller than the number of )が出ることを確認する
  # test("((1+2)+3)+(4+(2+3)") # ちゃんとSyntaxError: The number of ) is smaller than the number of (が出ることを確認する
  # test("()+2") # ちゃんとSyntaxError: This formula is including ()が出ることを確認する
  # test("(1+2)+(3)(4)") # 前のquestionでのSyntax Eoorでケアされる

  # ここ、本当は「エラー吐いたらeval()も実行しない」みたいな仕様に出来ればよかったんだけど、時間がありませんでした。
  print("==== Test finished! ====\n")

if __name__ == "__main__":
  run_test()


# バグらせまくってるので、死