
import sys
def solve():
    input=sys.stdin.readline
    n=int(input())
    a=list(map(int,input().split()))
    max_val=max(a)
    ans=0
    for g in range(2,max_val+1):
        prev1=0
        prev2=0
        for i in range(n):
            if a[i]%g==0:
                cur=max(prev1,prev2+1)
            else:
                cur=prev1
            prev2=prev1prev1=cur
        ans=max(ans,prev1)
    print(ans)
if __name__=="__main__":
    solve()


