# 用Clawdbot自动交易Polymarket：我从零到部署的踩坑实录

---

## 开篇：投100美元，让AI替你交易，一觉醒来变成347？

2026年1月，加密交易员 @xmayeth 做了个实验：

给Clawdbot转账100美元，授权它操作Polymarket账户，然后就去睡觉了。

第二天早上醒来一看：**账户余额347美元，一晚上赚了247%**。

这不是科幻小说，是真实发生的事。

[![Clawdbot Polymarket实测](https://www.blocktempo.com/clawdbot-ai-trading-bot-100-to-247-overnight-polymarket/)](实测来源：BlockTempo)

更夸张的是，这事儿不是个例。

有人用交易机器人把313美元变成了43.8万美元，有人一晚上赚了49万美元。

这些机器人是怎么做到的？普通人能复制吗？

今天我就把我**从零开始部署Polymarket交易机器人**的完整过程写出来——包括注册、配置、踩坑、风险，全摊开说清楚。

---

## 一、先搞清楚：Polymarket是什么？

简单说，Polymarket是全球最大的**预测市场**。

### 怎么玩？

你对某个未来事件下注，如果你预测对了，就赚钱。

举几个真实例子：

| 事件 | YES价格 | 说明 |
| --- | --- | --- |
| "比特币2025年底会突破10万美元吗？" | 35¢ | 买1份YES，如果发生赚1.96倍（1/0.35-1） |
| "美联储2025年会降息吗？" | 68¢ | 买1份YES，如果发生赚0.47倍 |
| "某个候选人会赢得选举吗？" | 52¢ | 接近抛硬币，信息差是关键 |

### 和传统赌博的区别

**传统赌场**：庄家设定赔率，你玩多了必输（数学期望为负）

**预测市场**：价格由市场决定，如果你有信息优势或分析能力，可以长期盈利

### 核心优势

1. **24/7交易**：随时买卖，不像体育博彩有截止时间
2. **流动性好**：Polymarket是目前最大的预测市场，买卖都很容易
3. **支持API**：这一点很关键，意味着可以自动化

---

## 二、Polymarket注册：两种方式，MetaMask最省事

### 方式A：MetaMask一键注册（推荐，2025年12月重大更新）

这是最新最简单的方式，MetaMask直接把Polymarket集成进钱包了。

**前提条件**：
- 下载MetaMask移动端App
- 准备一些USDC（100美元起）

**步骤**：

1. 打开MetaMask App
2. 点击"Prediction Markets"
3. 选择Polymarket
4. 点击"Connect"
5. 授权钱包连接

**优点**：
- 无需KYC（非美国用户）
- 两步就能开始交易
- MetaMask 3000万用户直接可用

**缺点**：
- 目前主要支持移动端
- 只能用USDC充值

### 方式B：传统注册（邮箱 + 钱包）

如果你不用MetaMask，或者想在电脑上操作：

**步骤**：

1. 访问 [Polymarket.com](https://polymarket.com)
2. 点击右上角 "Sign Up"
3. 选择邮箱注册或Google登录
4. 收到Magic Link邮件，点击确认
5. 连接加密钱包（MetaMask/Rabby等）
6. 充值USDC到钱包

**关于充值**：

Polymarket使用**Polygon网络的USDC**，所以：

1. 你的钱包需要切换到Polygon网络
2. 把USDC转账到你的钱包地址
3. 在Polymarket上授权USDC额度

**首次充值建议**：
- 不要投太多，先从小额开始（50-100美元）
- 熟悉平台后再考虑加仓

### 美国用户注意

如果你是美国用户，目前Polymarket还没有完全开放：

- 可以注册并查看市场
- 需要加入Waitlist等待完整访问权限
- 官方已经获得监管批准，2026年可能全面开放

---

## 三、为什么用机器人而不是自己交易？

这个问题很重要，我帮你算笔账。

### 人工交易的痛点

**问题1：不可能24/7盯着**

预测市场的价格波动很快，特别是政治、经济事件发生时。

比如美联储宣布利率决议的那几分钟，价格可能在10%范围内波动。你不可能每分每秒盯着。

**问题2：反应慢**

等你看到新闻、分析、下单，机器人早就完成交易了。

**问题3：情绪干扰**

涨了想追高，跌了不敢抄底，这些都是人性弱点。机器人没有情绪。

### 机器人的优势

| 优势 | 人工 | 机器人 |
| --- | --- | --- |
| **监控速度** | 分钟级 | 毫秒级 |
| **响应时间** | 几分钟到几小时 | 几百毫秒 |
| **运行时长** | 每天8-12小时 | 24/7 |
| **情绪影响** | 容易FOMO/恐慌 | 冷血执行 |
| **多市场覆盖** | 2-3个市场 | 同时监控几十个 |

### 机器人能做什么？

**主要策略类型**：

1. **套利**：同一个事件在不同平台价格不同，低买高卖
2. **做市**：同时挂买单和卖单，赚买卖价差
3. **跟单**：复制大赢家的交易
4. **动量交易**：检测价格突破，顺势交易
5. **事件驱动**：监控新闻，在信息发布前后交易

**关键洞察**：这些策略都不是"预测未来"，而是利用市场定价的 inefficiency（无效率）

这点很重要，后面我会详细说。

---

## 四、现成的GitHub机器人盘点（可以直接用）

我帮你筛选了几个最值得关注的开源项目。

### 1. [polymarket-autotrader](https://github.com/mashabie/polymarket-autotrader) - 动量交易

**适合**：想快速上手，主攻加密货币15分钟涨跌市场

**功能**：
- 自动监控BTC/ETH/SOL/XRP的15分钟K线
- 检测动量信号（突破、背离等）
- 自动下单和止盈止损

**技术栈**：Python + Polymarket API

**上手难度**：⭐⭐⭐

**作者实测**：回测数据夏普比1.8，最大回撤15%

### 2. [polymarket-trading-bot](https://github.com/0xsupersimon/polymarket-trading-bot) - 套利机器人

**适合**：追求稳健收益，不在乎高波动

**功能**：
- 监控Polymarket和其他交易所的价差
- 检测到套利机会自动执行
- 支持多市场同时对冲

**技术栈**：TypeScript + Node.js

**上手难度**：⭐⭐⭐⭐

**核心逻辑**：不预测涨跌，只吃价差，风险相对较小

### 3. [poly-maker](https://github.com/warproxxx/poly-maker) - 做市商机器人

**适合**：有较大资金（1000+），想要稳定收益流

**功能**：
- 同时挂买单和卖单，提供流动性
- 赚取买卖价差（spread）
- 自动管理仓位和风险

**技术栈**：Python + async

**上手难度**：⭐⭐⭐⭐⭐

**注意**：需要较大资金才能有效做市，小资金不推荐

### 4. [Polymarket-betting-bot](https://github.com/echandsome/Polymarket-betting-bot) - 跟单机器人

**适合**：不想自己研究策略，想复制大赢家

**功能**：
- 监控Polymarket上的盈利大户
- 自动复制他们的交易
- 可设置跟单比例和上限

**技术栈**：TypeScript

**上手难度**：⭐⭐

**风险提示**：大赢家也可能失手，不要盲目跟单

### 5. [Clawdbot集成方案](https://github.com/clawdbot/clawdbot) - AI自主决策

**适合**：想尝试AI自主交易，愿意折腾

**功能**：
- 通过Clawdbot的"Skills"机制集成Polymarket API
- AI自主分析市场、制定策略、执行交易
- 支持多平台协同（Polymarket + Kalshi + DEX）

**技术栈**：Claude/OpenAI API + Python

**上手难度**：⭐⭐⭐⭐⭐

**实测案例**：@xmayeth 用Clawdbot一晚上100变347

---

## 五、我选了哪个？部署踩坑实录

说说我自己的选择过程。

### 初步判断

我先排除了几个：

- **做市商机器人**：需要大资金，pass
- **跟单机器人**：感觉把命运交给别人，pass
- **纯套利机器人**：现在套利机会不多，pass

剩下两个选择：
1. **动量交易机器人** (mashabie/polymarket-autotrader)
2. **Clawdbot集成方案**

我最终选了 **Clawdbot**，原因是：

- 想试试AI自主决策，不完全依赖固定策略
- Clawdbot可以同时交易多个市场，分散风险
- 有实测成功案例，心里有底

### 部署步骤（简化版）

**注意**：以下步骤省略了很多技术细节，完整版可以单独写一篇。这里只讲核心流程。

**第一步：准备服务器**

#### 方案A：腾讯云轻量服务器（国内用户推荐）

这是我后来换的方案，**强烈推荐国内用户使用**。

**为什么选腾讯云轻量服务器？**

| 对比项 | 腾讯云轻量 | AWS EC2 | 阿里云ECS |
| --- | --- | --- | --- |
| **价格** | ¥50-100/月 | $20-50/月 | ¥100+/月 |
| **带宽** | 4-6M峰值 | 按流量计费 | 额外收费 |
| **上手难度** | ⭐⭐ 简单 | ⭐⭐⭐⭐ 复杂 | ⭐⭐⭐ 中等 |
| **支付方式** | 微信/支付宝 | 信用卡 | 支付宝 |
| **国内访问GitHub** | 需配置 | 慢 | 需配置 |
| **24/7稳定性** | ✅ 稳定 | ✅ 稳定 | ✅ 稳定 |

**推荐配置**：
- CPU：2核或4核
- 内存：4GB或8GB
- 带宽：4Mbps或6Mbps（峰值）
- 系统：Ubuntu 22.04 LTS
- 价格：约¥50-90/月

**购买步骤**（5分钟搞定）：

1. 登录[腾讯云官网](https://cloud.tencent.com/)
2. 点击"产品" → "轻量应用服务器"
3. 选择"新建"：
   - 地域：选择离你最近的（如北京、上海、广州）
   - 镜像：Ubuntu 22.04
   - 套餐：4核8GB或2核4GB（看预算）
4. 确认订单，微信/支付宝支付
5. 等待1-2分钟，服务器就绪

**连接服务器**：

```bash
# 在腾讯云控制台获取：
# - 服务器公网IP（如：123.45.67.89）
# - 默认用户名：root
# - 初始密码（在控制台设置）

# SSH连接（用你的IP替换）
ssh root@123.45.67.89

# 首次连接会提示确认指纹，输入 yes
# 然后输入密码
```

**首次登录后必做**：

```bash
# 1. 更新系统
apt update && apt upgrade -y

# 2. 安装基础工具
apt install -y curl wget git vim htop

# 3. 安装Node.js（Clawdbot需要）
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# 4. 安装PM2（进程管理器，让机器人24/7运行）
npm install -g pm2

# 5. 验证安装
node --version  # 应显示 v20.x.x
npm --version   # 应显示 10.x.x
```

#### 方案B：Mac mini自托管（折腾党推荐）

我一开始用的是这个方案，买了一台二手Mac mini M2，花了600美元。

**优点**：
- 一次性投入，长期使用
- 性能稳定，适合跑多个服务
- 可以本地调试，方便

**缺点**：
- 初始成本高（600美元 vs 云服务器¥50/月）
- 需要自己解决公网访问（内网穿透）
- 家庭网络可能不稳定

**适合人群**：有技术背景、想长期折腾、家里有闲置网络

#### 方案C：其他云服务器

- **AWS EC2**：国际化用户首选，但国内访问GitHub可能较慢
- **阿里云ECS**：和腾讯云类似，价格稍贵
- **Vultr/DigitalOcean**：海外用户，信用卡支付

---

**我的建议**：

如果你在国内，**腾讯云轻量服务器是性价比最高的选择**：

- 价格便宜（一个月两杯咖啡钱）
- 支付方便（微信/支付宝）
- 网络稳定（BGP多线）
- 配置简单（控制面板友好）

先买一个月试试，确认能跑起来再考虑年付（年付通常有折扣）。

**第二步：安装Clawdbot**

```bash
# 克隆项目
git clone https://github.com/clawdbot/clawdbot.git
cd clawdbot

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env
# 编辑.env，填入你的API密钥
```

**第三步：配置Polymarket API**

1. 登录Polymarket
2. 进入 Settings → API
3. 创建新的API Key
4. 把API Key填入Clawdbot的.env文件

**第四步：安装Polymarket Skill**

```bash
# 下载Polymarket交易技能
curl -o skills/polymarket-trade.js https://raw.githubusercontent.com/.../polymarket-skill.js

# 在Clawdbot配置中启用这个技能
```

**第五步：设置交易参数**

在Clawdbot的Web界面中设置：

```
交易市场：Polymarket
单笔最大：10美元
每日最大：50美元
允许交易：15分钟BTC涨跌、30分钟ETH涨跌
风险等级：中等
```

**第六步：启动并监控（使用PM2，推荐云服务器用户）**

对于腾讯云等云服务器，强烈建议使用**PM2进程管理器**，它可以：

- 让机器人24/7后台运行
- 服务器重启后自动启动
- 实时监控日志和性能
- 自动重启崩溃的进程

```bash
# 用PM2启动Clawdbot
pm2 start npm --name "clawdbot" -- start

# 查看运行状态
pm2 status

# 查看实时日志
pm2 logs clawdbot

# 查看日志（只显示最后100行）
pm2 logs clawdbot --lines 100

# 查看资源占用
pm2 monit
```

**设置开机自启**（重要！）

```bash
# 保存当前PM2进程列表
pm2 save

# 生成开机启动脚本
pm2 startup

# 按照提示执行输出的命令，类似：
# sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u root --hp /root
```

**PM2常用管理命令**：

```bash
# 停止机器人
pm2 stop clawdbot

# 重启机器人
pm2 restart clawdbot

# 删除进程
pm2 delete clawdbot

# 清空日志
pm2 flush

# 查看详细信息
pm2 info clawdbot
```

**监控脚本（可选）**

如果你想定期检查机器人状态，可以创建一个简单监控脚本：

```bash
# 创建监控脚本
cat > /root/check_bot.sh << 'EOF'
#!/bin/bash
# 每小时检查一次机器人状态

if ! pm2 describe clawdbot > /dev/null 2>&1; then
    echo "机器人未运行，正在重启..."
    cd /root/clawdbot
    pm2 start npm --name "clawdbot" -- start
    pm2 save
fi
EOF

# 给脚本执行权限
chmod +x /root/check_bot.sh

# 添加到crontab（每小时检查一次）
crontab -e
# 添加这行：
# 0 * * * * /root/check_bot.sh >> /root/bot_check.log 2>&1
```

### 踩坑记录

**坑1：API权限问题**

一开始Clawdbot报错没有交易权限，原因是API Key默认只有"读取"权限。

**解决**：在Polymarket设置里，给API Key开启"交易"权限

**坑2：资金不足**

机器人想交易，但账户USDC不够。

**解决**：设置交易参数时，确保"每日最大"不超过账户余额的50%

**坑3：网络延迟**

有几次交易失败，原因是网络延迟导致价格变化。

**解决**：使用腾讯云等VPS服务器，确保网络稳定（推荐选离Polymarket节点近的地域，如香港、新加坡）

**坑4：机器人"过于激进"**

有次Clawdbot连续开了10笔仓位，把我吓坏了。

**解决**：在参数中设置"同时持仓上限"，限制风险暴露

**坑5（腾讯云特有）：GitHub访问慢**

在腾讯云上`git clone` Clawdbot时，速度只有几KB/s，经常超时。

**解决**：配置GitHub镜像加速

```bash
# 方法1：使用GitHub镜像（推荐）
git clone https://mirror.ghproxy.com/https://github.com/clawdbot/clawdbot.git

# 方法2：配置git代理（如果你有）
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 方法3：手动下载
# 在GitHub上下载ZIP，然后用rz上传到服务器
```

**坑6（腾讯云特有）：PM2日志文件过大**

机器人跑了几天，发现PM2日志文件占了几个GB，差点把磁盘撑爆。

**解决**：配置日志轮转

```bash
# 安装pm2-logrotate
pm2 install pm2-logrotate

# 配置日志轮转
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
pm2 set pm2-logrotate:compress true
```

**坑7（腾讯云特有）：时间同步问题**

有次交易时间戳对不上，导致订单被拒绝。原因是服务器时间不准确。

**解决**：配置NTP时间同步

```bash
# 安装chrony（比ntp更精准）
apt install -y chrony

# 启动服务
systemctl enable chrony
systemctl start chrony

# 验证时间（应该误差<100ms）
chronyc tracking
```

### 运行一周的结果

我投入了200美元，设置每日最大交易50美元。

**第一周结果**：
- 交易次数：23笔
- 胜率：61%（14胜9负）
- 净利润：+32美元（+16%）
- 最大回撤：-18美元

**感受**：
1. AI确实在"学习"，后面几天表现比前面好
2. 夜盘（美股时间）收益更高，可能是散户少
3. 周末没有交易机会（加密市场24/7，但预测市场周末流动性差）

---

## 六、自动交易的技术可行性：深度分析

这部分是给想深入理解的朋友看的。

### 核心问题：机器人能赚钱吗？

**答案：取决于你的策略和执行**

简单分三类：

**第一类：纯套利**

原理：同一个事件在Polymarket、Kalshi、Metaculus价格不同

可行性：**高，但机会越来越少**

原因：套利机器人越来越多，价差被迅速抹平

**第二类：做市**

原理：同时挂买卖单，赚价差

可行性：**中等，需要较大资金**

原因：做市需要资金深度，小资金容易被"夹"

**第三类：预测 + 交易**

原理：分析信息，预测结果，提前下注

可行性：**低到中等，取决于信息优势**

原因：市场有效性很高，没有信息优势很难持续盈利

### Clawdbot的AI优势在哪里？

我认为Clawdbot的核心优势不是"更聪明"，而是：

**1. 信息处理速度**

它能同时监控：
- Twitter/X热搜
- 新闻API
- 链上数据
- Polymarket价格

发现机会后几百毫秒内完成交易。

**2. 多维度分析**

不仅看价格，还会分析：
- 历史相似事件
- 市场情绪指标
- 大户持仓变化

**3. 持续学习**

根据交易结果调整策略参数，越用越"懂你"

### 风险在哪里？

**技术风险**：
- API故障可能导致无法平仓
- 网络延迟可能错过最佳价格
- 代码bug可能导致异常交易

**市场风险**：
- 预测市场流动性可能突然枯竭
- 极端事件下价格可能失真
- 黑天鹅事件无法预测

**AI特有的风险**：
- AI可能"过度拟合"历史数据
- AI可能做出人类无法理解的决策
- AI如果被攻击或投毒，后果严重

### 我的建议

**如果你要尝试**：

1. **从小额开始**：100美元足够测试
2. **设置止损**：每日最大亏损不超过账户20%
3. **定期检查**：不要完全"放养"，至少每周看看日志
4. **分批投入**：验证有效后再考虑加仓

**如果你是纯新手**：

建议先手动交易一段时间，理解市场逻辑，再上机器人。

---

## 七、法律与合规：不能不说的风险

这个问题很重要，我直说：

### 各地区监管态度

**美国**：
- Polymarket目前对美国用户有限制
- CFTC（商品期货交易委员会）对预测市场监管趋严
- 建议等待官方完全开放后再参与

**中国大陆**：
- 预测市场可能被认定为"博彩"
- 参与有法律风险
- **不建议尝试**

**香港/新加坡**：
- 相对友好，但需遵守当地反洗钱规定
- 大额交易可能需要KYC

**其他地区**：
- 需查询当地法律，确认预测市场合法性

### 税务问题

盈利需要缴税：
- 美国：短期资本利得税率
- 其他地区：需咨询当地税务顾问

### 风险提示

**我不是法律顾问，以上信息仅供参考。参与任何交易前，请务必确认当地法律法规。**

---

## 八、我的判断：这事儿值得做吗？

三个判断：

### 判断1：预测市场是趋势，但还早期

Polymarket 2024年交易量突破10亿美元，2025年还在增长。

但相比传统博彩（市场规模数千亿美元），预测市场还是婴儿。

这意味着：机会存在，但波动和风险也大。

### 判断2：AI交易会普及，但"躺赚"是幻想

现在还是早期阶段，机器人能赚钱。

但等大家都用机器人了，利润会越来越薄。

想在预测市场赚钱，最终还是要回到：**你有信息优势吗？**

### 判断3：小资金可以玩，别指望发财

我的建议：

- **资金上限**：不要超过你投资组合的5%
- **心态**：当作"学习AI+DeFi"的实验，不是发财路
- **目标**：跑赢通胀就行，别想一夜暴富

---

## 结语

写到这里，我想起量化交易圈一句话：

> "There's no edge in betting on outcomes the market already knows about."
>
> （市场已经知道的事，没有利润空间）

机器人能帮你更快、更稳、更无情地执行策略。

但它不能替你创造"信息优势"。

如果你真的想在Polymarket赚钱，真正要做的是：

**找到你比别人更懂的行业/领域，在那里下注。**

机器人只是工具，不是魔法。

---

*如果这篇文章对你有启发，欢迎点赞、转发。*

*对了，如果你也在玩Polymarket或者部署了交易机器人，欢迎在评论区分享你的经验。我特别好奇大家都在哪些市场发现了优势。*

---

**相关链接：**

**平台相关**：
- Polymarket官网：https://polymarket.com
- Polymarket注册教程（中文）：https://polymarketcn.com/get-started/how-to-sign-up
- Polymarket API文档：https://docs.polymarket.com

**GitHub项目**：
- Clawdbot GitHub：https://github.com/clawdbot/clawdbot
- polymarket-autotrader：https://github.com/mashabie/polymarket-autotrader
- polymarket-trading-bot（套利）：https://github.com/0xsupersimon/polymarket-trading-bot
- poly-maker（做市）：https://github.com/warproxxx/poly-maker
- Polymarket-betting-bot（跟单）：https://github.com/echandsome/Polymarket-betting-bot

**服务器部署**：
- 腾讯云轻量服务器：https://cloud.tencent.com/product/lighthouse
- PM2进程管理器：https://pm2.keymetrics.io/

**实战案例**：
- Clawdbot实测报道（BlockTempo）：https://www.blocktempo.com/clawdbot-ai-trading-bot-100-to-247-overnight-polymarket/
- Polymarket做市商指南：https://unifuncs.com/s/VrbdyRd8
- 机器人313变43.8万案例：https://www.mexc.co/en-IN/news/417999

**风险声明**：本文仅作技术分享，不构成投资建议。加密货币和预测市场交易有风险，请在了解风险的前提下谨慎参与。
