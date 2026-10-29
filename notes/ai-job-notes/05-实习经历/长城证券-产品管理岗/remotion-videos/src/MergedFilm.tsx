import React from 'react';
import {
  AbsoluteFill,
  Audio,
  staticFile,
  useCurrentFrame,
  interpolate,
  spring,
  Sequence,
} from 'remotion';
import { PanelVideo, getDuration, type PanelConfig } from './components/PanelVideo';
import { WIDTH, HEIGHT, FPS, FONT_FAMILY } from './theme';
import { homeConfig } from './configs/home';
import { opportunityConfig } from './configs/opportunity';
import { synergyConfig } from './configs/synergy';
import { customerConfig } from './configs/customer';
import { assistantConfig } from './configs/assistant';

// 合并宣传片：以「某矿业公司发行公司债」为端到端案例，用 5 大面板串成一条协同链路。
// 复用 PanelVideo（<Sequence> 负责帧偏移），仅新增首尾案例卡 + 衔接，零重复实现、风格一致。

const BG = '#f4f6fa';
const TEXT = '#0f172a';
const MUTED = '#475569';
const ACCENT = '#2458D8';

// 顺序本身即案例流：信息中枢(首页) → 发现标的(商机挖掘) → 发起协同/分润(协同管理) → 建档(客户管理) → 答疑(AI助理)
const ORDER: PanelConfig[] = [
  homeConfig,
  opportunityConfig,
  synergyConfig,
  customerConfig,
  assistantConfig,
];

// 首尾案例卡时长（帧）。配音文案长度已匹配此预算，留有余量避免截断。
export const INTRO_FRAMES = 360; // ~12s
export const OUTRO_FRAMES = 300; // ~10s

export const getMergedDuration = (): number => {
  const panels = ORDER.reduce((s, c) => s + getDuration(c), 0);
  return INTRO_FRAMES + panels + OUTRO_FRAMES;
};

const INTRO_TEXT =
  '我们以一家想发行公司债的矿业公司为例——从发现这家企业，到发起协同、分润落袋，手拉手把五个模块串成一条完整的协同链路。';
const OUTRO_TEXT =
  '从发现商机到分润落袋，全流程在系统里留痕，权责清晰可追溯。长城证券 · 手拉手协同系统。';

const IntroCard: React.FC = () => {
  const frame = useCurrentFrame();
  const inO = interpolate(frame, [0, 16], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const outO = interpolate(frame, [INTRO_FRAMES - 18, INTRO_FRAMES], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const opacity = inO * outO;
  const s = spring({ frame, fps: FPS, config: { damping: 18, stiffness: 110, mass: 0.9 } });
  return (
    <AbsoluteFill
      style={{
        opacity,
        background: `radial-gradient(1100px 820px at 28% 16%, ${ACCENT}24, ${BG} 60%)`,
        fontFamily: FONT_FAMILY,
      }}
    >
      <AbsoluteFill style={{ opacity: 0.06, background: `radial-gradient(900px 700px at 100% 100%, ${ACCENT}, transparent 60%)` }} />
      <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', transform: `scale(${s})` }}>
        <div style={{ fontSize: 34, fontWeight: 800, color: ACCENT, letterSpacing: 10, marginBottom: 26 }}>手拉手协同系统</div>
        <div style={{ fontSize: 92, fontWeight: 900, color: TEXT, lineHeight: 1.08, textAlign: 'center' }}>五大模块 · 一条协同链路</div>
        <div style={{ width: 140, height: 6, borderRadius: 3, background: ACCENT, margin: '34px 0' }} />
        <div style={{ fontSize: 32, fontWeight: 600, color: MUTED, letterSpacing: 2 }}>端到端案例：一家矿业公司的发债协同</div>
      </div>
      {/* 底部口播字幕（与配音同窗） */}
      <AbsoluteFill style={{ opacity, pointerEvents: 'none' }}>
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, minHeight: 150, display: 'flex', alignItems: 'center', padding: '26px 72px', background: 'rgba(255,255,255,0.94)', backdropFilter: 'blur(8px)', borderTop: `3px solid ${ACCENT}` }}>
          <div style={{ width: 9, height: 56, borderRadius: 4, background: ACCENT, marginRight: 28, flex: '0 0 auto' }} />
          <div style={{ fontSize: 33, fontWeight: 700, color: TEXT, lineHeight: 1.42, maxWidth: 1640 }}>{INTRO_TEXT}</div>
        </div>
      </AbsoluteFill>
      <Audio src={staticFile('assets/audio/merged-intro.mp3')} volume={1} />
      <Audio src={staticFile('assets/audio/bgm.mp3')} volume={0.18} />
    </AbsoluteFill>
  );
};

