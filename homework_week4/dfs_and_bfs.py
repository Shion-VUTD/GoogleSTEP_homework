# 授業で扱ったdfs,bfs実装の復習

from collections import deque
import collections

# グラフを保持
graph = {}
graph[1] = [2,3]
graph[2] = [1]
graph[3] = [1,4,5]
graph[4] = []
graph[5] = [6,7]
graph[6] = [5]
graph[7] = [4]

print(graph)
visited_list = [False]*(len(graph)+1) # なんでノード1-indexにしたんや……
# これ、再帰で関数の内側に組み込むにはどうしたらええねんやろ


# まず、再帰関数で実装
def recursive_dfs(graph,node,target):

    if node == target:
        return True
    for next_node in graph[node]:
        if visited_list[next_node] == False:
            visited_list[next_node] =True
            result = recursive_dfs(graph,next_node,target)
            if result:
                return True

    return False

print(recursive_dfs(graph,1,7))

# 次に、stackで実装
def stack_dfs(graph,start,target):
    stack = []
    # 探索済みかどうかを保持
    visited_list = [False]*(len(graph)+1) # なんでノード1-indexにしたんや……

    stack.append(start)
    visited_list[start] = True

    while len(stack) > 0: # stackに入ってるノードがなくなるまで続ける
        #print(visited_list)
        #print(stack)
        node = stack.pop(-1) # 全てのノードを最大1度ずつ見るので、これを繰り返すことによる計算量は合計O(V)
        if node == target:
            return True
        
        for next_node in graph[node]: # 全てのエッジを最大1度ずつ見るので、これを繰り返すことによる計算量はO(E)
            if visited_list[next_node] == False:
                visited_list[next_node] = True
                stack.append(next_node)

    return False

print(stack_dfs(graph,1,7))
# print(recursive_dfs(graph,1,7) == stack_dfs(graph,1,7))

# BFSのqueueでの実装
def queue_bfs(graph,start,target):

    # データ構造を初期化
    visited_list = [False]*(len(graph)+1)
    queue = deque([])

    #初期値を入れる
    visited_list[start] = True
    queue.append(start)

    while len(queue) > 0:
        node = queue.popleft()
        #print(queue)
        #print(visited_list)

        if node == target:
            return True
         
        for next_node in graph[node]:
            if visited_list[next_node] == False:
                visited_list[next_node] = True
                queue.append(next_node)

    return False

print(queue_bfs(graph,1,7))

