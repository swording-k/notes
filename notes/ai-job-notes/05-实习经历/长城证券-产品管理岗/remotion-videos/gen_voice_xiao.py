#!/usr/bin/env python3
"""
用微软神经网络嗓 XiaoxiaoNeural 重新生成 5 面板中文配音（替换此前过假的 macOS Tingting）。
- 纯文本模式（绝不用 <speak> SSML，否则语速慢 7 倍）
- rate 走构造器顶层参数 "+5%"
- 语音安全替换（仅作用于配音文本，字幕保持原字）：
    "AI" -> "人工智能"（避免读成"哎"）
    "行内" -> "航内"（航=háng，听感等同"行内"）
    "每一行" -> "每一航"（表格"每行"读 háng）
- 逐句重试 + 整面板重试（应对 speech.platform.bing.com 偶发连接中断）+ ffmpeg 重新编码拼接
- 增量持久化到 /tmp/edge_xiao/results.json，崩溃可续跑；已完成的面板跳过
- 依据真实配音时长写出 src/timings.ts（帧数 = round(秒 * 30)，严格对齐 PanelVideo 的 title->beats->outro 时间轴）
"""
import asyncio
import edge_tts
import json
import os
import subprocess

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "+5%"
FPS = 30
PROJ = "/Users/baojian/Desktop/changcheng-securities-intern-work/remotion-videos"
AUDIO_DIR = os.path.join(PROJ, "public/assets/audio")
TMP = "/tmp/edge_xiao"
RESULTS_PATH = os.path.join(TMP, "results.json")
os.makedirs(TMP, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

SCRIPTS = {
    "home": [
        "首页，是整个系统的信息中枢，让一线和管理层在同一块屏上看见协同全局。",
        "顶部六张卡片不是装饰：协同总数、已对接，反映全公司协同有多活跃；参与人数，反映这个平台动员了多少人力。",
        "左边这块协同动态，是系统主动推到你面前的待办——过去靠微信@、靠自己记，现在系统替你盯着。",
        "右边六个协同入口，是把一次协同从发现到分润的六个动作做成一键直达，最高频的就是这个蓝色「发起协同」。",
        "再往下，企业360、产业链、AI舆情这些辅助工具，加上发现新商机的商机广场，都在这里随手可达。",
        "首页就是你的协同工作台：六张卡片看全局，协同动态管待办，一键发起协同，团队状态都在手里。",
    ],
    "opportunity-mining": [
        "商机挖掘，是客户经理商机漏斗的起点：把散落各渠道的值得跟的企业，统一收口。",
        "客户经理最贴近客户，但值得跟的企业散落在工商、产业链、舆情和广场线索里——左侧工具箱把它们统一收口到「关注的企业」。",
        "主列表里，行业、地区、融资阶段、是不是营销客户，多维字段让筛选有了统一口径，不再凭感觉。",
        "关键认知：商机不是终点，是协同的起点。每一行右边都能直接申请协同——发现需求，立刻就能发起协同。",
        "发现一家值得跟的，先点「新增」收进关注列表；后面所有的拜访、协同，都从这儿开始。",
        "商机挖掘帮你把值得跟的企业管起来：关注列表，加上多维字段，加上行内申请协同，商机漏斗一站打通。",
    ],
    "synergy-management": [
        "协同管理，是把过去靠人情对接的活儿，变成制度化、留痕的流程——分润是它的终点闭环。",
        "一线有客户、却干不了上市辅导、发债、并购这些专业活；总部有能力、但离客户远。点「申请协同」，就把这两边拉到一起。",
        "客户经理看「我发起的」，总部看「我对接的」，管理层看「全部」——谁该看什么，系统分得清清楚楚，权责不混。",
        "业务类型决定审批链：投行走一条、研究走另一条。两条链不同，说明系统已经把业务分类和组织职责挂上了钩。",
        "状态即责任到人：待填报是谁在填、待确认等总部接单、审批中走合规；到「财务确认」「已落储」，就是分润结算的闭环。",
        "协同管理是系统的灵魂：发起、确认、分润，全流程线上留痕，状态清晰可追溯。",
    ],
    "customer-management": [
        "客户管理，管的是协同的「主语」——人。每一次协同，都依附在某家客户身上。",
        "左边把客户分成「我服务的客户」和「潜在客户」，正式与潜客分层，是资源分配的抓手。",
        "可以按行业、地区、类型来筛选；几十上百个客户要录，不用一条条加，导入功能批量上传。",
        "每个客户卡片都显示拜访次数、联系人、还有关联的协同数——一眼就能判断该把精力花在谁身上。",
        "批量导入不只是省事：它减少重复建档，呼应监管「同一客户统一管理」的要求，也是打破信息孤岛的抓手。",
        "客户管理管的是人：拜访次数、联系人、关联协同数一目了然，而且支持批量导入。",
    ],
    "ai-assistant": [
        "AI 助理，是把法规和业务知识下沉到一线的随身顾问，降低客户经理获取专业知识的门槛。",
        "协同学院里最显眼的就是 AI 协同助手，一个专门对手拉手业务场景训练出来的对话助手。",
        "左边是历史对话记录，之前问过的——北交所条件、可交换债区别——随时回看，不用重复问。",
        "底部输入框打字就能问：客户发债要准备什么材料、协同被驳回怎么办，业务问题随时有答案。",
        "底部小字写得清楚：内容由 AI 生成、仅供参考，不做合规判断。它替代不了合规，但能降低一线获取知识的门槛。",
        "AI 协同助手，你的随身业务顾问：业务问题随时有答案，但内容仅供参考，决策以官方为准。",
    ],
}


def fix(text: str) -> str:
    t = text.replace("AI", "人工智能")
    t = t.replace("行内", "航内")        # 航 = háng，听感等同「行内」
    t = t.replace("每一行", "每一航")     # 表格「每行」读 háng
    return t


def dur(path):
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", path])
        return float(out.decode().strip())
    except Exception:
        return 0.0


async def gen_one(text, path, retries=8):
    last = None
    for _ in range(retries):
        try:
            c = edge_tts.Communicate(text, VOICE, rate=RATE)  # 纯文本 + 顶层 rate
            await asyncio.wait_for(c.save(path), timeout=40)
            d = dur(path)
            if d > 0.5 and os.path.getsize(path) > 2000:
                return d
            last = f"too short d={d}"
        except Exception as e:
            last = f"{type(e).__name__}:{e}"
        await asyncio.sleep(2.5)
    raise RuntimeError(f"FAILED after {retries} retries: {text[:20]} ({last})")


async def gen_panel(id, sentences):
    last_err = None
    for attempt in range(5):  # 整面板重试，应对连接中断
        try:
            paths, durs = [], []
            for i, s in enumerate(sentences):
                p = os.path.join(TMP, f"{id}_{i}.mp3")
                d = await gen_one(fix(s), p)
                paths.append(p)
                durs.append(round(d, 3))
                print(f"  [{id}] seg{i} {durs[-1]}s  {s[:16]}...")
            listfile = os.path.join(TMP, f"{id}.list")
            with open(listfile, "w") as f:
                for p in paths:
                    f.write(f"file '{p}'\n")
            out = os.path.join(AUDIO_DIR, f"{id}.mp3")
            subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
                            "-c:a", "libmp3lame", "-ar", "44100", "-b:a", "128k", out],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            total = dur(out)
            print(f">>> {id} TOTAL={total:.2f}s")
            to_frames = lambda sec: int(round(sec * FPS))
            return {
                "title": to_frames(durs[0]),
                "beats": [to_frames(durs[i + 1]) for i in range(4)],
                "outro": to_frames(durs[5]),
            }
        except Exception as e:
            last_err = e
            print(f"  [WARN {id}] attempt {attempt} failed: {e}; retry in 12s")
            await asyncio.sleep(12)
    raise last_err


