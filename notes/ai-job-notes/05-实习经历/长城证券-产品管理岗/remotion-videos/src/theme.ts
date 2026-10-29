// 全局常量（Constants-First Design）：改这里即可统一调整尺寸/节奏/风格
export const FPS = 30;
// 截图真实比例约 2:1（1909×955 等），用 1920×960 贴合，避免 16:9 拉伸变形
export const WIDTH = 1920;
export const HEIGHT = 960;

// 中文字体栈：依赖 macOS 系统字体（PingFang SC 等），无需联网下载
export const FONT_FAMILY =
  "'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans SC',system-ui,sans-serif";

export const TITLE_FRAMES = 78; // 标题卡 2.6s
export const OUTRO_FRAMES = 78; // 收尾 2.6s
export const BEAT_HOLD = 210; // 每拍停留 7s
export const TRANS_FRAMES = 24; // 两拍之间相机过渡 0.8s（期间不显示框，避免脱靶）
