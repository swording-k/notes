import { type PanelConfig } from '../components/PanelVideo';
import { DUR } from '../timings';

export const homeConfig: PanelConfig = {
  id: 'home',
  badge: '①',
  title: '首页',
  subtitle: '你的协同工作台',
  accent: '#2458D8',
  icon: 'home',
  image: '01-home.png',
  titleScript: '首页，是整个系统的信息中枢，让一线和管理层在同一块屏上看见协同全局。',
  outro: '首页就是你的协同工作台：六张卡片看全局，协同动态管待办，一键发起协同，团队状态都在手里。',
  voice: 'audio/home.mp3',
  bgm: 'audio/bgm.mp3',
  titleFrames: DUR.home.title,
  outroFrames: DUR.home.outro,
  beats: [
    {
      cx: 0.499, cy: 0.1415, z: 1.5, ww: 0.9719, wh: 0.17,
      label: '6 大核心数据卡片',
      sub: '协同总数 · 已对接 · 客户数 · 参与人数…',
      hold: DUR.home.beats[0],
      narration: '顶部六张卡片不是装饰：协同总数、已对接，反映全公司协同有多活跃；参与人数，反映这个平台动员了多少人力。',
    },
    {
      cx: 0.2018, cy: 0.4676, z: 1.5, ww: 0.4037, wh: 0.4996,
      label: '协同动态 · 待办 / 待评',
      hold: DUR.home.beats[1],
      narration: '左边这块协同动态，是系统主动推到你面前的待办——过去靠微信@、靠自己记，现在系统替你盯着。',
    },
    {
      cx: 0.6885, cy: 0.5788, z: 1.55, ww: 0.6, wh: 0.6431,
      label: '协同入口 · 发起协同 ⭐',
      sub: '最高频：新建拜访 / 联系人 / 发起协同',
      hold: DUR.home.beats[2],
      narration: '右边六个协同入口，是把一次协同从发现到分润的六个动作做成一键直达，最高频的就是这个蓝色「发起协同」。',
    },
    {
      cx: 0.2017, cy: 0.8708, z: 1.45, ww: 0.3931, wh: 0.2585,
      label: '辅助工具 + 商机广场',
      sub: '企业360 · 产业链 · AI舆情 · 公开线索',
      hold: DUR.home.beats[3],
      narration: '再往下，企业360、产业链、AI舆情这些辅助工具，加上发现新商机的商机广场，都在这里随手可达。',
    },
  ],
};
