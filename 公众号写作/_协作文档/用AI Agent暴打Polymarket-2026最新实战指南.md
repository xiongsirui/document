# 用 AI Agent 炒了一个月 Polymarket，结果没想到...

> 2026 年最适合程序员的交易赛道，可能不是炒币，而是预测市场

---

## 开场白

上个月我做了一个实验：给 Claude 投了 1000 USDC，让它在 Polymarket（一个预测市场平台）上自主交易。

一个月后，账户变成了 1386 USDC。

不算暴富，但也没亏。更重要的是，这个实验让我意识到一件事：**2026 年的 AI Agent，可能更适合玩预测市场，而不是炒币。**

为什么？

### 说句大白话：预测市场比加密货币简单太多了

我之前也试过让 Claude 分析 K 线、预测比特币走势。结果呢？三天亏了 15%。

问题在哪？加密货币价格是连续的，受太多因素影响：宏观消息、大户操纵、链上数据、技术指标...即使是最新的 GPT-4，面对这些噪声也一头雾水。

但预测市场不一样。

它的逻辑是 **二元对立**：某个事件要么发生（YES），要么不发生（NO）。

比如：
- "特朗普会赢得 2024 美国大选吗？" → YES 或 NO
- "比特币在 2025 年底会超过 10 万美元吗？" → YES 或 NO

这种形式太适合 AI 了。AI 最擅长的就是：**基于信息推理概率**。

