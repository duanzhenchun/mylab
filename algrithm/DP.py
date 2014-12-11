#动态规划问题

#package problem

values=[0,8,10,4,5,5]  #方便动态规划
weights=[0,6,4,2,4,3]

n=len(values)
V=15

dp=[[0 for i in range(V+1)] for j in range(n)]
res=0
for i in range(1, n):
    for j in range(V+1):
        if j < weights[i]:
            dp[i][j] = dp[i-1][j]
        else:
            dp[i][j] = max(dp[i-1][j], dp[i-1][j-weights[i]] + values[i])
        res=max(res,dp[i][j])
print dp
print res

