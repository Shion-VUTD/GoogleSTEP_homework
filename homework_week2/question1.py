# 行列積を求めるプログラムを書いて、行列のサイズNと実行時間の関係を調べる
import time
import numpy as np
import matplotlib.pyplot as plt

def mul_matrix(N,A,B): #サイズN*Nの行列A,Bの積を求める
    ans = [[0]*N for i in range(N)]
    start = time.time()
    for i in range(N):
        for j in range(N):
            #積の(i,j)成分を求める
            ans_ij = 0
            for k in range(N):
                ans_ij += A[i][k] * B[k][j]

            ans[i][j] = ans_ij
    
    return ans, time.time()-start


def cal_average_time(N,m): #成分の範囲が(0,1)なるN*N行列を一様ランダムに生成し、その実行時間のm個の平均を求める
    np.random.seed(seed=0)
    #乱数で行列を生成
    excution_time_sum = 0
    for i in range(m):
        A_i = np.random.rand(N,N)
        B_i = np.random.rand(N,N)
        ans_i, excution_time_i = mul_matrix(N,A_i,B_i)
        excution_time_sum += excution_time_i

    return excution_time_sum/m


def draw_gragh(): #m回ランダムに生成したものの実行時間の平均をとり、Nを縦軸、実行時間の平均を横軸に設定してグラフを描く
    m_list = [10,100,1000]
    N_list = np.arange(1,101)
    excution_time_list_10 = [cal_average_time(N,10) for N in N_list]
    excution_time_list_100 = [cal_average_time(N,100) for N in N_list]
    #excution_time_list_1000 = [cal_average_time(N,1000) for N in N_list]
    plt.plot(N_list,excution_time_list_10,"r",label= "trials:10")
    plt.plot(N_list,excution_time_list_100,"g",label= "trials:100")
    #plt.plot(N_list,excution_time_list_1000,"b",label= "trials:1000")
    plt.legend()
    plt.title("the relation between the size of matrix and excution time")
    plt.xlabel("N")
    plt.ylabel("Excution time")
    plt.show()

    


if __name__ == "__main__":
    draw_gragh()