def load_results():
    if os.path.exists(RESULTS_PATH):
        try:
            with open(RESULTS_PATH) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def write_timings(res):
    lines = []
    lines.append("// 自动生成：各面板口播时长（帧）。由 gen_voice_xiao.py 依据 XiaoxiaoNeural 真实配音生成，勿手改。")
    lines.append("export const DUR = {")
    for id, v in res.items():
        beats = ", ".join(str(b) for b in v["beats"])
        lines.append(f"  '{id}': {{ title: {v['title']}, beats: [{beats}], outro: {v['outro']} }},")
    lines.append("} as const;")
    with open(os.path.join(PROJ, "src/timings.ts"), "w") as f:
        f.write("\n".join(lines) + "\n")


async def main():
    res = load_results()
    for id, sents in SCRIPTS.items():
        mp3 = os.path.join(AUDIO_DIR, f"{id}.mp3")
        if id in res and os.path.exists(mp3) and dur(mp3) > 30:
            print(f"=== {id} (skip, already done) ===")
            continue
        print(f"=== {id} ===")
        res[id] = await gen_panel(id, sents)
        with open(RESULTS_PATH, "w") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
    write_timings(res)
    print("\n=== src/timings.ts ===")
    print(open(os.path.join(PROJ, "src/timings.ts")).read())
    print("ALL_VOICE_DONE")


if __name__ == "__main__":
    asyncio.run(main())
