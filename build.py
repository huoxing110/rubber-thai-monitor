import json
from datetime import datetime

def get_trend(data):
    cut = data["week_cut_days"]
    rain = data["rain_anomaly"]
    nino = data["nino34"]

    if cut <= 3:
        short = "【短期利多】有效割胶天数偏少，雨天压制原料产出，杯胶供给偏紧，盘面易受支撑。"
    elif cut >= 5:
        short = "【短期利空】晴好天气充足，割胶顺畅，原料集中上量，盘面承压概率大。"
    else:
        short = "【短期中性】供应平稳，等待天气增量指引。"

    if nino >= 2.0:
        long = "【中长期强利多】强厄尔尼诺持续，四季度至年底东南亚干旱减产风险高，远期多头逻辑稳固。"
    elif nino > 1.5:
        long = "【中长期偏多】厄尔尼诺维持，需持续跟踪产区干旱升温节奏。"
    else:
        long = "【中长期中性】无明显极端气候风险，跟随短期供应波动。"

    if "+" in rain:
        rain_txt = "近期降雨偏多，压制当日开割率，原料释放受限。"
    else:
        rain_txt = "近期降雨偏少，胶园干燥，利于割胶作业。"

    return short, long, rain_txt

def main():
    with open("data.json","r",encoding="utf-8") as f:
        d = json.load(f)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    d["update_date"] = now
    short, long_txt, rain_txt = get_trend(d)

    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>泰胶每日监控面板</title>
<style>
    *{{margin:0;padding:0;box-sizing:border-box;font-family:system-ui,-apple-system,sans-serif;}}
    body{{background:#f6f8fa;padding:20px;color:#222;}}
    .container{{max-width:1000px;margin:0 auto;}}
    .title{{font-size:24px;font-weight:bold;margin-bottom:10px;}}
    .time{{color:#666;margin-bottom:20px;}}
    .card{{background:#fff;border-radius:12px;padding:20px;margin-bottom:16px;box-shadow:0 2px 8px #00000010;}}
    .warn{{border-left:6px solid #f39c12;}}
    table{{width:100%;border-collapse:collapse;margin-top:10px;}}
    th,td{{border:1px solid #eee;padding:12px;text-align:center;}}
    th{{background:#f9fafb;font-weight:600;}}
    .judge{{font-size:16px;line-height:1.8;}}
</style>
</head>
<body>
<div class="container">
    <div class="title">🇹🇭 泰国橡胶核心监控面板（每日自动更新）</div>
    <div class="time">更新时间：{now}</div>

    <div class="card">
        <h3>🌤 产区天气供应指标</h3>
        <table>
            <tr><th>监控指标</th><th>当前数值</th><th>状态解读</th></tr>
            <tr><td>周有效割胶天数</td><td>{d['week_cut_days']} 天</td><td>≤3天供应受限 / ≥5天高产</td></tr>
            <tr><td>周降雨偏离均值</td><td>{d['rain_anomaly']}</td><td>{rain_txt}</td></tr>
            <tr><td>Nino3.4指数</td><td>{d['nino34']}</td><td>{('厄尔尼诺强势' if d['nino34']>1.5 else '正常气候区间')}</td></tr>
        </table>
    </div>

    <div class="card">
        <h3>💰 原料价格（泰铢/kg）</h3>
        <table>
            <tr><th>品类</th><th>现价</th></tr>
            <tr><td>杯胶 Cup Lump</td><td>{d['cup_lump']}</td></tr>
            <tr><td>田间胶水</td><td>{d['field_latex']}</td></tr>
            <tr><td>胶价价差</td><td>{d['spread']}</td></tr>
        </table>
    </div>

    <div class="card warn">
        <h3>📊 AI 行情自动判定</h3>
        <p class="judge"><b>短期走势：</b>{short}</p>
        <p class="judge"><b>中长期走势：</b>{long_txt}</p>
        <p class="judge"><b>当日备注：</b>{d['note']}</p>
    </div>

    <div class="card">
        <h3>📍 当下核心交易逻辑</h3>
        <p>1、9月底‑10月上旬：泰南西岸多雨扰动割胶，短期供应弹性偏弱；</p>
        <p>2、10月下旬起东北季风切换，降雨重心转移东岸；</p>
        <p>3、厄尔尼诺持续跟踪，是四季度核心多头逻辑。</p>
    </div>

</div>
</body>
</html>
    """
    with open("index.html","w",encoding="utf-8") as f:
        f.write(html)
    print("页面生成成功")

if __name__=="__main__":
    main()
