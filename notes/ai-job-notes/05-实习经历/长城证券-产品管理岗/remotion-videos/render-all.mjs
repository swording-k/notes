import { execSync } from 'node:child_process';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const ids = [
  'home',
  'opportunity-mining',
  'synergy-management',
  'customer-management',
  'ai-assistant',
];

execSync('mkdir -p out');

for (const id of ids) {
  const out = `out/${id}.mp4`;
  console.log(`\n=== Rendering ${id} -> ${out} ===`);
  execSync(
    `./node_modules/.bin/remotion render ${id} ${out} --chrome-executable "${CHROME}"`,
    { stdio: 'inherit' }
  );
}

console.log('\n✅ 全部渲染完成，产物在 out/ 目录。');
