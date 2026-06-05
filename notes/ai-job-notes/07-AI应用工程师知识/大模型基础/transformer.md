https://www.bilibili.com/video/BV1xoJwzDESD/?spm_id_from=333.337.search-card.all.click&vd_source=0f2b5f5dae4beb99b68547471f7432e0
## 一.为什么传统算法不适合序列转倒任务
### 1.FNN
![[attachments/Pasted image 20260421160145.png]]
### 2.RNN
![[attachments/Pasted image 20260421160410.png]]
在时间上展开了，一个词一个词进![[attachments/Pasted image 20260421160507.png]]
处理具有时序性的文本很不错，但是结果词数和输入词数不相同怎么办
### 3.编码器，解码器结构
![[attachments/Pasted image 20260421161131.png]]
去掉RNN的y输出，只保留h
拿着c，去解码
模型处理长序列会有遗忘问题，下游的h4遗忘了“我”字
### 4.注意力机制
![[attachments/Pasted image 20260421161724.png]]
## 二.Transformer结构的创新
完全摒弃RNN/CNN，完全基于自注意力机制

![[attachments/Pasted image 20260421162723.png]]
通过词嵌入将句子中每个词放在512维的向量中
进入注意力层：单头/多头注意力机制给输入矩阵加上了各个词之间的关联度，输出一个相同纬度的矩阵
进行残差连接，归一化
进入前馈层
进入右半部分，在注意力，前馈，通过softmax算出得到的矩阵的词位置在词库中对应哪个单词的概率最高
