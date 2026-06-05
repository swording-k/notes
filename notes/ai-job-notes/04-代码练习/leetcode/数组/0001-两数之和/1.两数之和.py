nums = list(map(int, input().split()))
target=int(input())
for i in range(len(nums)):
    for j in range(0,i):
        if nums[i]+nums[j]==target:
            print(j,i)