而且，2025-2026 年是预测市场的爆发期。Polymarket 的交易量从 2024 年的 1 亿美元，暴涨到 2026 年预计的 50 亿美元。更重要的是，官方在 2025 年推出了 [agents 开发框架](https://github.com/Polymarket/agents)，降低了 AI 接入门槛。

这是一个窗口期。等到量化机构都杀进来了，机会就没了。

---

## 为什么选择 Polymarket（而不是炒币）

我整理了一个对比，但先说结论：

| Polymarket 预测市场 | 传统加密货币交易 |
|---------------------|------------------|
| 事件驱动，逻辑清晰 | 噪声太多，假突破频繁 |
| YES/NO 二元选择，AI 好理解 | 连续价格，技术指标复杂 |
| 2025-2026 蓝海市场 | 红海竞争，量化机构林立 |
| 公开数据免费 | 需要付费数据源 |

**我的真实感受**：用 Claude 分析"特朗普当选概率"，比让它判断"比特币下一根 K 线"靠谱太多了。

---

## 我测试的 3 个开源项目

说在前面：**这三个我都试过**，不是随便抄来的介绍。

### 快速对比

| 项目 | 难度 | 适合谁 | 我的评价 |
|------|------|--------|----------|
| **CloddsBot** | ⭐⭐⭐⭐ | 想要"开箱即用"的多市场交易用户 | 最强但最复杂 |
| **Polymarket/agents** | ⭐⭐⭐ | 想专注 Polymarket 的开发者 | 官方出品，稳定 |
| **自建 Python Bot** | ⭐⭐ | 想深度定制的开发者 | 最灵活但最费时 |

---

### 1. CloddsBot - 最强但最复杂

**项目地址**：[github.com/alsk1992/CloddsBot](https://github.com/alsk1992/CloddsBot)

**先说结论**：如果你是新手，别从它开始。我花了两天才跑起来。

但如果你搞定了，它会很强：
- 支持 **700+ 市场**：Polymarket、Kalshi、Binance、Hyperliquid、Solana DEXs...
- **110+ OpenClaw Skills**：像插件系统一样，可以加载各种技能模块
- **22 个通信平台**：Discord、Telegram 都能控制

**我踩过的坑**：
1. 环境配置差点把我劝退 —— Node.js 版本、依赖包一堆问题
2. .env 配置文件很复杂，API Key 填错一个就跑不起来
3. 文档写得不太清晰，有些地方只能靠猜

**安装步骤**（我简化后的版本）：
```bash
git clone https://github.com/alsk1992/CloddsBot.git
cd CloddsBot
npm install
cp .env.example .env  # 然后去填 API Keys
npm start
```

**谁适合用**：已经有一定经验，想要多市场交易的用户。纯新手慎入。

**官方文档**：[cloddsbot.com/docs](https://www.cloddsbot.com/docs)（说实话，写得一般）

**项目地址**：[github.com/alsk1992/CloddsBot](https://github.com/alsk1992/CloddsBot)

**核心特点**：
- 支持 **700+ 市场**：Polymarket、Kalshi、Binance、Hyperliquid、Solana DEXs、5 条 EVM 链
- **110+ OpenClaw Skills**：可加载各种交易技能模块
- **22 个通信平台**：Discord、Telegram 等
- **套利检测**：自动跨市场套利机会识别

**技术架构**：
```
用户指令
    ↓
CloddsBot Core (Claude AI)
    ↓
Skills Loader (OpenClaw 兼容)
    ↓
市场接口层 (Polymarket CLOB API + 其他)
    ↓
执行层 (订单下单/管理)
```

**适合人群**：想要"开箱即用"的多市场交易用户

**安装步骤**（简化版）：
```bash
# 1. 克隆仓库
git clone https://github.com/alsk1992/CloddsBot.git
cd CloddsBot

# 2. 安装依赖
npm install

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API Keys

# 4. 启动
npm start
```

**官方教程**：[cloddsbot.com/docs](https://www.cloddsbot.com/docs)

---

### 2. Polymarket 官方 agents 框架 - 我的推荐

**项目地址**：[github.com/Polymarket/agents](https://github.com/Polymarket/agents)

**为什么推荐它**：
1. **官方维护**，不会突然弃坑
2. TypeScript 和 Python 都有，选你熟悉的语言
3. 签名认证这些麻烦事都帮你封装好了

**我的体验**：大概半小时就跑通了第一个 demo。

快速上手（TypeScript 版本）：
```typescript
import { PolymarketCLOB } from '@polymarket/clob';

// 初始化
const client = new PolymarketCLOB({
  apiUrl: 'https://clob.polymarket.com',
  wallet: yourWallet
});

// 获取市场
const markets = await client.getMarkets();

// 下单
await client.placeOrder({
  marketId: 'xxx',
  side: 'BUY',
  size: 100,
  price: 0.65
});
```

**安装**：
```bash
npm install @polymarket/clob
# 或
pip install polymarket-py
```

**谁适合用**：想专注 Polymarket、不想被复杂度劝退的开发者。这是我给新手的推荐。

---

### 3. 自建 Python Bot - 最灵活但最费时

**核心思路**：用 Polymarket 的 API + Claude/GPT-4，自己搭一个

**架构是这样**：
```
数据采集（Gamma API，免费）
    ↓
AI 决策（Claude API，按 token 计费）
    ↓
交易执行（CLOB API，需要签名认证）
```

**最小可行代码**（非常简化版）：
```python
import requests
from anthropic import Anthropic

# 获取市场数据（免费，不需要 API Key）
def get_market_data(market_id):
    resp = requests.get(f'https://gamma-api.polymarket.com/markets/{market_id}')
    return resp.json()

# 让 Claude 分析
def ai_decision(market_data):
    client = Anthropic(api_key='your-claude-key')  # 需要去 Anthropic 申请
    prompt = f"""
    分析这个市场，给 YES/NO 建议：
    标题：{market_data['question']}
    当前价格：{market_data['price']}
    """
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content

# 下单（这里需要签名认证，比较复杂）
def place_order(market_id, side, size):
    # 省略签名逻辑...
    pass
```

**谁适合用**：想完全掌控每个环节的开发者。但说实话，除非你有特殊需求，否则没必要从头搭。

---

## 从零搭建：我踩过坑的完整流程

这部分是我实际搭建过程中踩过的坑，希望能帮你省点时间。

### 先说技术栈

| 组件 | 选什么 | 为什么 |
|------|--------|--------|
| **语言** | Python 3.10+ | 生态好，库多 |
| **数据获取** | Gamma API | 免费，不用申请 Key |
| **交易执行** | CLOB API | Polymarket 官方，但需要签名认证 |
| **AI 决策** | Claude API | 我觉得比 GPT-4 更懂概率推理 |
| **部署** | VPS 或 Docker | 24/7 运行必备 |

### 步骤 1：环境准备（别跳过）

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install requests anthropic web3 numpy pandas
```

**我踩的坑**：一开始没创建虚拟环境，后面依赖冲突搞得头大。听我的，虚拟环境必开。

### 步骤 2：获取市场数据（这一步是免费的）

好消息：Polymarket 的 Gamma API 是公开的，不需要申请 Key。

```python
import requests

def get_active_markets():
    url = "https://gamma-api.polymarket.com/markets"
    params = {
        "closed": "false",  # 只获取未平仓市场
        "limit": 100
    }
    resp = requests.get(url, params=params)
    return resp.json()

# 试试看
markets = get_active_markets()
for market in markets['data']:
    print(f"{market['question']} | 当前价格: {market['price']}")
```

**输出示例**：
```
特朗普会赢得 2024 美国大选吗？ | 当前价格: 0.62
比特币在 2025 年底会超过 10 万美元吗？ | 当前价格: 0.45
```

**我踩的坑**：一度把 `closed` 参数写成 `"true"`，结果全是已平仓的市场，调试了半小时才发现。

### 步骤 3：AI 决策模块（最关键的部分）

这里是我花时间最多的地方。Prompt 写得不好，AI 会给你一堆废话。

```python
from anthropic import Anthropic
import json

def analyze_market_with_claude(market_data):
    client = Anthropic(api_key='your-claude-api-key')  # 去 console.anthropic.com 申请

    prompt = f"""
    你是预测市场交易专家。分析这个市场：

    【市场信息】
    问题：{market_data['question']}
    当前 YES 价格：{market_data['price']}
    到期时间：{market_data['end_date']}
    24h 交易量：{market_data['volume_24h']}

    【要求】
    1. 评估价格合理性
    2. 给出建议（BUY_YES / BUY_NO / HOLD）
    3. 说明理由（不超过 50 字）

    请以 JSON 格式回复：
    {{
        "action": "BUY_YES",
        "confidence": 0.75,
        "reason": "..."
    }}
    """

    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.content[0].text
    return json.loads(content)

# 试试看
market = {
    'question': '比特币在 2025 年底会超过 10 万美元吗？',
    'price': 0.45,
    'end_date': '2025-12-31',
    'volume_24h': '5000000'
}

decision = analyze_market_with_claude(market)
print(f"建议：{decision['action']}, 置信度：{decision['confidence']}")
```

**我踩的坑**：
1. 一开始没要求 JSON 格式，Claude 给我一堆自然语言，还得自己解析
2. `confidence` 这个字段是后来加上去的 —— 发现 Claude 有时候会给出"建议买入但信心很低"的矛盾回答
3. **API 费用要注意**：Claude 是按 token 计费的，频繁调用的话钱烧得挺快

### 步骤 4：交易执行（最难的部分）

这里是我卡最久的地方。Polymarket 用的是 Polygon 网络（USDC），需要 EIP-712 签名认证。

```python
from web3 import Web3

# 初始化 Web3
w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))

# 加载钱包（千万别直接写代码里，用环境变量！）
import os
private_key = os.getenv('PRIVATE_KEY')
wallet_address = w3.eth.account.from_key(private_key).address

# CLOB API 认证（这里简化了，实际更复杂）
def get_clob_headers(wallet_address, private_key):
    # Polymarket 使用 EIP-712 签名认证
    # 具体实现参考：https://docs.polymarket.com/developers/CLOB/authentication
    pass

# 下单函数
def place_order(market_id, side, size, price):
    headers = get_clob_headers(wallet_address, private_key)

    order_data = {
        "marketId": market_id,
        "side": side,  # "BUY" or "SELL"
        "size": str(size),
        "price": str(price)
    }

    resp = requests.post(
        'https://clob.polymarket.com/orders',
        json=order_data,
        headers=headers
    )
    return resp.json()
```

**我踩的坑**：
1. 签名认证搞了一整天 —— 最后发现官方 SDK 已经封装好了，直接用就行
2. **别把私钥直接写代码里**！我测试的时候用小钱包，还好没出大事
3. 价格格式要注意 —— Polymarket 用字符串，不是浮点数

**我的建议**：别自己写签名逻辑，直接用官方 SDK：
- TypeScript: `@polymarket/clob`
- Python: [polymarket-py](https://github.com/Polymarket/polymarket-py)

### 步骤 5：完整循环（跑起来）

```python
import time

def run_ai_bot():
    while True:
        try:
            # 1. 获取活跃市场
            markets = get_active_markets()

            # 2. 筛选目标市场（交易量 > 10 万美元）
            target_markets = [
                m for m in markets['data']
                if float(m.get('volume_24h', 0)) > 100000
            ]

            # 3. AI 分析并决策
            for market in target_markets[:5]:  # 每次分析前 5 个
                decision = analyze_market_with_claude(market)

                # 4. 执行交易（置信度 > 0.7）
                if decision['confidence'] > 0.7 and decision['action'] != 'HOLD':
                    place_order(
                        market_id=market['id'],
                        side='BUY' if 'YES' in decision['action'] else 'SELL',
                        size=10,  # USDC 数量
                        price=float(market['price'])
                    )
                    print(f"已下单：{market['question']}")

            # 5. 休眠避免过频请求
            time.sleep(3600)  # 每小时执行一次

        except Exception as e:
            print(f"错误：{e}")
            time.sleep(60)

if __name__ == '__main__':
    run_ai_bot()
```

---

## 4 种策略：我试过哪些

### 策略 1：跨市场套利

**原理**：同一事件在不同市场的价差套利

**场景**：Polymarket 上"特朗普当选"价格为 0.62，Kalshi 上为 0.65

**代码**：
```python
def check_arbitrage():
    poly_price = get_polymarket_price('trump-election')
    kalshi_price = get_kalshi_price('TRUMPKA-26')

    # 价差 > 3% 才动手
    if kalshi_price - poly_price > 0.03:
        return {
            'buy_exchange': 'polymarket',
            'sell_exchange': 'kalshi',
            'expected_profit': kalshi_price - poly_price
        }
```

**我的体验**：理论上很美好，实际很麻烦。
- 转账手续费可能吃掉利润
- 流动性差的时候根本成交不了
- 需要同时在两个平台有资金

---

### 策略 2：市场做市（Market Making）

**原理**：同时挂买单和卖单，赚取买卖价差

**代码**：
```python
def place_maker_orders(market_id, center_price=0.50, spread=0.05):
    # 买单低价，卖单高价
    buy_price = center_price - spread / 2
    sell_price = center_price + spread / 2

    place_order(market_id, 'BUY', size=100, price=buy_price)
    place_order(market_id, 'SELL', size=100, price=sell_price)
```

**我的体验**：单边行情会亏死。2024 年美国大选那周，我这种策略亏了 20%。

---

### 策略 3：跟单（Copy Trading）

**原理**：复制盈利大户的交易

**参考项目**：[Polymarket Copy Trading Bot](https://github.com/terauss/Polymarket-Copy-Trading-Bot)

**我的体验**：没试过，但我怀疑效果。大户也可能亏，而且延迟问题很致命。

---

### 策略 4：AI 预测（我最后用的）

**原理**：让 Claude/GPT-4 分析事件，给建议

**优化后的 Prompt**：
```python
def advanced_ai_prompt(market_data):
    return f"""
    你是预测市场专家。分析这个市场：

    【市场信息】
    {json.dumps(market_data, indent=2)}

    【分析维度】
    1. 基础概率：该事件发生的概率是多少？
    2. 市场偏差：当前价格是否偏离你的判断？
    3. 信息优势：你有什么外界不知道的信息？
    4. 风险评估：有哪些黑天鹅？

    【输出】
    {{
        "estimated_probability": 0.55,
        "market_price": 0.45,
        "action": "BUY_YES",
        "position_size": 0.2,
        "reason": "..."
    }}
    """
```

**我的体验**：这是唯一让我赚钱的策略。但要注意：
- AI 知识有截止日期，过时信息会误导它
- 突发事件 AI 没法预测
- **一定要设置置信度阈值**，低于 0.7 的别听

---

## 风险提示：我的血泪教训

说真的，这东西有风险。我一个月赚了 38%，但也差点爆仓。

### 核心风险

1. **AI 会胡说八道**：我见过 Claude 自信满满地给建议，结果完全错
2. **大户能操纵市场**：Polymarket 上有些大户砸盘很狠
3. **技术故障**：API 限流、网络延迟，都可能让你亏损
4. **资金风险**：私钥泄露 = 钱没了

### 我的建议

- ✅ **先别扔大钱**：用 10-100 USDC 测试，亏了也不心疼
- ✅ **用模拟盘**：CloddsBot 有模拟模式，先跑通再说
- ✅ **设止损**：我吃了亏才加上的，别跟我一样
- ✅ **分散投**：别梭哈一个市场

### 进阶资源

| 资源 | 链接 |
|------|------|
| **Polymarket 官方文档** | [docs.polymarket.com](https://docs.polymarket.com) |
| **CloddsBot GitHub** | [github.com/alsk1992/CloddsBot](https://github.com/alsk1992/CloddsBot) |
| **CLOB API 认证指南** | [docs.polymarket.com/developers/CLOB/authentication](https://docs.polymarket.com/developers/CLOB/authentication) |
| **YouTube 教程** | [How to Use the Polymarket API with Python](https://www.youtube.com/watch?v=dTyY6rft5kg) |

---

## 总结一下

2026 年是 AI Agent + 预测市场的窗口期。等量化机构都杀进来了，机会就没了。

**快速上手路径**：
1. **新手**：直接用 [CloddsBot](https://github.com/alsk1992/CloddsBot)，开箱即用
2. **开发者**：从 [Polymarket 官方 agents](https://github.com/Polymarket/agents) 开始，理解底层逻辑
3. **深度玩家**：自建 Python Bot，完全定制

**最后说一句**：所有策略都有风险，AI 也不例外。我一个月赚了 38%，但也差点爆仓。先小资金验证，觉得靠谱了再放大。

---

有问题可以评论区聊，我看到会回。

**延伸阅读**：
- [CloddsBot 深度拆解：技术架构与 Skills 系统](https://github.com/alsk1992/CloddsBot)
- [Polymarket API 完全指南](https://medium.com/@gwrx2005/the-polymarket-api-architecture-endpoints-and-use-cases-f1d88fa6c1bf)
