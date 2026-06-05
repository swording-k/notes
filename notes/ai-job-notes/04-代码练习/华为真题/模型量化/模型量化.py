"""
华为真题：模型量化问题

题目：深度学习模型的推理量化问题，该模型包含多个全连接层，
      每个层可以选择不同的量化方案（16bit量化、8bit量化），
      不同方案会带来不同的内存占用和精度损失。

      需要选择模型最优的量化方案组合，在满足总精度损失约束的前提下最小化内存占用。

输入：
  第一行：整数 L（层数）和浮点数 T（精度损失阈值）
  接下来 L 行，每行描述一层的量化选项：
    整数 K（该层可选的量化位宽数量）
    K 组数据，每组包含：位宽描述、精度损失（浮点数）、内存占用（浮点数）

输出：
  最优总内存占用（保留两位小数）

示例：
  输入:
  3 0.3
  2 8bit 0.2 100.0 16bit 0.1 200.0
  2 8bit 0.3 150.0 16bit 0.1 300.0
  1 8bit 0.1 150.0
  输出:
  650.00
"""

import sys

class Solution:
    def quantize(self, L, T, layers):
        """
        动态规划解法

        问题转化：带约束的背包问题
        - 精度损失 = "重量"
        - 内存占用 = "价值"
        - 目标：重量 <= T 的情况下，价值最小

        dp[j] = 在总精度损失恰好为 j 时所需的最小内存

        时间复杂度: O(L * T * max_options)
        空间复杂度: O(T)
        """
        # 将精度损失阈值放大为整数（保留两位小数）
        SCALE = 100
        T_scaled = int(T * SCALE)

        # 初始化：dp[j] = 最小内存达到精度损失 j
        max_loss = T_scaled  # 最多只需要到 T
        dp = [float('inf')] * (max_loss + 1)
        dp[0] = 0  # 0 精度损失需要 0 内存

        # 遍历每一层
        for options in layers:
            # options: [(loss, mem), ...]
            dp_new = dp[:]  # 复制上一层的状态

            # 枚举当前层的所有量化选项
            for loss, mem in options:
                loss_scaled = int(loss * SCALE)
                mem_scaled = int(mem * SCALE)

                # 更新 dp（从低精度往高精度枚举）
                for j in range(max_loss - loss_scaled + 1):
                    if dp[j] != float('inf'):
                        new_loss = j + loss_scaled
                        dp_new[new_loss] = min(dp_new[new_loss], dp[j] + mem_scaled)

            dp = dp_new

        # 找到精度损失 <= T 的最小内存
        result = float('inf')
        for j in range(T_scaled + 1):
            result = min(result, dp[j])

        return result / SCALE  # 还原为浮点数


if __name__ == "__main__":
    # 读取输入
    data = sys.stdin.read().strip().split()
    if not data:
        exit()

    L = int(data[0])
    T = float(data[1])

    layers = []
    idx = 2

    for _ in range(L):
        K = int(data[idx])
        idx += 1

        options = []
        for _ in range(K):
            # 格式: 8bit loss mem 或 16bit loss mem
            bit = data[idx]  # 8bit 或 16bit（不用于计算）
            loss = float(data[idx + 1])
            mem = float(data[idx + 2])
            idx += 3
            options.append((loss, mem))

        layers.append(options)

    # 计算并输出
    sol = Solution()
    result = sol.quantize(L, T, layers)
    print(f"{result:.2f}")