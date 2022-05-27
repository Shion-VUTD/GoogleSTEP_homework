# 再帰の練習をしています

# input:tokens
# output:answer(int)

# 式 := 数 | 開きかっこ 加算式 閉じかっこ 
# 加算式 := 式 + 式 + ..... + 式
# before: I 1   )
# after :   1 I )

def consume_additive_expr(tokens,index):
    tokens, new_index, ans = consume_expr(tokens,index)
    while True:
        if new_index >= len(tokens):
            break
        if tokens[new_index]["type"] != 'PLUS':
            break
        tokens,new_index,ans2 = consume_expr(tokens,new_index+1)
        ans += ans2

    return tokens, new_index , ans

def consume_expr(tokens,index): # カーソルを動かしてtoken列を消費する
    if tokens[index]["type"] == "NUMBER":
        ans = tokens[index]['number']
        return tokens,index+1,ans

    elif tokens[index]["type"] == "LEFT_PARENTHESIS":
        tokens, new_index, ans = consume_additive_expr(tokens,index+1)
        if tokens[new_index]["type"] == "RIGHT_PARENTHESIS":
            return tokens, new_index+1, ans
        else:
            raise Exception("かっこが揃っていません") 

    else:
        raise Exception("かっこが揃っていないか未知のtokenです")



# print(consume_expr([{'type': 'LEFT_PARENTHESIS'}, {'type': 'NUMBER', 'number': 135}, {'type': 'RIGHT_PARENTHESIS'}],index=0))
# print(consume_expr([{'type': 'LEFT_PARENTHESIS'},{'type': 'LEFT_PARENTHESIS'}, {'type': 'NUMBER', 'number': 135}, {'type': 'RIGHT_PARENTHESIS'},{'type': 'RIGHT_PARENTHESIS'}],index=0))

print(consume_expr([{'type': 'LEFT_PARENTHESIS'}, {'type': 'NUMBER', 'number': 1}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 2}, {'type': 'RIGHT_PARENTHESIS'}],0))
# print(consume_additive_expr([{'type': 'NUMBER', 'number': 1}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 2}],0))


def fact(n):
    if n == 0:
        return 1
    else:
        return n*fact(n-1)


