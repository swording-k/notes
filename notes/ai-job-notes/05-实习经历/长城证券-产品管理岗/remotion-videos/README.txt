# 手拉手协同系统 · 五大面板产品介绍短视频

基于 **Remotion**（React + TypeScript 代码驱动）生成，每个面板一个独立短视频。

## 目录结构
```
remotion-videos/
├── src/
│   ├── index.ts              # 注册入口
│   ├── Root.tsx              # 注册 5 个 Composition
│   ├── theme.ts              # 全局常量（尺寸/节奏/字体）
│   ├── icons.tsx             # 内联线性图标
│   ├── components/
│   │   └── PanelVideo.tsx    # 可复用的「标题卡 + 截图走查 + 收尾」组件
│   └── configs/              # 5 个面板的可编辑配置（改文案/区域在此）
│       ├── home.ts
│       ├── opportunity.ts
│       ├── synergy.ts
│       ├── customer.ts
│       └── assistant.ts
├── public/assets/            # 5 张面板截图（01~05）
├── out/                      # 渲染产物 MP4
├── render-all.mjs            # 一键渲染脚本
└── package.json
```

## 视频设计
每个视频约 33 秒（1920×1080 / 30fps），结构为：
1. **标题卡**（2.6s）：面板名 + 一句话定位 + 图标
2. **截图走查**（~28s）：在面板截图上做「电影感推拉摇移」+ 聚光灯高亮 + 标签 + 底部口播字幕
3. **收尾**（2.6s）：一句话总结 + 品牌落版

> 因为素材是 PC 端横屏截图，默认输出 **16:9**。如需抖音竖屏（9:16），改 `theme.ts` 的 `WIDTH/HEIGHT` 并在 config 里把截图区域调整为竖向布局即可。

## 常用命令
```bash
# 本地预览（浏览器实时调参）
npm run studio

# 渲染单个视频
./node_modules/.bin/remotion render home out/home.mp4 \
  --chrome-executable "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 一键渲染全部 5 个
npm run render:all
```

## 自定义
- 改文案 / 高亮区域：编辑 `src/configs/*.ts`（`beats` 里的 `cx/cy/z` 控制聚焦点与放大，`label/sub/narration` 控制字幕）。
- 加 BGM：把 mp3 放到 `public/assets/`，在对应 config 里加 `bgm: 'xxx.mp3'` 即可。
- 节奏：改 `theme.ts` 的 `BEAT_HOLD`（每拍停留帧数）。
