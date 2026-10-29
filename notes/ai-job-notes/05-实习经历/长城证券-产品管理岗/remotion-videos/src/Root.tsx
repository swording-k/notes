import React from 'react';
import { Composition } from 'remotion';
import { PanelVideo, getDuration, type PanelConfig } from './components/PanelVideo';
import { MergedFilm, getMergedDuration } from './MergedFilm';
import { WIDTH, HEIGHT, FPS } from './theme';
import { homeConfig } from './configs/home';
import { opportunityConfig } from './configs/opportunity';
import { synergyConfig } from './configs/synergy';
import { customerConfig } from './configs/customer';
import { assistantConfig } from './configs/assistant';

const configs: PanelConfig[] = [
  homeConfig,
  opportunityConfig,
  synergyConfig,
  customerConfig,
  assistantConfig,
];

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {configs.map((c) => (
        <Composition
          key={c.id}
          id={c.id}
          component={PanelVideo}
          durationInFrames={getDuration(c)}
          fps={FPS}
          width={WIDTH}
          height={HEIGHT}
          defaultProps={{ config: c }}
        />
      ))}
      {/* 合并宣传片：矿业公司发债端到端案例（intro + 5 面板 + outro） */}
      <Composition
        id="merged-film"
        component={MergedFilm}
        durationInFrames={getMergedDuration()}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
        defaultProps={{}}
      />
      {/* 校准图：同一套配置，calibration=true，用于人工核对框位置 */}
      {configs.map((c) => (
        <Composition
          key={`cal-${c.id}`}
          id={`cal-${c.id}`}
          component={PanelVideo}
          durationInFrames={30}
          fps={FPS}
          width={WIDTH}
          height={HEIGHT}
          defaultProps={{ config: c, calibration: true }}
        />
      ))}
    </>
  );
};
