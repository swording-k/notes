import { type PanelConfig } from '../components/PanelVideo';
import { DUR } from '../timings';

export const assistantConfig: PanelConfig = {
  id: 'ai-assistant',
  badge: '⑤',
  title: 'AI 助理',
  subtitle: '随身的金融业务顾问',
  accent: '#2458D8',
  icon: 'sparkles',
  image: '05-ai-assistant.png',
  titleScript: 'AI 助理，是把法规和业务知识下沉到一线的随身顾问，降低客户经理获取专业知识的门槛。',
  outro: 'AI 协同助手，你的随身业务顾问：业务问题随时有答案，但内容仅供参考，决策以官方为准。',
  voice: 'audio/ai-assistant.mp3',
  bgm: 'audio/bgm.mp3',
  titleFrames: DUR['ai-assistant'].title,
  outroFrames: DUR['ai-assistant'].outro,
  beats: [
    {
      cx: 0.0632, cy: 0.2971, z: 1.5, ww: 0.1263, wh: 0.4142,
      label: '左侧 · AI 协同助手 ⭐',
      hold: DUR['ai-assistant'].beats[0],
      narration: '协同学院里最显眼的就是 AI 协同助手，一个专门对手拉手业务场景训练出来的对话助手。',
    },
    {
      cx: 0.2139, cy: 0.3975, z: 1.4, ww: 0.1929, wh: 0.7065,
      label: '历史对话记录',
      hold: DUR['ai-assistant'].beats[1],
      narration: '左边是历史对话记录，之前问过的——北交所条件、可交换债区别——随时回看，不用重复问。',
    },
    {
      cx: 0.5487, cy: 0.8292, z: 1.35, ww: 0.5619, wh: 0.2008,
      label: '底部输入框 · 问业务问题',
      sub: '如：北交所上市条件？可交换债与普通公司债区别？',
      hold: DUR['ai-assistant'].beats[2],
      narration: '底部输入框打字就能问：客户发债要准备什么材料、协同被驳回怎么办，业务问题随时有答案。',
    },
    {
      cx: 0.6038, cy: 0.93, z: 1.4, ww: 0.7, wh: 0.14,
      label: '⚠️ 免责声明',
      sub: '内容由 AI 生成，仅供参考，决策以官方为准',
      hold: DUR['ai-assistant'].beats[3],
      narration: '底部小字写得清楚：内容由 AI 生成、仅供参考，不做合规判断。它替代不了合规，但能降低一线获取知识的门槛。',
    },
  ],
};
