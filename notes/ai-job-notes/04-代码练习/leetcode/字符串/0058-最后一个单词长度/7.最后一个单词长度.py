s=input()
lens=0
for i in range(len(s)-1,0,-1):
    if s[i]==" "and lens!=0:
               print (lens)

    elif s[i]!=' ':lens+=1  
if s[0]==' ':print (lens)
else:print (lens+1)