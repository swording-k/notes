import asyncio, edge_tts, json, os, subprocess, sys

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "+5%"
TMP = "/tmp/edge_v3"
AUDIO = "/Users/baojian/Desktop/changcheng-securities-intern-work/remotion-videos/public/assets/audio"
os.makedirs(TMP, exist_ok=True)
os.makedirs(AUDIO, exist_ok=True)

# 配音文本：每段 6 句 = [开场白(标题+副标题), beat1, beat2, beat3, beat4, 收尾]
# 注意：AI -> 人工智能（避免读成"哎"），字幕保持 AI 不变
SCRIPTS = {
    "home": [
        "首页，你的协同工作台。",
        "一进来就是首页，顶部六张核心数据卡片，让你一眼看清整个团队的协同全局。",
        "左侧的协同动态，是等着你处理的任务，有事儿系统会在这里提醒你。",
        "最重要的在右边协同入口，日常最高频的就是发起协同这个蓝色核心按钮。",
        "下面还有企业三百六十、人工智能舆情、产业链图谱这些辅助工具，以及发现新商机的商机广场。",
        "首页看全局：六张核心数据卡片，加上协同动态待办，加上一键发起协同，团队协同状态尽在掌握。",
    ],
    "opportunity-mining": [
        "商机挖掘，发现并跟踪目标企业。",
        "左侧是一整套商机发现工具箱，核心是你关注的企业。",
        "主界面里是全部目标企业，行业、地区、融资阶段、是不是营销客户，一目了然。",
        "每一行右边都能直接新增联系人、记拜访，甚至一键申请协同。",
        "发现值得跟进的企业，点新增加入关注列表，后面所有动作都从这里启动。",
        "商机挖掘帮你发现值得跟进的企业：关注列表，加上多维字段，加上航内申请协同，商机漏斗一站管理。",
    ],
    "synergy-management": [
        "协同管理，跨部门协同的核心引擎。",
        "协同管理是整个系统的灵魂。左侧五个子功能对应协同的全生命周期，核心是申请协同。",
        "客户经理最常用我发起的，总部同事看我对接的，管理层看全部，三个视图各取所需。",
        "每条协同都有唯一编号，业务大类比如投行或者研究，业务类型比如公司债、北交所，还有当前状态。",
        "常见状态有：刚创建的待填报，等总部接单的待确认，以及走合规流程的审批中。",
        "协同管理是系统灵魂：发起、确认、分润，全流程线上留痕，状态清晰可追溯。",
    ],
    "customer-management": [
        "客户管理，维护你负责的客户档案。",
        "客户管理管的是人，也就是你名下负责的客户档案，分正式客户和潜客。",
        "可以按行业、地区、类型来筛选，大批录入还能用导入功能批量上传。",
        "每个客户卡片都显示拜访次数、联系人、还有关联的协同数量，帮你判断该多花精力。",
        "要是有大批客户要录入，不用一条条加，直接用导入功能批量上传。",
        "客户管理管的是人：拜访次数、联系人、关联协同数一目了然，而且支持批量导入。",
    ],
    "ai-assistant": [
        "人工智能助理，随身的金融业务顾问。",
        "协同学院里最醒目的是人工智能协同助手，一个专门懂业务的智能聊天工具。",
        "左边是历史对话记录，随时回看之前问过的问题。",
        "底部输入框打字就能问，像北交所上市条件、可交换债区别，都能直接问。",
        "注意底部小字：内容由人工智能生成，仅供参考，做决策请以官方文件为准。",
        "人工智能协同助手，你的随身业务顾问，业务问题随时有答案。",
    ],
}

def dur(path):
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", path])
        return float(out.decode().strip())
    except Exception:
        return 0.0

async def gen_one(text, path, retries=6):
    last = None
    for i in range(retries):
        try:
            c = edge_tts.Communicate(text, VOICE, rate=RATE)
            await c.save(path)
            d = dur(path)
            if d > 0.5 and os.path.getsize(path) > 2000:
                return d
            last = f"too short d={d}"
        except Exception as e:
            last = str(e)
        await asyncio.sleep(1.5)
    raise RuntimeError(f"FAILED after {retries} retries: {text[:20]}... ({last})")

async def gen_video(id, sentences):
    paths = []
    durs = []
    for i, s in enumerate(sentences):
        p = os.path.join(TMP, f"{id}_{i}.mp3")
        d = await gen_one(s, p)
        paths.append(p)
        durs.append(round(d, 2))
        print(f"  [{id}] sent{i} {durs[-1]}s  {s[:18]}...")
    # 重新编码拼接，确保时长元数据准确
    listfile = os.path.join(TMP, f"{id}.list")
    with open(listfile, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")
    out = os.path.join(AUDIO, f"{id}.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
        "-c:a", "libmp3lame", "-ar", "44100", "-b:a", "128k", out
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total = dur(out)
    print(f">>> {id} TOTAL={total}s (should ~= {sum(durs)})")
    return durs

async def main():
    timings = {}
    for id, sents in SCRIPTS.items():
        print(f"=== {id} ===")
        timings[id] = await gen_video(id, sents)
    with open("/tmp/edge_timings.json", "w") as f:
        json.dump(timings, f, ensure_ascii=False, indent=2)
    print("ALL_VOICE_DONE")

asyncio.run(main())
