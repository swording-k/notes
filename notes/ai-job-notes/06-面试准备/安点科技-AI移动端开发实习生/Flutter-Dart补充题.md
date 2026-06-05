# Flutter & Dart 面试补充题库

> 基于2024-2025年真实面试题整理

---

## 一、Dart 语言核心问题

### Q1: Dart 是值传递还是引用传递？

```dart
✅ 参考答案：
"Dart是值传递。每次调用函数，传递的都是对象的引用（内存地址），而不是对象的拷贝。

但要注意：
- 原始类型（int、String、bool）传递的是值
- 对象类型传递的是引用副本

示例1（基础类型）：
void main() {
  int x = 1;
  fun(x);
  print(x); // 输出：1
}
void fun(int x) {
  x = 2; // 修改的是副本
}

示例2（对象类型）：
void main() {
  List<int> list = [1, 2, 3];
  fun(list);
  print(list); // 输出：[1, 2, 3, 4]
}
void fun(List<int> list) {
  list.add(4); // 修改的是同一个对象
}"
```

---

### Q2: Dart 中的 var、dynamic、const、final 区别？

```dart
✅ 参考答案：
"┌──────────┬──────────────────┬──────────────────┐
│ 关键字   │ 类型推断         │ 赋值后能否修改   │
├──────────┼──────────────────┼──────────────────┤
│ var      │ 编译时推断       │ 能（重新赋值）   │
│ dynamic   │ 运行时不检查     │ 能              │
│ final     │ 运行时常量       │ 不能            │
│ const     │ 编译时常量       │ 不能            │
└──────────┴──────────────────┴──────────────────┘

详细说明：

1️⃣ var：
   var x = 1;  // 推断为int
   x = 2;      // 可以重新赋值

2️⃣ dynamic：
   dynamic y = 1;
   y = "hello"; // 编译时不报错，运行时不报错
   // 相当于放弃了类型检查

3️⃣ final vs const：
   final now = DateTime.now(); // 正确，运行时常量
   const now2 = DateTime.now(); // 错误，编译时常量

   final List a = [1, 2]; // 可以修改列表内容
   a.add(3); // 正确
   a = [4, 5]; // 错误，不能重新赋值

   const List b = [1, 2]; // 内容也不能改"
```

---

### Q3: Dart 的 ?? 和 ??= 操作符？

```dart
✅ 参考答案：
"┌─────────────┬────────────────────────────────┐
│ 操作符      │ 含义                           │
├─────────────┼────────────────────────────────┤
│ ??          │ 空则取右边值                    │
│ ??=         │ 空则赋值                        │
└─────────────┴────────────────────────────────┘

1️⃣ ?? (空合并运算符)：
   String a;
   String b = a ?? "默认值"; // b = "默认值"

   // 等价于
   String b = a == null ? "默认值" : a;

2️⃣ ??= (空赋值运算符)：
   String a; // null
   a ??= "默认值"; // a = "默认值"

   // 等价于
   if (a == null) {
     a = "默认值";
   }"
```

---

### Q4: Dart 的 Mixin 是什么？

```dart
✅ 参考答案：
"Dart支持Mixin，可以达到"多继承"的效果：

Mixin的特点：
1. 只能继承自Object，不能继承其他类
2. 不能有构造函数
3. 一个类可以mix多个mixin

示例：
mixin Flyable {
  void fly() => print("I can fly!");
}

mixin Swimmable {
  void swim() => print("I can swim!");
}

class Duck with Flyable, Swimmable {
  void quack() => print("Quack!");
}

void main() {
  Duck duck = Duck();
  duck.fly();  // 来自Flyable
  duck.swim(); // 来自Swimmable
  duck.quack();// 来自Duck
}

限制：Mixin的类只能继承自Object"
```

---

### Q5: Dart 的异步编程：Future 和 Stream？

```dart
✅ 参考答案：
"1️⃣ Future：单次异步操作

Future<String> getData() async {
  await Future.delayed(Duration(seconds: 1));
  return "数据";
}

// 使用
getData().then((data) => print(data));
// 或
String data = await getData();

2️⃣ Stream：多次异步事件流

Stream<int> countStream() async* {
  for (int i = 1; i <= 3; i++) {
    await Future.delayed(Duration(seconds: 1));
    yield i; // 产生数据
  }
}

// 使用
await for (var value in countStream()) {
  print(value); // 1, 2, 3
}

// 常用方法
stream.listen((data) {...});    // 监听
stream.first;                   // 第一个元素
stream.where((x) => x > 1);     // 过滤
stream.map((x) => x * 2);       // 转换
stream.take(5);                 // 取前5个
stream.skip(2);                 // 跳过前2个"
```

