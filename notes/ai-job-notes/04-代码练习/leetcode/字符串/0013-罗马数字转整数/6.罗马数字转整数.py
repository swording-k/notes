
roman_map = {'I': 1, 'V': 5, 'X':10,'L':50,'C':100,'D':500,'M':1000}

s = input() 
sum=0

for i in range(0,len(s)):
    if i >0 and i<len(s)-1 and roman_map[s[i]] < roman_map[s[i +1]]:
       sum-=roman_map[s[i]]
    else :sum+=roman_map[s[i]]
print(sum)
