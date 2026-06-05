s=input()
s1= ''.join(c.lower() for c in s if c.isalnum())
s2=s1[::-1]
if s1==s2:print('true')
else:print('false')