---

### Q6: async/await 的原理？

```dart
✅ 参考答案：
"async/await 是语法糖，编译后变成Future链式调用：

// 源代码
Future<void> fetchData() async {
  var data = await getUser();
  var profile = await getProfile(data);
  print(profile);
}

// 编译后等价于
Future<void> fetchData() {
  return getUser().then((data) {
    return getProfile(data);
  }).then((profile) {
    print(profile);
  });
}

注意：
- await只能在async函数中使用
- await会暂停当前协程，等待完成后继续
- 不阻塞其他代码执行"
```

---

## 二、Flutter 核心问题

### Q7: Widget、Element、RenderObject 关系？

```dart
✅ 参考答案：
"三层架构：

┌───────────────┐
│   Widget      │ ← 配置信息（不可变）
│   (配置层)     │
└───────┬───────┘
        │ 创建
        ▼
┌───────────────┐
│   Element      │ ← 实例化对象（可变）
│   (中间层)     │
└───────┬───────┘
        │ 更新
        ▼
┌───────────────┐
│ RenderObject   │ ← 真正渲染（布局+绘制）
│   (渲染层)     │
└───────────────┘

关键点：
1. Widget是不可变的"蓝图"
2. 状态变化时创建新Widget
3. Element比较新旧Widget，决定是否更新RenderObject
4. RenderObject负责真正的布局和绘制

性能优化原理：
- Widget重新创建很快（只是对象）
- Element比较是增量更新
- 只重绘变化的部分"
```

---

### Q8: StatefulWidget 和 StatelessWidget 区别？

```dart
✅ 参考答案：
"┌─────────────────┬──────────────────┬──────────────────┐
│                 │  StatelessWidget  │ StatefulWidget   │
├─────────────────┼──────────────────┼──────────────────┤
│ 状态            │ 不可变           │ 可变             │
│ 刷新方式        │ 父组件重建       │ setState         │
│ 性能            │ 更高             │ 稍低             │
│ 使用场景        │ 静态UI           │ 动态交互         │
└─────────────────┴──────────────────┴──────────────────┘

StatelessWidget示例：
class MyText extends StatelessWidget {
  final String text; // 不可变

  @override
  Widget build(BuildContext context) {
    return Text(text);
  }
}

StatefulWidget示例：
class Counter extends StatefulWidget {
  @override
  _CounterState createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int count = 0; // 可变状态

  void increment() {
    setState(() { // 触发重建
      count++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('$count'),
        ElevatedButton(onPressed: increment, child: Text('+'))
      ],
    );
  }
}"
```

---

### Q9: Flutter 的状态管理方案？

```dart
✅ 参考答案：
"主流方案对比：

┌────────────┬──────────┬──────────────┬─────────────────┐
│ 方案       │ 复杂度   │ 适用场景     │ 官方推荐度      │
├────────────┼──────────┼──────────────┼─────────────────┤
│ setState   │ 低       │ 简单页面     │ ★★★★★          │
│ Provider   │ 中       │ 中小型应用   │ ★★★★☆（官方） │
│ Riverpod   │ 中高     │ 中大型应用   │ ★★★★☆          │
│ GetX       │ 中       │ 快速开发     │ ★★★☆☆          │
│ BLoC       │ 高       │ 大型团队     │ ★★★☆☆          │
└────────────┴──────────┴──────────────┴─────────────────┘

Provider示例：
class Counter extends ChangeNotifier {
  int _count = 0;
  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();
  }
}

// 使用
ChangeNotifierProvider(
  create: (_) => Counter(),
  child: Consumer<Counter>(
    builder: (_, counter, __) => Text('${counter.count}'),
  ),
)

GetX示例（最简单）：
GetxController controller = GetxController();
Get.put(controller);
// 使用：Obx(() => Text('${controller.count}'))"
```

---

### Q10: Flutter 的 Key 有什么作用？

```dart
✅ 参考答案：
"Key是Widget、Element、SemanticsNode的标识符

分类：
┌────────────┬────────────────────────────┐
│ 类型       │ 用途                       │
├────────────┼────────────────────────────┤
│ LocalKey   │ 同一层级的Widget比较       │
│  └ ValueKey│ 用具体值标识                │
│  └ ObjectKey│ 用对象标识                 │
├────────────┼────────────────────────────┤
│ GlobalKey  │ 跨层级获取State            │
│  └ LabeledGB│ 带标签                    │
│  └ UniqueGB│ 自动生成唯一ID             │
└────────────┴────────────────────────────┘

使用场景：

1️⃣ ValueKey（最常用）：
   ListView中重新排序时保持状态
   ListTile(key: ValueKey(item.id), ...)

2️⃣ GlobalKey（获取子组件状态）：
   final key = GlobalKey<ScaffoldState>();
   Scaffold(key: key, ...);
   key.currentState!.openDrawer(); // 打开抽屉"
```

