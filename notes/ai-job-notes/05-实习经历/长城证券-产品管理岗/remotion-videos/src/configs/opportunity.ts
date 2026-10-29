import { type PanelConfig } from '../components/PanelVideo';
import { DUR } from '../timings';

export const opportunityConfig: PanelConfig = {
  id: 'opportunity-mining',
  badge: '②',
  title: '商机挖掘',
  subtitle: '发现并跟踪目标企业',
  accent: '#2458D8',
  icon: 'search',
  image: '02-opportunity-mining.png',
  titleScript: '商机挖掘，是客户经理商机漏斗的起点：把散落各渠道的值得跟的企业，统一收口。',
  outro: '商机挖掘帮你把值得跟的企业管起来：关注列表，加上多维字段，加上行内申请协同，商机漏斗一站打通。',
  voice: 'audio/opportunity-mining.mp3',
  bgm: 'audio/bgm.mp3',
  titleFrames: DUR['opportunity-mining'].title,
  outroFrames: DUR['opportunity-mining'].outro,
  beats: [
    {
      cx: 0.13, cy: 0.5, z: 1.5, ww: 0.26, wh: 0.72,
      label: '左侧工具箱 · 关注的企业 ⭐',
      hold: DUR['opportunity-mining'].beats[0],
      narration: '客户经理最贴近客户，但值得跟的企业散落在工商、产业链、舆情和广场线索里——左侧工具箱把它们统一收口到「关注的企业」。',
    },
    {
      cx: 0.5183, cy: 0.4952, z: 1.35, ww: 0.7835, wh: 0.5712,
      label: '关注企业列表',
      sub: '行业 · 地区 · 注册资本 · 融资阶段 · 是否营销客户',
      hold: DUR['opportunity-mining'].beats[1],
      narration: '主列表里，行业、地区、融资阶段、是不是营销客户，多维字段让筛选有了统一口径，不再凭感觉。',
    },
    {
      cx: 0.8344, cy: 0.5462, z: 1.5, ww: 0.2696, wh: 0.6808,
      label: '行内操作 · 申请协同',
      hold: DUR['opportunity-mining'].beats[2],
      narration: '关键认知：商机不是终点，是协同的起点。每一行右边都能直接申请协同——发现需求，立刻就能发起协同。',
    },
    {
      cx: 0.306, cy: 0.2008, z: 1.5, ww: 0.36, wh: 0.2,
      label: '发现目标 → + 新增',
      hold: DUR['opportunity-mining'].beats[3],
      narration: '发现一家值得跟的，先点「新增」收进关注列表；后面所有的拜访、协同，都从这儿开始。',
    },
  ],
};
