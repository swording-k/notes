# LeetCode 412. Fizz Buzz

## 题目链接
https://leetcode.cn/problems/fizz-buzz/

## 题目描述
给你一个整数 n，从 1 到 n 按照下面的规则打印：
- 如果 n 能被 3 整除，打印 "Fizz"
- 如果 n 能被 5 整除，打印 "Buzz"
- 如果 n 能同时被 3 和 5 整除，打印 "FizzBuzz"
- 否则，打印 n 本身（数字）

## 示例
```
示例 1：
输入：n = 3
输出：["1", "2", "Fizz"]

示例 2：
输入：n = 5
输出：["1", "2", "Fizz", "4", "Buzz"]

示例 3：
输入：n = 15
输出：["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]
```

## 提示
- 1 ≤ n ≤ 10⁴

## 解题思路

### 方法1：简单模拟 O(n) ✅
```python
class Solution:
    def fizzBuzz(self, n: int) -> list[str]:
        result = []
        for i in range(1, n + 1):
            if i % 15 == 0:        # 先判断 15 的倍数
                result.append("FizzBuzz")
            elif i % 3 == 0:
                result.append("Fizz")
            elif i % 5 == 0:
                result.append("Buzz")
            else:
                result.append(str(i))
        return result
```

### 方法2：字符串拼接（扩展性强）
```python
class Solution:
    def fizzBuzz(self, n: int) -> list[str]:
        result = []
        for i in range(1, n + 1):
            s = ""
            if i % 3 == 0:
                s += "Fizz"
            if i % 5 == 0:
                s += "Buzz"
            result.append(s if s else str(i))
        return result
```
**优点**：如果再加一个 "Jazz"（能被 7 整除），方法 2 更容易扩展

### 核心思想
- 简单的条件判断题
- 注意判断顺序：先判断 15，再判断 3 和 5
- 也可以用字符串拼接，代码更灵活

## 代码实现

### LeetCode 函数模式
```python
class Solution:
    def fizzBuzz(self, n: int) -> list[str]:
        result = []
        for i in range(1, n + 1):
            if i % 15 == 0:
                result.append("FizzBuzz")
            elif i % 3 == 0:
                result.append("Fizz")
            elif i % 5 == 0:
                result.append("Buzz")
            else:
                result.append(str(i))
        return result
```

### ACM 模式
```python
def fizz_buzz(n: int) -> list[str]:
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result

if __name__ == "__main__":
    n = int(input().strip())
    result = fizz_buzz(n)
    print('[' + ', '.join(f'"{s}"' for s in result) + ']')
```

## 复杂度分析
- **时间复杂度**：O(n)
- **空间复杂度**：O(n)

## 关联