const OutroCard: React.FC = () => {
  const frame = useCurrentFrame();
  const inO = interpolate(frame, [0, 16], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const outO = interpolate(frame, [OUTRO_FRAMES - 18, OUTRO_FRAMES], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const opacity = inO * outO;
  const s = spring({ frame: frame, fps: FPS, config: { damping: 18, stiffness: 110, mass: 0.9 } });
  return (
    <AbsoluteFill
      style={{
        opacity,
        background: `radial-gradient(1100px 820px at 72% 84%, ${ACCENT}24, ${BG} 60%)`,
        fontFamily: FONT_FAMILY,
      }}
    >
      <AbsoluteFill style={{ opacity: 0.06, background: `radial-gradient(900px 700px at 0% 0%, ${ACCENT}, transparent 60%)` }} />
      <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', transform: `scale(${s})` }}>
        <div style={{ fontSize: 30, fontWeight: 800, color: ACCENT, letterSpacing: 6, marginBottom: 24 }}>协同闭环</div>
        <div style={{ fontSize: 74, fontWeight: 900, color: TEXT, lineHeight: 1.18, textAlign: 'center', maxWidth: 1500 }}>从发现到分润，全流程留痕</div>
        <div style={{ fontSize: 30, fontWeight: 600, color: MUTED, marginTop: 36, letterSpacing: 2 }}>长城证券 · 手拉手协同系统</div>
      </div>
      <AbsoluteFill style={{ opacity, pointerEvents: 'none' }}>
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, minHeight: 150, display: 'flex', alignItems: 'center', padding: '26px 72px', background: 'rgba(255,255,255,0.94)', backdropFilter: 'blur(8px)', borderTop: `3px solid ${ACCENT}` }}>
          <div style={{ width: 9, height: 56, borderRadius: 4, background: ACCENT, marginRight: 28, flex: '0 0 auto' }} />
          <div style={{ fontSize: 33, fontWeight: 700, color: TEXT, lineHeight: 1.42, maxWidth: 1640 }}>{OUTRO_TEXT}</div>
        </div>
      </AbsoluteFill>
      <Audio src={staticFile('assets/audio/merged-outro.mp3')} volume={1} />
      <Audio src={staticFile('assets/audio/bgm.mp3')} volume={0.18} />
    </AbsoluteFill>
  );
};

export const MergedFilm: React.FC = () => {
  const offsets: number[] = [];
  let acc = INTRO_FRAMES;
  for (const c of ORDER) {
    offsets.push(acc);
    acc += getDuration(c);
  }
  const outroStart = acc;

  return (
    <AbsoluteFill style={{ backgroundColor: BG, fontFamily: FONT_FAMILY }}>
      <Sequence from={0} durationInFrames={INTRO_FRAMES}>
        <IntroCard />
      </Sequence>
      {ORDER.map((c, i) => (
        <Sequence key={c.id} from={offsets[i]} durationInFrames={getDuration(c)}>
          <PanelVideo config={c} />
        </Sequence>
      ))}
      <Sequence from={outroStart} durationInFrames={OUTRO_FRAMES}>
        <OutroCard />
      </Sequence>
    </AbsoluteFill>
  );
};
