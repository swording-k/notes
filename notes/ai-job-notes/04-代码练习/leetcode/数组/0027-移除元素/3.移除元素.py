
nums = list(map(int, input().split()))
val=int(input())
slow=0
k=0
for fast in range(0,len(nums)):
    if nums[fast]!=val:
       nums[slow]=nums[fast];
       slow+=1
       k+=1
print(k)
print(nums)

