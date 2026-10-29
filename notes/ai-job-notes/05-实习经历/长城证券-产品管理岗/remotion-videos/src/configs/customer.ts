import { type PanelConfig } from '../components/PanelVideo';
import { DUR } from '../timings';

export const customerConfig: PanelConfig = {
  id: 'customer-management',
  badge: '④',
  title: '客户管理',
  subtitle: '维护你负责的客户档案',
  accent: '#2458D8',
  icon: 'users',
  image: '04-customer-management.png',
  titleScript: '客户管理，管的是协同的「主语」——人。每一次协同，都依附在某家客户身上。',
  outro: '客户管理管的是人：拜访次数、联系人、关联协同数一目了然，而且支持批量导入。',
  voice: 'audio/customer-management.mp3',
  bgm: 'audio/bgm.mp3',
  titleFrames: DUR['customer-management'].title,
  outroFrames: DUR['customer-management'].outro,
  beats: [
    {
      cx: 0.0685, cy: 0.2062, z: 1.5, ww: 0.1369, wh: 0.4123,
      label: '左侧：我服务的客户 / 潜在客户',
      hold: DUR['customer-management'].beats[0],
      narration: '左边把客户分成「我服务的客户」和「潜在客户」，正式与潜客分层，是资源分配的抓手。',
    },
    {
      cx: 0.4913, cy: 0.1119, z: 1.4, ww: 0.72, wh: 0.16,
      label: '多维筛选',
      sub: '客户名称 · 行业 · 地区 · 类型',
      hold: DUR['customer-management'].beats[1],
      narration: '可以按行业、地区、类型来筛选；几十上百个客户要录，不用一条条加，导入功能批量上传。',
    },
    {
      cx: 0.5482, cy: 0.4202, z: 1.3, ww: 0.8344, wh: 0.5173,
      label: '客户档案字段',
      sub: '拜访次数 · 联系人数量 · 关联协同数',
      hold: DUR['customer-management'].beats[2],
      narration: '每个客户卡片都显示拜访次数、联系人、还有关联的协同数——一眼就能判断该把精力花在谁身上。',
    },
    {
      cx: 0.2921, cy: 0.2542, z: 1.5, ww: 0.32, wh: 0.18,
      label: '批量导入客户',
      hold: DUR['customer-management'].beats[3],
      narration: '批量导入不只是省事：它减少重复建档，呼应监管「同一客户统一管理」的要求，也是打破信息孤岛的抓手。',
    },
  ],
};
