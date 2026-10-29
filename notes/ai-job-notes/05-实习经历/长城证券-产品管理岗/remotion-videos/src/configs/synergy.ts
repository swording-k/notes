import { type PanelConfig } from '../components/PanelVideo';
import { DUR } from '../timings';

export const synergyConfig: PanelConfig = {
  id: 'synergy-management',
  badge: '③',
  title: '协同管理',
  subtitle: '跨部门协同的核心引擎',
  accent: '#2458D8',
  icon: 'network',
  image: '03-synergy-management.png',
  titleScript: '协同管理，是把过去靠人情对接的活儿，变成制度化、留痕的流程——分润是它的终点闭环。',
  outro: '协同管理是系统的灵魂：发起、确认、分润，全流程线上留痕，状态清晰可追溯。',
  voice: 'audio/synergy-management.mp3',
  bgm: 'audio/bgm.mp3',
  titleFrames: DUR['synergy-management'].title,
  outroFrames: DUR['synergy-management'].outro,
  beats: [
    {
      cx: 0.0531, cy: 0.3779, z: 1.5, ww: 0.1062, wh: 0.6719,
      label: '左侧 5 大子功能 · 申请协同 ⭐',
      hold: DUR['synergy-management'].beats[0],
      narration: '一线有客户、却干不了上市辅导、发债、并购这些专业活；总部有能力、但离客户远。点「申请协同」，就把这两边拉到一起。',
    },
    {
      cx: 0.4346, cy: 0.1677, z: 1.4, ww: 0.62, wh: 0.16,
      label: '三个视图：我发起的 / 我对接的 / 全部',
      hold: DUR['synergy-management'].beats[1],
      narration: '客户经理看「我发起的」，总部看「我对接的」，管理层看「全部」——谁该看什么，系统分得清清楚楚，权责不混。',
    },
    {
      cx: 0.5639, cy: 0.576, z: 1.3, ww: 0.8671, wh: 0.6288,
      label: '业务类型决定审批链',
      sub: '投行走一条 · 研究走另一条',
      hold: DUR['synergy-management'].beats[2],
      narration: '业务类型决定审批链：投行走一条、研究走另一条。两条链不同，说明系统已经把业务分类和组织职责挂上了钩。',
    },
    {
      cx: 0.799, cy: 0.5538, z: 1.45, ww: 0.4, wh: 0.4554,
      label: '状态流转 = 责任到人',
      sub: '待填报 → 待确认 → 审批中 → 财务确认 → 已落储',
      hold: DUR['synergy-management'].beats[3],
      narration: '状态即责任到人：待填报是谁在填、待确认等总部接单、审批中走合规；到「财务确认」「已落储」，就是分润结算的闭环。',
    },
  ],
};
