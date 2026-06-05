import sys
def solve():
    input=sys.stdin.readline()
    print(input)
    T=int (input())
    for _ in range(T):
        n,k= map(int ,input().split() )
        a=list(map(int,sys.stdin.readline().split()))
        INF=float('inf')
        dp=[INF]*n
        for i in range(n):
            dp[i]=a[i]+i*k
            ans=[0]*n
            ans[0]=min(dp)
        for j in range(2,n+1):
            new_dp=[INF]*n
            min_val=INF
            for i in range(j-1,n):
                t=i-1
                if t>=0:
                    min_val=min(min_val,dp[t]-t*k)
                if min_val<INF:
                    new_dp[i]=min_val+(i-1)*k+a[i]
            dp=new_dp
            ans[j-1]=min(dp)
        print(' '.join(map(str,ans)))
if __name__=="__main__":
    solve()
                        