---

### Q11: Flutter 如何处理网络请求？

```dart
✅ 参考答案：
"常用方案：

1️⃣ http包（基础）：
   import 'package:http/http.dart' as http;

   var response = await http.get(Uri.parse('https://api.example.com'));
   var data = jsonDecode(response.body);

2️⃣ dio包（推荐，功能强大）：
   import 'package:dio/dio.dart';

   final dio = Dio();
   final response = await dio.get('/users');

   // 拦截器
   dio.interceptors.add(LogInterceptor());

   // 请求拦截
   dio.interceptors.add(InterceptorsWrapper(
     onRequest: (options, handler) {
       options.headers['Authorization'] = 'Bearer token';
       handler.next(options);
     },
   ));

3️⃣ 错误处理：
   try {
     final response = await dio.get('/data');
   } on DioException catch (e) {
     if (e.type == DioExceptionType.connectionTimeout) {
       // 超时处理
     }
   }

4️⃣ Flutter AI项目中：
   - 使用openai或flutter_openai库
   - 处理流式输出（SSE）
   - 缓存策略"
```

---

### Q12: Flutter 的热重载原理？

```dart
✅ 参考答案：
"热重载基于JIT编译（开发模式）：

┌─────────────────────────────────────────┐
│           Flutter 热重载流程            │
├─────────────────────────────────────────┤
│                                         │
│  1. 修改Dart代码                        │
│           ↓                              │
│  2. 增量编译（只编译变化的文件）         │
│           ↓                              │
│  3. 发送 hot-reload 信号给VM             │
│           ↓                              │
│  4. VM更新代码                           │
│           ↓                              │
│  5. Flutter重建Widget树                  │
│           ↓                              │
│  6. 保留当前页面状态                      │
│                                         │
└─────────────────────────────────────────┘

热重载 vs 热重启：
- 热重载：代码变更，状态保留（UI重建）
- 热重启：状态丢失，重新运行APP

注意：
- 状态修改（setState）可以用热重载
- 修改main()或修改静态成员需要热重启"
```

---

### Q13: Flutter 的路由管理？

```dart
✅ 参考答案：
"1️⃣ Navigator 1.0（基础）：
   Navigator.push(
     context,
     MaterialPageRoute(builder: (_) => SecondPage()),
   );

2️⃣ Navigator 2.0（声明式，复杂）：
   - RouterDelegate
   - RouteInformationParser
   - 适合深层嵌套路由

3️⃣ go_router（推荐，Google官方）：
   import 'package:go_router/go_router.dart';

   final router = GoRouter(
     routes: [
       GoRoute(
         path: '/',
         builder: (context, state) => HomePage(),
       ),
       GoRoute(
         path: '/user/:id',
         builder: (context, state) => UserPage(
           id: state.pathParameters['id']!,
         ),
       ),
     ],
   );

   // 使用
   context.go('/user/123'); // 导航
   context.push('/user/123'); // 压栈
   context.pop(); // 返回

4️⃣ 路由守卫（拦截）：
   GoRoute(
     path: '/profile',
     redirect: (_, __) => isLogin ? null : '/login',
   )"
```

---

### Q14: Flutter 的 isolate（并发）？

```dart
✅ 参考答案：
"Dart的并发方案，类似Go的goroutine：

1️⃣ 基本使用：
   import 'dart:isolate';

   void isolateFunction(String message) {
     print(message);
   }

   void main() async {
     // 创建isolate
     final receivePort = ReceivePort();
     await Isolate.spawn(
       isolateFunction,
       'Hello from isolate!',
     );

     // 接收结果
     receivePort.listen((message) {
       print(message);
     });
   }

2️⃣ 传递数据（只能传递可序列化对象）：
   // 发送端
   final message = {'data': 'test'};
   await Isolate.spawn(isolateFunction, message);

   // 接收端
   void isolateFunction(dynamic message) {
     print(message['data']);
   }

3️⃣ compute函数（简化版）：
   import 'package:flutter/foundation.dart';

   final result = await compute(heavyFunction, inputData);

使用场景：
- CPU密集型计算（加密、压缩）
- 大数据处理
- 后台任务处理"
```

---

## 三、综合问题

