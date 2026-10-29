import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  staticFile,
  useCurrentFrame,
  interpolate,
  spring,
} from 'remotion';
import {
  FPS,
  WIDTH,
  HEIGHT,
  FONT_FAMILY,
  TITLE_FRAMES,
  OUTRO_FRAMES,
  TRANS_FRAMES,
} from '../theme';
import { PanelIcon, type IconName } from '../icons';

export interface Beat {
  /** 聚焦中心 X（0~1，指截图图像自身比例，即该功能在截图里的真实横向位置） */
  cx: number;
  /** 聚焦中心 Y（0~1） */
  cy: number;
  /** 放大倍数（决定框占屏大小） */
  z: number;
  /** 高亮窗口宽（图像比例，默认 0.42） */
  ww?: number;
  /** 高亮窗口高（图像比例，默认 0.34） */
  wh?: number;
  label: string;
  sub?: string;
  narration: string;
  /** 该拍停留帧数（默认 210） */
  hold?: number;
}

export interface PanelConfig {
  id: string;
  badge: string; // ①
  title: string;
  subtitle: string;
  accent: string;
  icon: IconName;
  image: string; // public/assets 下的文件名
  /** 标题卡旁白口播（与配音文件第一句一致） */
  titleScript: string;
  beats: Beat[];
  outro: string;
  bgm?: string; // 可选：public/assets 下的背景音乐文件名
  voice?: string; // 可选：public/assets 下的 AI 旁白配音文件名
  /** 标题卡时长（帧），默认 78；设为开场旁白句时长可使配音与标题卡对齐 */
  titleFrames?: number;
  /** 收尾卡时长（帧），默认 78；设为收尾旁白句时长可使配音不被截断 */
  outroFrames?: number;
}

// 中性浅底（B2B 内训风：去掉电影感深色，改用干净浅灰蓝底）
const BG = '#f4f6fa';
const TEXT = '#0f172a';
const MUTED = '#475569';

const easeInOut = (t: number) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

/** 根据配置计算视频总帧数（供 Composition 使用） */
export const getDuration = (config: PanelConfig): number => {
  const walk = config.beats.reduce((sum, b) => sum + (b.hold ?? 210), 0);
  return (config.titleFrames ?? TITLE_FRAMES) + walk + (config.outroFrames ?? OUTRO_FRAMES);
};

