import json, re, os

FPS = 30
BASE = "/Users/baojian/Desktop/changcheng-securities-intern-work/remotion-videos/src/configs"
timings = json.load(open("/tmp/edge_timings.json"))

# id -> 文件名
FILEMAP = {
    "home": "home.ts",
    "opportunity-mining": "opportunity.ts",
    "synergy-management": "synergy.ts",
    "customer-management": "customer.ts",
    "ai-assistant": "assistant.ts",
}

# 每拍缓冲帧（防字幕在句尾被截断）
BUF = 6

for vid, durs in timings.items():
    path = os.path.join(BASE, FILEMAP[vid])
    src = open(path).read()
    # durs: [open, b1, b2, b3, b4, outro]
    title_f = round(durs[0] * FPS)
    holds = [round(d * FPS) + BUF for d in durs[1:5]]
    outro_f = round(durs[5] * FPS)

    # titleFrames
    src, n1 = re.subn(r"titleFrames:\s*\d+", f"titleFrames: {title_f}", src, count=1)
    # 4 个 hold（按顺序）
    def repl(m, holds=holds, i=[0]):
        v = holds[i[0]]; i[0] += 1; return f"hold: {v}"
    src, n2 = re.subn(r"hold:\s*\d+", repl, src)
    # outroFrames
    src, n3 = re.subn(r"outroFrames:\s*\d+", f"outroFrames: {outro_f}", src, count=1)

    assert n1 == 1 and n2 == 4 and n3 == 1, f"{vid}: n1={n1} n2={n2} n3={n3}"
    open(path, "w").write(src)
    print(f"{vid}: title={title_f} holds={holds} outro={outro_f}  total={title_f+sum(holds)+outro_f}f ({round((title_f+sum(holds)+outro_f)/FPS,1)}s)")
print("TIMINGS_APPLIED")
