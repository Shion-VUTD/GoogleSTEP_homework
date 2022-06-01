# question1では、Googleから渋谷へ至る経路があるか探します

import re
from collections import deque
from turtle import st
# graghを隣接リストの形で保持する
# idと名称のセットを辞書で保存する

graph = {}
id_to_name = {}
name_to_id = {}

# homework_week4 に移って実行してください

with open("./data/links_small.txt") as f:
    for line in f:
        # とりあえず2つの数字をlistにして読み込む
        line = line.replace('\n','')
        line_mod = re.sub('\s+',' ',line)
        relative_nodes = list(map(int,line_mod.split(' ')))
        #print(relative_nodes)

        # 隣接リストに追加
        for i, node_id in enumerate(relative_nodes):
            if node_id in graph:
                graph[node_id].append(relative_nodes[1-i])
            else:
                graph[node_id] = [relative_nodes[1-i]]

#print(graph.keys())


with open("./data/pages_small.txt") as f_:
    for line in f_:
        line = line.replace('\n','')
        id, name = line.split('\t')
        id = int(id)   
        id_to_name[id] = name
        name_to_id[name] = id

#print(id_and_name)


# dfs,bfsの実装
# idを使ってdfs
def id_dfs(graph,start_id,target_id):
    stack = []
    # 探索済みかどうかを保持
    visited_list = [False]*(max(graph.keys())+1) # なんでノード1-indexにしたんや……

    stack.append(start_id)
    visited_list[start_id] = True

    while len(stack) > 0: # stackに入ってるノードがなくなるまで続ける
        #print(visited_list)
        #print(stack)
        node = stack.pop(-1) # 全てのノードを最大1度ずつ見るので、これを繰り返すことによる計算量は合計O(V)
        if node == target_id:
            return True
        
        for next_node in graph[node]: # 全てのエッジを最大1度ずつ見るので、これを繰り返すことによる計算量はO(E)
            if visited_list[next_node] == False:
                visited_list[next_node] = True
                stack.append(next_node)

    return False

# idを使ってbfs
def id_bfs(graph,start_id,target_id):

    # データ構造を初期化
    visited_list = [False]*(max(graph.keys())+1)
    queue = deque([])

    #初期値を入れる
    visited_list[start_id] = True
    queue.append(start_id)

    while len(queue) > 0:
        node = queue.popleft()
        #print(queue)
        #print(visited_list)

        if node == target_id:
            return True
         
        for next_node in graph[node]:
            if visited_list[next_node] == False:
                visited_list[next_node] = True
                queue.append(next_node)

    return False


# 名称からidを抽出
def name_dfs(graph,start_name,target_name):
    # 名称をidに変換
    start_id = name_to_id[start_name]
    target_id = name_to_id[target_name]

    return id_dfs(graph,start_id,target_id)


def name_bfs(graph,start_name,target_name):
    # 名称をidに変換
    start_id = name_to_id[start_name]
    target_id = name_to_id[target_name]

    return id_bfs(graph,start_id,target_id)



print(id_bfs(graph,30,1089))
print(id_dfs(graph,30,1089))
print(name_bfs(graph,'人工知能','アイスクリーム'))