export const PanelVideo: React.FC<{ config: PanelConfig; calibration?: boolean }> = ({
  config,
  calibration,
}) => {
  if (calibration) return <Calibration config={config} />;

  const frame = useCurrentFrame();
  const beats = config.beats;
  const n = beats.length;
  const TITLE = config.titleFrames ?? TITLE_FRAMES;
  const OUTRO = config.outroFrames ?? OUTRO_FRAMES;

  // 每拍的起始帧
  const holds = beats.map((b) => b.hold ?? 210);
  const enters: number[] = [];
  let acc = TITLE;
  for (let i = 0; i < n; i++) {
    enters.push(acc);
    acc += holds[i];
  }
  const walkEnd = acc;
  const outroStart = walkEnd;

  // 当前激活的拍
  let idx = 0;
  for (let i = 0; i < n; i++) {
    if (frame >= enters[i]) idx = i;
  }

  // 相机：在每拍的"停留段"保持静止，仅在停留段末尾 TRANS_FRAMES 帧内过渡到下一拍
  let cam = { cx: beats[0].cx, cy: beats[0].cy, z: beats[0].z };
  if (idx >= n - 1) {
    cam = { cx: beats[n - 1].cx, cy: beats[n - 1].cy, z: beats[n - 1].z };
  } else {
    const steadyEnd = enters[idx] + holds[idx] - TRANS_FRAMES;
    if (frame <= steadyEnd) {
      cam = { cx: beats[idx].cx, cy: beats[idx].cy, z: beats[idx].z };
    } else {
      const t = easeInOut(
        interpolate(frame, [steadyEnd, enters[idx] + holds[idx]], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        })
      );
      cam = {
        cx: lerp(beats[idx].cx, beats[idx + 1].cx, t),
        cy: lerp(beats[idx].cy, beats[idx + 1].cy, t),
        z: lerp(beats[idx].z, beats[idx + 1].z, t),
      };
    }
  }

  // 把 (cx,cy) 这个点平移到屏幕中央并放大 z（图像比例语义，所见即所得）
  const tx = (0.5 - cam.cx) * WIDTH * cam.z;
  const ty = (0.5 - cam.cy) * HEIGHT * cam.z;

  // 各图层透明度
  const titleIn = interpolate(frame, [0, 12], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const titleOut = interpolate(frame, [TITLE - 14, TITLE], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const titleOpacity = titleIn * titleOut;

  const walkIn = interpolate(frame, [TITLE_FRAMES - 10, TITLE_FRAMES + 14], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const walkOut = interpolate(frame, [outroStart - 14, outroStart], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const walkOpacity = walkIn * walkOut;

  const outroIn = interpolate(frame, [outroStart - 10, outroStart + 14], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const titleSpring = spring({ frame, fps: FPS, config: { damping: 18, stiffness: 110, mass: 0.9 } });
  const outroSpring = spring({ frame: frame - outroStart, fps: FPS, config: { damping: 18, stiffness: 110, mass: 0.9 } });

  // 高亮框：停稳那一拍显示，进入后淡入、停留段末尾（过渡前）淡出
  const boxOpacity = (i: number) => {
    const steadyStart = enters[i] + 16;
    const steadyEndI = i < n - 1 ? enters[i] + holds[i] - TRANS_FRAMES : walkEnd;
    return (
      interpolate(frame, [steadyStart, steadyStart + 16], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) *
      interpolate(frame, [steadyEndI - 16, steadyEndI], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
    );
  };

  // 字幕条：与该拍口播音频同窗（enters[i] ~ enters[i]+hold），与配音逐句对齐
  const captionOpacity = (i: number) => {
    const start = enters[i];
    const end = enters[i] + holds[i];
    return (
      interpolate(frame, [start, start + 10], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) *
      interpolate(frame, [end - 10, end], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
    );
  };

  return (
    <AbsoluteFill style={{ backgroundColor: BG, fontFamily: FONT_FAMILY }}>
      {/* 背景极淡品牌光晕（克制，不抢戏） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(1200px 800px at 16% 0%, ${config.accent}12, transparent 60%), radial-gradient(1000px 700px at 100% 100%, ${config.accent}0d, transparent 55%)`,
        }}
      />

      {/* ===================== 走查层 ===================== */}
      <AbsoluteFill style={{ opacity: walkOpacity }}>
        <AbsoluteFill style={{ overflow: 'hidden' }}>
          <div
            style={{
              position: 'absolute',
              inset: 0,
              transform: `translate(${tx}px, ${ty}px) scale(${cam.z})`,
              transformOrigin: 'center',
            }}
          >
            <Img
              src={staticFile(`assets/${config.image}`)}
              style={{ width: '100%', height: '100%', objectFit: 'fill' }}
            />
          </div>
        </AbsoluteFill>

        {/* 高亮框（停稳时显示，正中央即聚焦功能）；浅色柔化四周、边框清晰，非电影感聚光灯 */}
        {beats.map((b, i) => {
          const op = boxOpacity(i);
          if (op <= 0.01) return null;
          const ww = b.ww ?? 0.42;
          const wh = b.wh ?? 0.34;
          const bw = ww * WIDTH * cam.z;
          const bh = wh * HEIGHT * cam.z;
          return (
            <AbsoluteFill key={`box-${i}`} style={{ opacity: op, pointerEvents: 'none' }}>
              <div
                style={{
                  position: 'absolute',
                  left: '50%',
                  top: '50%',
                  width: bw,
                  height: bh,
                  transform: 'translate(-50%, -50%)',
                  border: `3px solid ${config.accent}`,
                  borderRadius: 12,
                  boxShadow: `0 0 0 4000px rgba(244,246,250,0.30), 0 0 22px 2px ${config.accent}33`,
                }}
              >
                <div
                  style={{
                    position: 'absolute',
                    left: 0,
                    top: 0,
                    transform: 'translate(-1px, -100%)',
                    padding: '10px 18px',
                    borderRadius: '12px 12px 12px 0',
                    background: `${config.accent}`,
                    color: '#ffffff',
                    fontWeight: 800,
                    fontSize: 25,
                    whiteSpace: 'nowrap',
                    boxShadow: `0 6px 18px ${config.accent}40`,
                  }}
                >
                  {b.label}
                  {b.sub ? ` · ${b.sub}` : ''}
                </div>
              </div>
            </AbsoluteFill>
          );
        })}

        {/* 底部口播字幕条（浅色毛玻璃，逐句对齐） */}
        {beats.map((b, i) => {
          const op = captionOpacity(i);
          if (op <= 0.01) return null;
          return (
            <AbsoluteFill key={`cap-${i}`} style={{ opacity: op, pointerEvents: 'none' }}>
              <div
                style={{
                  position: 'absolute',
                  left: 0,
                  right: 0,
                  bottom: 0,
                  minHeight: 150,
                  display: 'flex',
                  alignItems: 'center',
                  padding: '24px 64px',
                  background: 'rgba(255,255,255,0.94)',
                  backdropFilter: 'blur(8px)',
                  borderTop: `3px solid ${config.accent}`,
                }}
              >
                <div
                  style={{
                    width: 9,
                    height: 56,
                    borderRadius: 4,
                    background: config.accent,
                    marginRight: 28,
                    flex: '0 0 auto',
                  }}
                />
                <div
                  style={{
                    fontSize: 35,
                    fontWeight: 700,
                    color: TEXT,
                    lineHeight: 1.42,
                    maxWidth: 1640,
                  }}
                >
                  {b.narration}
                </div>
              </div>
            </AbsoluteFill>
          );
        })}

        {/* 左上角品牌标（浅色胶囊） */}
        <div
          style={{
            position: 'absolute',
            left: 46,
            top: 38,
            padding: '10px 20px',
            borderRadius: 999,
            background: 'rgba(255,255,255,0.86)',
            backdropFilter: 'blur(8px)',
            border: `1px solid ${config.accent}55`,
            color: TEXT,
            fontSize: 23,
            fontWeight: 700,
            display: 'flex',
            alignItems: 'center',
            gap: 10,
          }}
        >
          <PanelIcon name={config.icon} size={24} color={config.accent} />
          手拉手协同系统 · {config.badge}
        </div>
      </AbsoluteFill>

      {/* ===================== 标题卡（浅底编辑式排版） ===================== */}
      <AbsoluteFill
        style={{
          opacity: titleOpacity,
          background: `radial-gradient(920px 720px at 22% 16%, ${config.accent}1f, ${BG} 62%)`,
          fontFamily: FONT_FAMILY,
        }}
      >
        <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center' }}>
          <div
            style={{
              paddingLeft: 140,
              transform: `scale(${titleSpring})`,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'flex-start',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 18, marginBottom: 30 }}>
              <div
                style={{
                  width: 104,
                  height: 104,
                  borderRadius: 26,
                  background: `${config.accent}14`,
                  border: `1.5px solid ${config.accent}`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <PanelIcon name={config.icon} size={56} color={config.accent} />
              </div>
              <div style={{ fontSize: 30, fontWeight: 700, color: config.accent, letterSpacing: 6 }}>
                产品介绍 · {config.badge}
              </div>
            </div>
            <div
              style={{
                fontSize: 104,
                fontWeight: 900,
                color: TEXT,
                lineHeight: 1.05,
              }}
            >
              {config.title}
            </div>
            <div style={{ width: 120, height: 6, borderRadius: 3, background: config.accent, margin: '26px 0' }} />
            <div style={{ fontSize: 40, fontWeight: 600, color: MUTED }}>{config.subtitle}</div>
          </div>
        </div>
        {/* 标题卡口播字幕（与配音同窗） */}
        <AbsoluteFill style={{ opacity: titleOpacity, pointerEvents: 'none' }}>
          <div
            style={{
              position: 'absolute',
              left: 0,
              right: 0,
              bottom: 0,
              minHeight: 132,
              display: 'flex',
              alignItems: 'center',
              padding: '22px 140px',
              background: 'rgba(255,255,255,0.92)',
              borderTop: `3px solid ${config.accent}`,
            }}
          >
            <div style={{ width: 9, height: 50, borderRadius: 4, background: config.accent, marginRight: 26, flex: '0 0 auto' }} />
            <div style={{ fontSize: 33, fontWeight: 700, color: TEXT, lineHeight: 1.4, maxWidth: 1500 }}>
              {config.titleScript}
            </div>
          </div>
        </AbsoluteFill>
      </AbsoluteFill>

      {/* ===================== 收尾 ===================== */}
      <AbsoluteFill
        style={{
          opacity: outroIn,
          background: `radial-gradient(920px 720px at 78% 82%, ${config.accent}1f, ${BG} 62%)`,
          fontFamily: FONT_FAMILY,
        }}
      >
        <div
          style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            transform: `scale(${outroSpring})`,
          }}
        >
          <div style={{ fontSize: 28, fontWeight: 700, color: config.accent, letterSpacing: 3 }}>
            {config.badge} · {config.title}
          </div>
          <div
            style={{
              fontSize: 50,
              fontWeight: 800,
              color: TEXT,
              marginTop: 18,
              maxWidth: 1480,
              textAlign: 'center',
              lineHeight: 1.45,
            }}
          >
            {config.outro}
          </div>
          <div style={{ fontSize: 28, fontWeight: 600, color: MUTED, marginTop: 36 }}>
            长城证券 · 手拉手协同系统
          </div>
        </div>
      </AbsoluteFill>

      {/* 配音（音量 1.0）+ 背景音乐（音量 0.18，轻量垫底不抢戏） */}
      {config.voice ? <Audio src={staticFile(`assets/${config.voice}`)} volume={1} /> : null}
      {config.bgm ? <Audio src={staticFile(`assets/${config.bgm}`)} volume={0.18} /> : null}
    </AbsoluteFill>
  );
};

/** 校准图：完整截图 + 坐标网格 + 编号框（所见即所得，供人工校正坐标） */
const Calibration: React.FC<{ config: PanelConfig }> = ({ config }) => {
  const beats = config.beats;
  const linesV = Array.from({ length: 9 }, (_, i) => (i + 1) * 0.1);
  const linesH = Array.from({ length: 5 }, (_, i) => (i + 1) * (1 / 6));
  return (
    <AbsoluteFill style={{ backgroundColor: BG, fontFamily: FONT_FAMILY }}>
      <Img
        src={staticFile(`assets/${config.image}`)}
        style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'fill' }}
      />
      <AbsoluteFill style={{ background: 'rgba(244,246,250,0.20)' }} />
      {linesV.map((p, i) => (
        <div key={`v${i}`} style={{ position: 'absolute', left: `${p * 100}%`, top: 0, bottom: 0, width: 1, background: 'rgba(15,23,42,0.10)' }} />
      ))}
      {linesH.map((p, i) => (
        <div key={`h${i}`} style={{ position: 'absolute', top: `${p * 100}%`, left: 0, right: 0, height: 1, background: 'rgba(15,23,42,0.10)' }} />
      ))}
      {beats.map((b, i) => {
        const ww = b.ww ?? 0.42;
        const wh = b.wh ?? 0.34;
        return (
          <React.Fragment key={`c${i}`}>
            <div
              style={{
                position: 'absolute',
                left: `${(b.cx - ww / 2) * 100}%`,
                top: `${(b.cy - wh / 2) * 100}%`,
                width: `${ww * 100}%`,
                height: `${wh * 100}%`,
                border: `3px solid ${config.accent}`,
                borderRadius: 12,
              }}
            >
              <div
                style={{
                  position: 'absolute',
                  left: -2,
                  top: -2,
                  width: 52,
                  height: 52,
                  borderRadius: 14,
                  background: config.accent,
                  color: '#fff',
                  fontSize: 28,
                  fontWeight: 900,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '0 4px 14px rgba(15,23,42,0.25)',
                }}
              >
                {i + 1}
              </div>
            </div>
            <div
              style={{
                position: 'absolute',
                left: `${b.cx * 100}%`,
                top: `${b.cy * 100}%`,
                width: 18,
                height: 18,
                transform: 'translate(-50%, -50%)',
                borderRadius: '50%',
                border: '3px solid #fff',
                boxShadow: `0 0 0 3px ${config.accent}`,
              }}
            />
          </React.Fragment>
        );
      })}
      <div style={{ position: 'absolute', left: 46, top: 34, color: TEXT, fontSize: 28, fontWeight: 800 }}>
        校准图 · {config.title}
      </div>
      <div style={{ position: 'absolute', left: 46, top: 78, color: MUTED, fontSize: 22, fontWeight: 600, maxWidth: 1500, lineHeight: 1.5 }}>
        请核对：编号框是否框住了对应功能？中心白点是否落在该功能正中？偏了就告诉我「编号 + 往哪偏 + 大概几格」。
      </div>
    </AbsoluteFill>
  );
};
