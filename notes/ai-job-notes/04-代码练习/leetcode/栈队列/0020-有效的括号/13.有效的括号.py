import sys
s=input()
stack = []
mapping = {')': '(', '}': '{', ']': '['}

for char in s:
    if char in mapping:
                # 遇到右括号，检查栈顶
        top = stack.pop() if stack else '#'
        if mapping[char] != top:
            print (False)
            sys.exit()
    else:
                # 遇到左括号，入栈
         stack.append(char)

print(len(stack) == 0)