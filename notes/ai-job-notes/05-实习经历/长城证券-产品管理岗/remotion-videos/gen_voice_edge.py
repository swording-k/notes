import asyncio, edge_tts, subprocess, json, os, re

AUDIO_DIR = "/Users/baojian/Desktop/changcheng-securities-intern-work/remotion-videos/public/assets/audio"
TMP = "/tmp/edge_v3"
SRC_DIR = "/Users/baojian/Desktop/changcheng-securities-intern-work/remotion-videos/src"
os.makedirs(TMP, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
VOICE = "zh-CN-XiaoxiaoNeural"
FPS = 30

def ssml_of(text):
    s = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"AI(\s?)", r'<say-as interpret-as="characters">AI</say-as>\1', s)
    return (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">'
        f'<voice name="{VOICE}">{s}</voice></speak>'
    )

async def gen_sentence(path, text, retries=6):
    for att in range(retries):
        try:
            c = edge_tts.Communicate(ssml_of(text), VOICE)
            await asyncio.wait_for(c.save(path), timeout=25)
            if os.path.getsize(path) > 2000:
                return True
            print(f"    [warn] 空文件, 重试 {att+1}", flush=True)
        except Exception as e:
            print(f"    [warn] 异常 {type(e).__name__} {str(e)[:60]}, 重试 {att+1}", flush=True)
        await asyncio.sleep(1.2)
    raise RuntimeError(f"生成失败: {text[:20]}")

def dur(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path]
    ).decode().strip()
    return float(out)

# ============ 深度口播稿（6 句/面板：标题卡1 + 4镜头 + 收尾卡1） ============
SENTENCES = {
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

async def main():
    timings = {}
    for vid, sents in SENTENCES.items():
        print(f"=== {vid} ===", flush=True)
        seg_paths, durs = [], []
        for i, s in enumerate(sents):
            p = os.path.join(TMP, f"{vid}_{i}.mp3")
            await gen_sentence(p, s)
            d = dur(p)
            durs.append(d)
            seg_paths.append(p)
            print(f"  [{i}] {d:.2f}s  {s[:18]}...", flush=True)
        listfile = os.path.join(TMP, f"{vid}.list")
        with open(listfile, "w") as f:
            for p in seg_paths:
                f.write(f"file '{p}'\n")
        out = os.path.join(AUDIO_DIR, f"{vid}.mp3")
        subprocess.check_call([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", listfile, "-c:a", "libmp3lame", "-b:a", "128k", out
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        total = dur(out)
        timings[vid] = {"title": durs[0], "beats": durs[1:5], "outro": durs[5], "total": total}
        print(f"  -> {vid}.mp3 总时长 {total:.2f}s", flush=True)

    # 写出 remotion 用的帧数（与配音逐帧对齐）
    lines = ["// 自动生成：各面板口播时长（帧）。由 gen_voice_edge.py 依据真实配音生成，勿手改。",
             "export const DUR = {"]
    for vid, t in timings.items():
        beats = ", ".join(str(round(b * FPS)) for b in t["beats"])
        title = round(t["title"] * FPS)
        outro = round(t["outro"] * FPS)
        lines.append(f"  '{vid}': {{ title: {title}, beats: [{beats}], outro: {outro} }},")
    lines.append("} as const;")
    with open(os.path.join(SRC_DIR, "timings.ts"), "w") as f:
        f.write("\n".join(lines) + "\n")

    with open("/tmp/edge_timings.json", "w") as f:
        json.dump(timings, f, ensure_ascii=False, indent=2)
    print("ALL_EDGE_DONE", flush=True)

asyncio.run(main())
