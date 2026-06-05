# Python刷题语法速查

> 专为有C基础的人准备，快速上手Python刷题

---

## 📋 详细目录

- [[#一、基础入门]]
  - [[#1-为什么python刷题不需要头文件]]
- [[#二、数据结构]]
  - [[#1-列表-list-刷题最常用的数据结构]]
    - [[#列表创建方式]]
    - [[#列表访问与切片]]
    - [[#列表常用操作表]]
    - [[#负索引从右往左数]]
    - [[#列表拷贝避免引用问题]]
    - [[#列表推导式pythonic写法]]
    - [[#二维数组矩阵]]
  - [[#2-字典dict-哈希表刷题神器]]
    - [[#字典创建与访问]]
    - [[#get-vs-直接访问]]
    - [[#统计出现次数]]
    - [[#字典常用操作表]]
  - [[#3-集合set-去重与快速查找]]
    - [[#集合创建与基本操作]]
    - [[#set的三大用途]]
    - [[#set-vs-list-查找速度对比]]
    - [[#set与list类型转换]] ← 新增
    - [[#sorted-vs-set-对比]] ← 新增
  - [[#4-字符串string-刷题高频]]
    - [[#字符串访问与切片]]
    - [[#字符串大小写]]
    - [[#字符判断回文串专用]]
    - [[#字符串查找分割]]
    - [[#字符串与列表转换]]
    - [[#字符串修剪去除空格]]
    - [[#字符串统计判断]]
    - [[#字符串反转]]
    - [[#生成器表达式-join高效连接]]
- [[#三、核心语法]]
  - [[#1-变量引用机制与c的区别]] ← 升级为独立章节
    - [[#基本原理]]
    - [[#cur-dummy-为什么改一个都变]]
    - [[#什么时候不联动]]
    - [[#可变对象-vs-不可变对象]]
    - [[#链表刷题常见坑]]
    - [[#对比总结表]]
  - [[#2-for循环]]
    - [[#range的三种用法]]
    - [[#从后往前遍历刷题常用]]
    - [[#for循环中修改循环变量无效]]
  - [[#3-while循环]]
  - [[#4-if条件判断]]
  - [[#5-类型转换]] ← 新增汇总
    - [[#数值转换]]
    - [[#容器类型转换]]
- [[#四、刷题输入输出]]
  - [[#1-单行输入]]
    - [[#map函数拆解]]
  - [[#2-多行输入]]
  - [[#3-字符数组输入]]
  - [[#4-二维数组输入]]
  - [[#5-sysstdinread-优化写法]]
  - [[#6-常用输出]]
- [[#五、常用函数速查表]] ← 新增汇总
  - [[#数学类函数]]
  - [[#排序类函数]] ← 强调 sorted
  - [[#字符串类函数]]
  - [[#其他常用函数]]
- [[#六、enumerate函数]]
- [[#七、map函数]]
- [[#八、刷题常见错误]]
  - [[#语法类错误]]
  - [[#引用类错误]]
  - [[#类型类错误]]
  - [[#循环类错误]]
- [[#九、代码模板]]
  - [[#模板1-两数之和哈希表]]
  - [[#模板2-统计频率]]
  - [[#模板3-双指针]]
  - [[#模板4-滑动窗口]]
- [[#十、刷题流程与模式]]
  - [[#leetcode函数模式-vs-acm模式]]

---

## 一、基础入门

### 1-为什么python刷题不需要头文件

```python
# C语言
#include <stdio.h>
#include <stdlib.h>

# Python
# 不需要！直接用
print("hello")
```

**原因**：Python的"标准库"都是内置的，用 `import` 按需引入即可。

---

## 二、数据结构

### 1-列表-list-刷题最常用的数据结构

> 列表 List（类似C数组），刷题中最常用的数据结构

#### 列表创建方式

```python
# 创建空列表
dp = []                 # ✅ 推荐，动态增长
dp = list()             # 也可以，但多余

# 创建固定长度列表（DP常用）
dp = [0] * 10           # 长度为10，全0数组 [0,0,0,0,0,0,0,0,0,0]
dp = [None] * 5         # 全None数组

# 创建二维列表
dp = [[0] * n for _ in range(m)]   # m×n 全0矩阵 ✅
dp = [[] for _ in range(m)]        # m个空列表

# ⚠️ 错误写法！[[0] * 3] * 3 三个行是同一引用
matrix = [[0] * 3] * 3  # ❌ 千万不要用！
```

#### 动态增长 vs 预分配

```python
# 方式1：动态增长（不确定长度时）
dp = []
for i in range(n):
    dp.append(i * 2)   # dp = [0, 2, 4, ...]

# 方式2：预分配（固定长度，按索引赋值）
dp = [0] * (n + 1)      # 常用于DP
dp[0] = 1
dp[1] = 1
```

#### 列表访问与切片

```python
nums = [1, 2, 3, 4, 5]

# 访问
nums[0]      # 第一个元素
nums[-1]     # 最后一个元素
nums[-2]     # 倒数第二个元素

# 切片（左闭右开）
nums[1:4]    # [2, 3, 4]
nums[:3]     # [1, 2, 3]
nums[2:]     # [3, 4, 5]
nums[:-1]    # [1, 2, 3, 4] - 去掉最后一个
nums[-2:]    # [4, 5] - 最后两个
```

#### 列表常用操作表

| 操作 | 代码 | 说明 |
|------|------|------|
| 添加 | `nums.append(x)` | 末尾添加，动态增长 |
| 删除 | `nums.pop()` | 末尾删除 |
| 插入 | `nums.insert(i, x)` | 索引i处插入 |
| 排序 | `nums.sort()` | 原地排序 |
| 反转 | `nums.reverse()` | 原地反转 |
| 长度 | `len(nums)` | 元素个数 |

#### 负索引从右往左数

```python
words = ['Hello', 'World']

words[0]     # 'Hello' - 第一个
words[1]     # 'World' - 第二个
words[-1]    # 'World' - 最后一个
words[-2]    # 'Hello' - 倒数第二个

# 常用场景
s = "Hello"
s[-1]        # 'o' - 最后一个字符
s[-2:]       # 'lo' - 最后两个字符
```

#### 列表拷贝避免引用问题

```python
# 浅拷贝问题
a = [1, 2, 3]
b = a           # ❌ 同一个引用，修改b会影响a
b.append(4)     # a也变成[1,2,3,4]

# 正确拷贝方式
b = a[:]        # ✅ 切片拷贝
b = list(a)     # ✅ 构造函数拷贝
b = a.copy()    # ✅ copy方法
```

#### 列表推导式pythonic写法

```python
# 生成新列表
squares = [x**2 for x in range(10)]   # [0,1,4,9,16,25,36,49,64,81]

# 带条件过滤
evens = [x for x in range(10) if x % 2 == 0]  # [0,2,4,6,8]

# 二维列表创建
dp = [[0] * n for _ in range(m)]  # ✅ 正确
```

#### 链式调用一行搞定

```python
s = "  Hello World  "

s.strip()              # "Hello World" - 去首尾空格
s.strip().split()     # ['Hello', 'World'] - 分割成列表
s.strip().split()[-1] # 'World' - 取最后一个单词
len(s.strip().split()[-1])  # 5 - 求长度

# 一行搞定：
print(len(s.strip().split()[-1]))  # 5
```

#### 二维数组矩阵

```python
# 创建 3x3 的二维数组（初始值为0）
matrix = [[0] * 3 for _ in range(3)]
# 结果：
# [[0, 0, 0],
#  [0, 0, 0],
#  [0, 0, 0]]

# ⚠️ 错误写法！
matrix = [[0] * 3] * 3  # 这样三个行是同一个引用！

# 访问元素
matrix[0][0]    # 第1行第1列
matrix[1][2]    # 第2行第3列

# 遍历二维数组
for i in range(3):
    for j in range(3):
        print(matrix[i][j])
```

---

### 2-字典dict-哈希表刷题神器

> 字典 Dict（哈希表，查重、统计必备）

#### 字典创建与访问

```python
# 创建空字典
count = {}

# 添加/修改
count[3] = 2        # count = {3: 2}
count[1] = 1        # count = {3: 2, 1: 1}

# 读取（防止报错）
count.get(3, 0)     # 如果没有key，返回0
```

#### get-vs-直接访问

```python
count = {'a': 1}

count['a']           # → 1，正常
count['b']           # → KeyError: 'b'，键不存在会报错！
count.get('b')       # → None，键不存在返回 None
count.get('b', 0)    # → 0，键不存在返回默认值 0
```

#### 统计出现次数

```python
# 用 get 避免键不存在报错
nums = [3, 1, 2, 3, 1]
count = {}
for num in nums:
    count[num] = count.get(num, 0) + 1

# 分解：
#   第一次 num=3: count.get(3,0) = 0, count[3] = 0+1 = 1
#   第二次 num=3: count.get(3,0) = 1, count[3] = 1+1 = 2
# 结果：{3: 2, 1: 2, 2: 1}
```

#### 字典常用操作表

| 操作 | 代码 | 说明 |
|------|------|------|
| 创建 | `d = {}` | 空字典 |
| 添加 | `d[key] = value` | 添加/修改 |
| 读取 | `d.get(key, default)` | 安全读取 |
| 判断 | `key in d` | key是否存在 |
| 删除 | `d.pop(key)` | 删除key |

---

### 3-集合set-去重与快速查找

> 集合 Set（去重 + 快速查找）

#### 集合创建与基本操作

```python
# 创建
nums = [1, 2, 2, 3, 3, 3]
unique = set(nums)  # {1, 2, 3}

# 空集合（注意：不能用 {}，那是空字典）
empty_set = set()    # set()
# empty_dict = {}     # dict，不是 set！

# 添加元素
s = {1, 2, 3}
s.add(4)             # {1, 2, 3, 4}

# 删除元素
s.remove(2)          # {1, 3, 4}  （元素不存在会报错）
s.discard(2)         # {1, 3, 4}  （元素不存在不报错）

# 判断元素是否存在（O(1) 速度！）
s = {1, 2, 3}
print(2 in s)        # True
print(5 in s)        # False
```

#### set的三大用途

| 用途 | 示例 | 说明 |
|------|------|------|
| **去重** | `set([1,2,2,3])` → `{1,2,3}` | 自动去除重复 |
| **快速查找** | `if x in set_x` | O(1) 判断是否存在 |
| **集合运算** | `a & b`（交集）, `a \| b`（并集） | 数学集合操作 |

#### set-vs-list-查找速度对比

```python
# list 查找：O(n) 逐个比较
nums = [1, 2, 3, 4, 5]
print(3 in nums)  # 慢！要检查每个元素

# set 查找：O(1) 哈希定位
s = {1, 2, 3, 4, 5}
print(3 in s)     # 快！直接计算哈希定位
```

**刷题中什么时候用 set？**
- 题目问"是否存在重复" → set
- 题目问"某个元素在不在集合里" → set
- 简单去重 → set

#### set与list类型转换

```python
# list → set（去重）
nums = [1, 2, 2, 3, 3]
s = set(nums)      # {1, 2, 3}

# set → list（必须转！set不是序列）
lst = list(s)     # [1, 2, 3]  ⚠️ 必须转！set不是list

# ⚠️ 常见错误：以为 set 可以直接用下标访问
s = {1, 2, 3}
print(s[0])        # ❌ TypeError: 'set' object is not subscriptable
print(list(s)[0])  # ✅ 1 - 先转成 list 就能下标访问了
```

#### sorted-vs-set-对比

> 重要！这两个经常搭配使用

```python
nums = [3, 1, 2, 3, 1]

# sorted() - 直接返回列表，不需要转
a = sorted(nums)      # [1, 1, 2, 3, 3]  ✅ 类型是 list
print(type(a))        # <class 'list'>

# set() - 返回集合，必须转 list 才能下标访问
b = set(nums)         # {1, 2, 3}  ⚠️ 类型是 set
print(type(b))        # <class 'set'>

# 常见组合：去重 + 排序
c = sorted(set(nums)) # [1, 2, 3]  ✅ 先去重后排序，返回列表
```

| 函数 | 返回类型 | 需要转 list 吗？ | 说明 |
|------|----------|------------------|------|
| `sorted(x)` | **list** | ❌ 否 | 对可迭代对象排序 |
| `set(x)` | **set** | ✅ 是 | 去重，返回集合 |
| `list(x)` | **list** | ❌ 否 | 转成列表 |

---

### 4-字符串string-刷题高频

> 字符串 String（刷题高频！）

#### 字符串访问与切片

```python
s = "Hello World"

# 访问字符
s[0]        # 'H'
s[-1]       # 'd'

# 切片（左闭右开）
s[0:5]      # 'Hello'
s[6:]       # 'World'

# 长度
len(s)      # 11

# ⚠️ 越界会报错！不会像C一样访问任意内存
# s[100] → IndexError: string index out of range
```

#### 字符串大小写

```python
"Hello".lower()    # → "hello"
"abc".upper()      # → "ABC"
```

#### 字符判断回文串专用

```python
c = 'A'
c.isalpha()   # True - 是否是字母
c.isdigit()   # False - 是否是数字
c.isalnum()   # True - 是否是字母或数字
c.isupper()   # True - 是否是大写
c.islower()   # False - 是否是小写
```

#### 字符串查找分割

```python
s = "Hello World"
s.split()        # ['Hello', 'World'] - 按空格分割
s.replace("H", "J")  # 'Jello World' - 替换
s.find("World") # 6 - 找不到返回 -1
```

#### 字符串与列表转换

```python
list("abc")       # ['a', 'b', 'c'] - 字符串转列表（每个字符拆分）
"".join(['a','b'])  # 'ab' - 列表转字符串（字符拼接）

# ===== sorted() 与 join() 的组合 =====
s = "eat"
sorted(s)          # ['e', 'a', 't'] - sorted 字符串返回字符列表！
"".join(sorted(s)) # "eat" - 先排序，再合并成字符串

# 常见用法：让字母异位词有相同的 key
# "eat", "tea", "ate" 排序后都是 "aet"
```

**常见错误**：
```python
s = "abc"
s.sort()  # ❌ 报错！字符串没有 sort() 方法
sorted(s)  # ✅ 正确，返回列表
```

#### 字符串修剪去除空格

```python
s = "  Hello World  "

s.strip()       # "Hello World" - 去掉首尾空格
s.lstrip()      # "Hello World  " - 只去左边
s.rstrip()      # "  Hello World" - 只去右边

# 刷题常用：去除首尾空格后分割
s = "   hello world   "
words = s.strip().split()  # ['hello', 'world']
```

#### 字符串统计判断

```python
s = "Hello World"

s.count('l')          # 3 - 统计字符出现次数
s.startswith('He')    # True - 是否以某字符串开头
s.endswith('ld')      # True - 是否以某字符串结尾
s.isdigit()           # False - 是否全是数字
s.isalpha()           # False - 是否全是字母
s.isspace()           # False - 是否全是空格
```

#### 字符串反转

```python
s = "Hello"
s[::-1]               # "olleH" - 反转字符串，超简洁！
```

#### 列表原地反转leetcode-专用

```python
lst = ['h','e','l','l','o']

# ❌ 错误：s1 = lst[::-1] 创建新列表，原列表不变！
s1 = lst[::-1]        # s1 是新列表，lst 不变

# ✅ 正确方法1：reverse() 原地反转
lst.reverse()          # lst 变成 ['o','l','l','e','h']

# ✅ 正确方法2：切片赋值写回
lst[:] = lst[::-1]    # 把反转后的内容写回原列表
```

**LeetCode 函数模式必须用 `s.reverse()`！** 不能创建新列表。

#### 生成器表达式-join高效连接

```python
s = "A man, a plan, a canal: Panama"

# 筛选字母并转小写后连接
cleaned = ''.join(c.lower() for c in s if c.isalnum())
# 分解：
# 1. (c.lower() for c in s if c.isalnum()) - 生成器
# 2. ''.join(...) - 用空字符串连接
```

---

## 三、核心语法

### 1-变量引用机制与c的区别

> **核心概念：Python没有"变量"，只有"名字标签"**
>
> Python的变量更像是"贴标签"，C的指针是"地址值复制"

#### 基本原理

```python
# C语言：两个独立的指针变量，各存一份地址
Node *cur = &dummy;    // cur和dummy是独立的指针，指向同一节点

# Python：两个名字指向同一个对象
cur = dummy            # cur和dummy是同一个对象的两个标签
```

**图示：**
```
Python的标签模型：
    dummy ──→ [节点A] ←── cur
              (同一个对象)

C的指针模型：
    dummy ──→ [节点A]      cur ──→ [节点A]
              (两个节点副本，地址相同)
```

#### cur-dummy-为什么改一个都变

```python
dummy = ListNode(0)   # 创建节点
cur = dummy           # cur 和 dummy 现在是同一个节点的"两个名字"

print(cur is dummy)   # True —— 是同一个对象
print(id(cur))         # 相同地址
print(id(dummy))

cur.val = 99           # 修改节点属性
print(dummy.val)      # 99 —— dummy也看到了变化
```

**原因**：`cur = dummy` 不是"复制节点"，而是"让cur也指向dummy指向的节点"。

#### 什么时候不联动

```python
cur = dummy
cur = cur.next        # cur 重新指向别的对象

cur.val = 100         # 只改 cur 指向的对象
print(dummy.val)      # 还是 99，dummy没变
```

**关键**：`cur = cur.next` 是"让cur指向新节点"，而不是"修改节点"。

#### 可变对象-vs-不可变对象

| 类型 | 示例 | 能否修改内容 |
|------|------|-------------|
| **不可变** | int, str, tuple | 不能改，只能重新赋值 |
| **可变** | list, dict, set | 可以改内容 |

```python
# 不可变对象 - 真的改不了
a = 5
def try_modify(x):
    x = 10  # 只是局部变量x重新指向10，不影响a
try_modify(a)
print(a)  # 仍然是 5

# 可变对象 - 真的能改
b = [1, 2, 3]
def try_modify_list(lst):
    lst.append(4)  # 修改的是同一个list对象
try_modify_list(b)
print(b)  # [1, 2, 3, 4]
```

#### 链表刷题常见坑

```python
# 错误：以为重新赋值会修改链表
def remove_middle_wrong(head):
    cur = head
    cur = cur.next  # 这只是让cur指向下一个，原链表不变

# 正确：原地修改
def remove_middle_right(head):
    cur = head
    cur.next = cur.next.next  # 修改的是节点的next属性
```

#### 对比总结表

| 操作 | C | Python |
|------|---|--------|
| 赋值给另一个变量 | `b = a` 复制地址 | `b = a` 共享对象 |
| 修改指向 | `b = b->next` | `b = b.next` |
| 修改内容 | `b->val = 5` | `b.val = 5` |
| 断开连接 | `b = NULL` | `b = None` |

**记住**：Python没有指针，只有"引用"（对象的另一个名字）

---

### 2-for循环

> for循环

```python
# 基本遍历
for i in range(10):      # 0, 1, 2, ..., 9
    print(i)

for i in range(1, 10):  # 1, 2, ..., 9

# 遍历列表
nums = [1, 2, 3]
for num in nums:
    print(num)

# 带索引遍历
for i, num in enumerate(nums):
    print(f"{i}: {num}")
```

#### range的三种用法

```python
# 1. range(stop) - 从 0 开始
for i in range(5):       # 0, 1, 2, 3, 4

# 2. range(start, stop) - 左闭右开
for i in range(2, 5):    # 2, 3, 4

# 3. range(start, stop, step) - 带步长，可正可负
for i in range(0, 10, 2):   # 0, 2, 4, 6, 8  （正序）
for i in range(5, 0, -1):   # 5, 4, 3, 2, 1  （倒序）
```

#### 从后往前遍历刷题常用

```python
# 错误写法：range(len-1, 0) 不包含 0！
digits = [1, 2, 3]
for i in range(len(digits) - 1, 0):
    print(i)
# 输出: 2, 1  （漏掉了索引 0！）

# 正确写法：range(len-1, -1, -1) 包含 0
digits = [1, 2, 3]
for i in range(len(digits) - 1, -1, -1):
    print(i)
# 输出: 2, 1, 0  ✓
```

**为什么用 -1？**
- `range` **不包含 stop**（容易错的点！）
- `range(len-1, -1, -1)` 中的 `-1` 是 stop 参数，表示"包含索引 0"
- 等价于 `range(2, -1, -1)` → 生成 `[2, 1, 0]`

#### for循环中修改循环变量无效

```python
# ❌ 错误：想在循环里跳过元素
for i in range(5):
    i = 999  # 改了也没用，下次循环还是按 range 给的值
    print(i)
# 输出: 999, 1, 2, 3, 4

# ✅ 正确：跳过用 continue
for i in range(5):
    if i == 2:
        continue  # 跳过 i==2
    print(i)
# 输出: 0, 1, 3, 4
```

---

### 3-while循环

> while循环

```python
i = 0
while i < 10:
    print(i)
    i += 1  # 注意：没有 i++
```

---

### 4-if条件判断

> if条件

```python
if x > 0:
    print("正数")
elif x < 0:
    print("负数")
else:
    print("零")
```

---

### 5-类型转换

> 常用类型转换汇总

#### 数值转换

```python
int("123")         # 字符串 → 整数
float("3.14")       # 字符串 → 浮点数
str(123)           # 整数 → 字符串
abs(-5)            # 绝对值
```

#### 容器类型转换

```python
# list ↔ set
list(set([1,2,2,3]))   # list转set去重，再转回list
set([1,2,3])           # list转set

# str ↔ list
list("abc")            # "abc" → ['a', 'b', 'c']  按字符拆分
"".join(['a','b'])    # ['a','b'] → "ab"           拼接

# sorted() - 返回列表（不需要再转）
sorted([3,1,2])        # [1, 2, 3]  ✅ 返回list
sorted("bac")          # ['b', 'a', 'c'] ✅ 返回list
sorted({3,1,2})        # [1, 2, 3]  ✅ 对set排序也返回list

# ⚠️ 注意：set 没有 sort() 方法！
s = {3, 1, 2}
s.sort()               # ❌ AttributeError: 'set' object has no attribute 'sort'
sorted(s)              # ✅ [1, 2, 3]  用 sorted()
```

---

## 四、刷题输入输出

### 1-单行输入

```python
# 单个整数
n = int(input())                    # 输入: 5

# 一行整数数组（空格分隔）
nums = list(map(int, input().split()))   # 输入: 1 2 3 4 5 → [1,2,3,4,5]

# 一行字符串（空格分隔）
a, b = input().split()             # 输入: hello world → 'hello', 'world'

# 字符串转整数数组
nums = [int(x) for x in input().split()]  # 另一种写法
```

#### map函数拆解

```python
# 拆解: nums = list(map(int, input().split()))
input().split()        # → ['1', '2', '3']    字符串列表
map(int, ['1','2','3']) # → map对象(1, 2, 3)    整数迭代器
list(...)              # → [1, 2, 3]           转成列表
```

---

### 2-多行输入

```python
# 已知n行
n = int(input())
for _ in range(n):
    row = list(map(int, input().split()))
    matrix.append(row)

# 示例输入：
# 3
# 1 2 3
# 4 5 6
# 7 8 9
# matrix = [[1,2,3], [4,5,6], [7,8,9]]
```

---

### 3-字符数组输入

```python
# 字符用空格分隔
chars = list(input().split())   # 输入: a b c d e → ['a','b','c','d','e']

# 整行作为一个字符串（不带split）
s = input().strip()            # 输入: abcde → 'abcde'
```

---

### 4-二维数组输入

```python
# m行 n列矩阵
m, n = map(int, input().split())
matrix = []
for _ in range(m):
    row = list(map(int, input().split()))
    matrix.append(row)
```

---

### 5-sysstdinread-优化写法

```python
# 一次性读取所有输入，打平为列表
data = sys.stdin.read().strip().split()

# 等价于（但更简洁，适合不确定行数时）
data = input().split()  # 只有一行时

# 实际效果：
# 输入: 1 2 3\n4 5 6\n
# data = ['1', '2', '3', '4', '5', '6']  ← 全打平了

# 读取为整数数组
nums = list(map(int, sys.stdin.read().split()))
```

---

### 6-常用输出

```python
print("hello")              # 打印字符串
print(123)                  # 打印数字
print(a, b, c)              # 打印多个，空格分隔
print(f"{a} + {b} = {c}")   # f-string格式化
print(*result)              # 解包列表输出
```

---

## 五、常用函数速查表

> 刷题中最常用的内置函数

### 数学类函数

```python
max(nums)          # 最大值
min(nums)          # 最小值
sum(nums)          # 求和
abs(-5)            # 绝对值
float('inf')       # 正无穷（用于DP初始化）
float('-inf')      # 负无穷

# ⚠️ 需要 import math 的函数
import math
math.sqrt(4)       # 平方根
math.pi            # 圆周率
math.floor(3.5)    # 向下取整
math.ceil(3.2)     # 向上取整
```

### 排序类函数

```python
nums = [3, 1, 2]

# 原地排序（修改原列表）
nums.sort()        # [1, 2, 3] - nums 本身被修改

# 返回新列表（原列表不变）
nums = [3, 1, 2]
a = sorted(nums)   # [1, 2, 3] - nums 不变，a 是新列表

# 对 set 排序（sorted 返回 list，set 没有 sort 方法）
s = {3, 1, 2}
sorted(s)          # [1, 2, 3]  ✅ 返回 list
# s.sort()          # ❌ 报错！set 没有 sort

# 对字符串排序
sorted("bac")      # ['b', 'a', 'c'] - 返回字符列表
"".join(sorted("bac"))  # "abc" - 排序后拼接
```

### 字符串类函数

```python
s = "Hello"

# 大小写
s.lower()         # "hello"
s.upper()         # "HELLO"

# 字符判断
c.isalpha()       # 是否是字母
c.isdigit()       # 是否是数字
c.isalnum()       # 是否是字母或数字
c.isupper()       # 是否是大写
c.islower()       # 是否是小写

# 查找/替换
s.find("ll")      # 2 - 找不到返回 -1
s.replace("ll", "xx")  # "Hexxo"
s.split()         # ['Hello'] - 按空格分割
"-".join(['a','b'])  # "a-b" - 用连接符合并

# 修剪
s.strip()         # 去除首尾空格
s.lstrip()        # 只去左边
s.rstrip()        # 只去右边

# 统计
s.count('l')      # 3 - 字符出现次数
s.startswith('He')   # True - 是否以某字符串开头
s.endswith('ld')      # True - 是否以某字符串结尾
```

### 其他常用函数

```python
# enumerate - 同时获取索引和值
for i, val in enumerate(nums):
    print(f"{i}: {val}")

# len - 获取长度
len(nums)          # 列表长度
len(s)            # 字符串长度

# type - 查看类型
type(123)         # <class 'int'>
type([1,2])       # <class 'list'>
type({1,2})       # <class 'set'>
```

---

## 六、enumerate函数

> enumerate = 同时获取「索引」和「值」

```python
# 同时获取「索引」和「值」
nums = ['a', 'b', 'c']
for i, num in enumerate(nums):
    print(f"{i}: {num}")
# 输出：
# 0: a
# 1: b
# 2: c

# 等价于：
for i in range(len(nums)):
    num = nums[i]
    print(f"{i}: {num}")
```

**刷题中的用法**：
```python
# 找值为x的元素下标
for i, num in enumerate(nums):
    if num == target:
        print(i)
```

---

## 七、map函数

> map = 对每个元素做同样的操作

```python
# map(函数, 列表) = 对每个元素做同样的操作

# 拆解这行代码：
nums = list(map(int, input().split()))

# input()        → "1 2 3"
# input().split() → ["1", "2", "3"]  （字符串列表）
# map(int, ...)   → 逐个转整数
# list(...)       → 转回列表

# 常用场景：
list(map(int, ["1", "2", "3"]))      # → [1, 2, 3]
```

---

## 八、刷题常见错误

### 语法类错误

| 错误写法 | 正确写法 | 说明 |
|----------|----------|------|
| `for i in range(10)` | `for i in range(10):` | 缺冒号 |
| `if x > 0 { }` | `if x > 0:` | 用冒号，不用花括号 |
| `i++` | `i += 1` | Python没有++ |
| `a = input()` 然后 `a + 1` | `a = int(input())` | 类型转换 |
| `arr = array[]` | `arr = []` | 空列表 |

### 引用类错误

```python
# 二维数组拷贝问题
matrix = [[0]*3]*3  # ❌ 三个行是同一个引用
matrix = [[0]*3 for _ in range(3)]  # ✅ 正确

# 列表浅拷贝问题
b = a           # ❌ 同一个引用
b = a[:]        # ✅ 切片拷贝
```

### 类型类错误

```python
# 字符串没有 sort() 方法
s = "abc"
s.sort()        # ❌ 报错
sorted(s)       # ✅ 正确，返回列表

# set 没有 sort() 方法
s = {1, 2, 3}
s.sort()        # ❌ 报错
sorted(s)       # ✅ 正确

# 字符串不能用 + 拼接数字
s = "abc" + 1   # ❌ 报错
s = "abc" + str(1)  # ✅ "abc1"
```

### 循环类错误

```python
# for 循环修改循环变量无效
for i in range(5):
    i = 999  # ❌ 改了也没用
    i += 1   # ❌ 也是无用功

# 从后往前漏掉 0
for i in range(2, 0):    # ❌ 输出 2, 漏掉 0
for i in range(2, -1, -1): # ✅ 2, 1, 0

# 空集合不能用 {}
empty_set = {}     # ❌ 这是空字典！
empty_set = set()  # ✅ 这是空集合
```

---

## 九、代码模板

### 模板1-两数之和哈希表

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

### 模板2-统计频率

```python
def count_frequency(nums):
    freq = {}
    for num in nums:
        freq[num] = freq.get(num, 0) + 1
    return freq
```

### 模板3-双指针

```python
def two_pointer(nums):
    left = 0
    right = len(nums) - 1
    while left < right:
        # 处理逻辑
        left += 1
        right -= 1
    return result
```

### 模板4-滑动窗口

```python
def sliding_window(nums, k):
    left = 0
    window_sum = 0
    result = 0

    for right in range(len(nums)):
        window_sum += nums[right]

        # 窗口收缩条件
        while window_sum > k and left <= right:
            window_sum -= nums[left]
            left += 1

        # 更新结果
        result = max(result, right - left + 1)

    return result
```

---

## 十、刷题流程与模式

### leetcode函数模式-vs-acm模式

| ACM模式 | LeetCode模式 |
|---------|--------------|
| `input()` | 参数传入 |
| `print()` | `return` |
| 完整程序 | class + 方法 |
| `if __name__ == "__main__"` | 不需要 |

```python
# ==================== LeetCode函数模式 ====================
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            if target - num in seen:
                return [seen[target - num], i]
            seen[num] = i

# ==================== ACM完整程序模式 ====================
import sys

class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, num in enumerate(nums):
            if target - num in seen:
                return [seen[target - num], i]
            seen[num] = i
        return []

if __name__ == "__main__":
    nums = list(map(int, input().split()))
    target = int(input())
    sol = Solution()
    print(*sol.twoSum(nums, target))
```

---

## 📌 结论

```
Python刷算法题，只需要掌握：

✅ 列表 list       - 存数据
✅ 字典 dict       - 哈希表，查重、统计
✅ 集合 set        - 去重（注意：不是序列，需要 list() 转）
✅ 字符串          - 切片、分割、查找
✅ 二维列表        - 矩阵、棋盘
✅ for/while循环   - 遍历
✅ if条件判断      - 选择
✅ 常用函数        - max/min/sum/sorted/enumerate/map

⚠️ 特别注意：
- sorted() 返回 list，不需要再转
- set() 返回 set，需要 list(set()) 才能下标访问
- set 没有 sort() 方法，用 sorted(set())

❌ 不需要：类、继承、文件IO、多线程
❌ 不需要：NumPy、Pandas（刷题用不到）
```

**看完这个，明天直接刷题！**