### Q15: Flutter vs 原生Android，你怎么选？

```dart
✅ 参考答案：
"┌────────────┬──────────────┬──────────────┐
│ 维度       │ Flutter      │ 原生Android  │
├────────────┼──────────────┼──────────────┤
│ 开发效率   │ 高（一套代码）│ 中            │
│ 性能       │ 接近原生      │ 最优          │
│ 生态       │ 增长中        │ 成熟          │
│ 第三方库   │ 相对较少      │ 非常丰富      │
│ 学习成本   │ Dart语言      │ Java/Kotlin  │
│ 适用场景   │ 快速迭代      │ 高性能要求    │
└────────────┴──────────────┴──────────────┘

我的选择标准：

1️⃣ 选Flutter：
   - 跨平台（iOS + Android）
   - 快速原型验证
   - 团队较小（减少维护成本）
   - 中等复杂度UI

2️⃣ 选原生：
   - 极致性能要求（游戏、视频编辑）
   - 深度系统集成（系统权限）
   - 需要大量原生SDK
   - 长期大型项目

对于AI移动端：
Flutter足够，且能快速迭代验证AI功能"
```

---

### Q16: 移动端如何优化性能？

```dart
✅ 参考答案：
"性能优化策略：

1️⃣ UI层面：
   - 避免在build()中创建新Widget
   - 使用const构造器
   - 合理使用RepaintBoundary
   - 图片使用cached_network_image

2️⃣ 列表优化：
   - 使用ListView.builder（懒加载）
   - 合理设置itemExtent
   - 避免在ItemBuilder中重建Widget

3️⃣ 网络层面：
   - 接口缓存
   - 图片压缩
   - 请求合并
   - 离线优先

4️⃣ 内存层面：
   - 及时dispose资源
   - 避免内存泄漏
   - 合理使用WeakReference

5️⃣ 包体积：
   - tree shaking
   - 移除未使用资源
   - 按需加载

示例 - 列表优化：
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ListTile(
      key: ValueKey(items[index].id), // 保持状态
      title: Text(items[index].name),
    );
  },
)"
```

---

### Q17: 你如何实现一个AI聊天界面？

```dart
✅ 参考答案：
"实现思路：

1️⃣ 数据模型：
   class Message {
     final String content;
     final bool isUser;
     final DateTime timestamp;
   }

2️⃣ 状态管理：
   class ChatBloc extends Cubit<List<Message>> {
     Future<void> sendMessage(String text) async {
       // 添加用户消息
       emit([...state, Message(text, true, DateTime.now())]);

       // 调用AI API
       final response = await openai.chat.create(
         messages: [...history, {'role': 'user', 'content': text}],
       );

       // 添加AI回复
       emit([...state, Message(response.text, false, DateTime.now())]);
     }
   }

3️⃣ UI实现：
   ListView.builder(
     reverse: true, // 新消息在底部
     itemCount: messages.length,
     itemBuilder: (_, index) {
       final msg = messages[index];
       return Align(
         alignment: msg.isUser ? Alignment.centerRight : Alignment.centerLeft,
         child: msg.isUser ? UserBubble(msg) : AIBubble(msg),
       );
     },
   )

4️⃣ 打字机效果（流式输出）：
   StreamBuilder<String>(
     stream: streamResponse,
     builder: (_, snapshot) {
       return Text(snapshot.data ?? '');
     },
   )"
```

---

## 四、面试高频手撕代码

### 题目1：反转字符串

```dart
void main() {
  print(reverseString("hello")); // "olleh"
}

String reverseString(String s) {
  return s.split('').reversed.join('');
}
```

### 题目2：合并两个有序数组

```dart
List<int> mergeSortedArrays(List<int> a, List<int> b) {
  int i = 0, j = 0;
  List<int> result = [];

  while (i < a.length && j < b.length) {
    if (a[i] < b[j]) {
      result.add(a[i++]);
    } else {
      result.add(b[j++]);
    }
  }

  result.addAll(a.sublist(i));
  result.addAll(b.sublist(j));
  return result;
}
```

### 题目3：Flutter遍历Map

```dart
void main() {
  Map<String, int> scores = {'Alice': 90, 'Bob': 85};

  // 方法1：forEach
  scores.forEach((key, value) {
    print('$key: $value');
  });

  // 方法2：for in
  for (var entry in scores.entries) {
    print('${entry.key}: ${entry.value}');
  }

  // 方法3：keys/values
  for (var key in scores.keys) {
    print('$key: ${scores[key]}');
  }
}
```

---

> ⭐ 面试前把这些代码在脑子里过一遍！