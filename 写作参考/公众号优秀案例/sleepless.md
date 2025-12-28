Sleepless Agent 是一个开源项目，它把 Claude Code CLI 包装成一个可以 24/7 持续运行的后台服务。你可以在睡觉前提交开发任务，AI 会在夜间自动编写代码、运行测试、创建 Pull Request，第二天早上起来直接 Review 代码就行。听起来很科幻对吧？



这个项目最大的价值在于：如果你订阅了 Claude Max（$200/月），白天工作时可能只用掉 20-30% 的额度，剩下 70% 在夜间闲置。Sleepless Agent 让你充分利用这些闲置额度，把 AI 变成一个真正的"不眠开发团队"。

（说个福利：需要低成本使用ClaudeCode可以联系易安：20133213，原生claude帐号）

最近我花了几天时间测试它的 GitHub 集成功能。从环境配置到成功创建 Pull Request，整个过程遇到了不少坑，也产生了很多思考。

最重要的是，我想明白了一个问题：



AI Agent 到底能不能完全自动化开发项目？



为什么要折腾这个？
说实话，一开始我对这种"睡觉也能写代码"的概念是半信半疑的。真的能做到吗？代码质量怎么样？会不会跑偏？GitHub 集成靠谱吗？带着这些疑问，我决定今天彻底测试一下。如果真的能用，那每个月 $200 的 Claude Max 订阅就物超所值了。如果不行，至少也能搞清楚这类工具的局限性在哪里。

从零开始配置
图片
第一个问题：如何快速上手？
装完 Sleepless Agent 之后，我第一个问题就是：这玩意儿怎么用？README 写得挺详细，但我想快速搞明白最小可用流程是什么。

Claude 给我梳理了一遍，其实核心就三步：

环境准备部分比较简单。首先确保 Python 3.11 以上版本，然后安装依赖，创建配置文件。关键是配置文件里有几个地方必须改。最重要的是 API Key，需要从 Anthropic 控制台获取一个 User Key（不是普通的 API Key）。另外还要配置使用量阈值，白天设置成 95%，晚上设置成 96%，这样可以最大化利用订阅额度。

第一次运行的时候我有点懵。文档里给了三种方式，我问了 Claude：“分别介绍下这三种方式的区别？”Claude 解释说，前台运行最简单，就是直接跑 python -m sleepless_agent daemon，但缺点是占用终端，一关掉就停了。nohup 方式可以真正后台运行，但管理起来不太方便，要用 ps 命令找进程号，停止的时候还要手动 kill。最推荐的是用 tmux 或 screen，既能后台运行，又能随时 attach 进去查看日志。

我选择了 tmux 方式，开了个新 session 跑起来。用 sle check 命令看了一眼状态，发现 daemon 已经在跑了，但没有任务在执行。接下来就该测试 GitHub 集成了。

GitHub 集成
在测试 GitHub 之前，我问了一个关键问题：“它能运行什么样的任务，可以自定义吗，比如开发一个全新的项目，自动提交到 GitHub？”Claude 给了个很详细的回答。Sleepless Agent 本质上就是调用 Claude Code CLI，所以 Claude Code 能做的事情它都能做。任务分两种类型：



第一种是 Random Thoughts，就是不带 -p 参数的任务，用来记录灵感和想法。这种任务执行完会自动提交到 thought-ideas 分支，不会创建 PR，主要用于日常记录。



第二种是 Serious Tasks，带 -p 参数指定项目名称。这种任务会创建独立的 feature 分支，执行完成后自动 commit 和 push，然后可以手动创建 PR 进行 code review。

理论上听起来很完美，但要让它真正工作，还需要配置几个东西。

首先是 Git 配置。打开 config.yaml，把 git.enabled 改成 true，use_remote_repo 也改成 true，然后填写远程仓库地址。这里有个坑我后面会说到。

其次是多代理工作流。这个特别重要。图片

Sleepless Agent 用了三个 Agent 协作：Planner 负责分析任务和制定计划，Worker 负责执行任务，Evaluator 负责验证代码质量。如果只开启 Worker，执行效果会很差，可能只生成一个 README 就结束了。所以这三个必须全开。



最后是 GitHub CLI 认证。这个必须先做，不然推送不了代码。

gh auth login 的小插曲

我跟 Claude 说：“辅助我完成 gh auth login”。



它给我列出了完整步骤。运行 gh auth login 之后，会问你要登录哪个账号（GitHub.com 还是 GitHub Enterprise），我选 GitHub.com。然后问用什么协议，我选 HTTPS（后面会说为什么不选 SSH）。接着问用什么方式认证，我选了 Browser。



这时候会生成一个设备码，打开浏览器访问 github.com/login/device，输入设备码，授权成功。回到终端，会提示 “Logged in as yiancode”。



验证一下：gh auth status，输出显示已经登录，token 包含了 repo、gist、read:org 权限。完美。接下来就可以创建远程仓库了。我用 GitHub CLI 创建了一个新仓库：

gh repo create sleepless-workspace --public --description "Sleepless Agent workspace for task execution"
仓库地址是

 
https://github.com/yiancode/sleepless-workspace.git
然后把这个地址填到 config.yaml 的 remote_repo_url 里。



SSH vs HTTPS 的坑
一开始我图方便，配置的是 SSH 地址：git@github.com``:yiancode/sleepless-workspace.git。结果后面 push 的时候报错了：

Permission denied (publickey).fatal: Could not read from remote repository.
我一看就知道是 SSH key 的问题。但我不想再配置 SSH key，因为 GitHub CLI 已经用 HTTPS 认证过了。所以我直接把配置改成了 HTTPS：

remote_repo_url:https://github.com/yiancode/sleepless-workspace.git
改完之后 push 就成功了。这个教训就是，如果你已经用 gh auth login 认证过，那就直接用 HTTPS，不要折腾 SSH。

提交第一个测试任务
图片配置全部搞定之后，我对 Claude 说：“提交一个测试任务，测试 GitHub 集成”。我想测试的是完整的开发流程，所以提交了一个稍微复杂点的任务：

python-msleepless_agentthink "创建一个完整的 PythonCLI 工具项目，包含：1. hello.py 主脚本使用 argparse 处理命令行参数2. 支持 --name 参数来自定义问候语3. 支持 --verbose 标志显示详细信息4. requirements.txt5. README.md 说明如何使用6. 添加适当的注释和文档字符串" -pcli-tool-test
任务提交之后，daemon 自动开始执行。我用 tail -f daemon.log 看着日志滚动：

17:43:23 | scheduler.dispatch available_slots=1 dispatching_tasks=117:43:23 | Task 2 marked as in_progress17:43:23 | task.start description="创建一个完整的 Python CLI 工具项目..."
然后就是 Planner 开始分析，制定了详细的执行计划。接着 Worker 开始执行，创建文件、编写代码。最后 Evaluator 验证代码质量，确认完成。整个过程用了 149 秒，大概 2 分半。

验证执行结果
任务完成后，我立刻去看 Git 提交记录：

git log --oneline -3
输出显示：

8566946 Implementtask#2: 创建一个完整的 PythonCLI 工具项目...a4546eeImplementtask#1: 创建一个简单的 HelloWorldPython 脚本...767288bInitialcommit
代码已经自动提交了！而且 commit message 写得很规范。再看看远程分支：

gh api repos/yiancode/sleepless-workspace/branches | jq -r '.[].name'
输出：

mainproject/cli-tool-testproject/github-testtasks
所有分支都成功 push 到 GitHub 了。但这里有个小问题，我后面会说。

文件创建位置的问题
打开 daemon.log，我发现了几行警告：

17:45:52 | Skipping file outside workspace repo: /private/tmp/README.md17:45:52 | Skipping file outside workspace repo: /private/tmp/hello.py17:45:52 | Skipping file outside workspace repo: /private/tmp/requirements.txt
原来 Worker Agent 把文件创建到了 /private/tmp/ 目录，而不是项目的 workspace 目录。这导致这些文件没有被 Git 追踪。



查看 workspace/projects/cli-tool-test/ 目录，里面只有一个 README.md，记录了任务的执行计划和状态。实际的代码文件都在 /private/tmp/ 里。

这个问题目前还没完美解决。我猜测是 Claude Code SDK 的工作目录配置问题。临时的解决办法是，在任务描述里明确指定文件路径，让它创建到正确的位置。

创建 Pull Request
验证完提交之后，我说：“帮我创建 Pull Request”。Claude 执行了创建 PR 的命令，但失败了：

no commits between main and project/cli-tool-test
我一愣，怎么会没有差异？明明刚才还提交了代码。

Claude 帮我分析了一下，原因是 daemon 在推送的时候用了 git push --all，这会把所有提交推送到所有分支。结果 main 分支和 feature 分支完全一样，没有差异，自然无法创建 PR。

手动创建测试分支
为了演示完整的 PR 流程，我们决定手动创建一个测试分支：

git checkout -b feature/pr-demo mainecho "# GitHub PR 演示" > PR_DEMO.mdgit add PR_DEMO.mdgit commit -m "docs: Add GitHub PR demonstration"git push -u origin feature/pr-demo
这样 feature/pr-demo 分支就比 main 多了一个 commit，可以创建 PR 了。

成功创建 PR
接下来用 GitHub CLI 创建 PR：

gh pr create --repo yiancode/sleepless-workspace \  --head feature/pr-demo \  --base main \  --title "🎉 GitHub 集成测试完成 - PR 创建演示" \  --body "这个 PR 演示了 Sleepless Agent 的完整 GitHub 集成流程..."
成功！PR 地址是：https://github.com/yiancode/sleepless-workspace/pull/1至此，从任务提交到代码提交，再到创建 PR，整个流程全部跑通了。

图片

深入思考：AI Agent 到底能做什么
测试完 GitHub 集成之后，我陷入了思考。我问了 Claude 一大堆问题，这些问题可能也是很多人关心的：



"这个工具到底是不是真的可以睡觉也能干活？"



"听起来好像还是需要人工确认很多东西，那为什么不直接手动做？"



"如果真的要从 0 到 1 开发一个项目，是不是还需要人类做大量前期工作？比如 UI/UX 设计、技术选型、架构设计？"



"如何确保 AI 不会跑偏，比如实现了一个功能但方向完全错了？"



Claude 给的回答让我豁然开朗。



不是完全无人值守，而是协作开发
图片

首先要纠正一个误区：很多人可能以为，用了 Sleepless Agent 就可以睡觉前说一句"帮我做个电商网站"，第二天起来整个项目就完成了。

这是不可能的，也不应该这样。



真实的协作模式是：人类充当产品经理、架构师和 Code Reviewer，AI 充当开发团队。



人类负责定义需求和目标，做技术选型和架构设计，把大任务分解成具体的小任务，然后 Review 代码质量。AI 负责编写代码，创建测试，生成文档，处理重复性任务。



换句话说，你还是要做 PM、架构师、Reviewer 的工作，但不需要做码农的工作了。

为什么还需要人类
Claude 举了几个例子说明为什么人类不可或缺。



产品决策方面。AI 无法回答"是否要添加这个功能"、“用户真正需要什么”、"优先级如何排序"这些问题。这需要人类根据商业价值和用户需求做判断。



技术选型方面。选择用什么技术栈不仅仅是技术问题，还涉及团队能力、长期维护成本、扩展性要求、预算限制等非技术因素。AI 可以提供建议，但最终决定必须人类来做。



质量把关方面。每个 PR 都需要人类检查代码逻辑是否正确，有没有安全问题，性能如何，是否真的符合需求。不能盲目 Merge AI 生成的代码。



从 0 到 1 搞一个真实流程

我继续追问：“如果真的要用 Sleepless Agent 从零开发一个项目，具体流程应该是什么样的？”

Claude 给了一个非常详细的回答。



阶段 0 是人类必须做的前期工作。你需要写一份项目需求文档，列出核心功能、技术栈选择、优先级划分。这部分工作 AI 帮不了你，因为它不知道你要做什么，为什么要做，给谁用。



比如你要做一个任务管理系统，你得明确：用户系统要不要做？任务分类怎么设计？要不要团队协作功能？用什么数据库？部署到哪里？这些决策必须人类做。



阶段 1 是任务分解。这一步特别关键。你要把项目分解成非常具体、可执行的任务。举个例子，不能只说"实现用户系统"，这太宽泛了。应该说"实现用户注册功能，包含 email 格式验证，密码强度检查（8位以上含数字和字母），发送验证邮件，数据库存储（加密密码），返回 JSON 响应，单元测试"。这种级别的具体性，AI 才能准确执行。



阶段 2 是迭代开发。这是 Sleepless Agent 发挥作用的地方。晚上睡觉前，花 30 分钟提交 3 到 5 个具体任务。然后去睡觉。夜间 AI 自动执行所有任务，编写代码、测试、文档，创建 PR。早上起来，花 1 小时 Review 每个 PR，检查代码质量，验证是否符合需求，Merge 或者提出修改意见。



就这样重复 4 到 7 天，一个中小型项目就完成了。



时间对比
图片

我问 Claude：“这样做到底能节省多少时间？”



Claude 给我算了一笔账：



传统开发一个项目，需求分析 4 小时，架构设计 2 小时，任务分解 1 小时，代码实现 40 小时，测试调试 20 小时，文档编写 8 小时，总计 75 小时。



用 Sleepless Agent，需求分析还是 4 小时，架构设计还是 2 小时，任务分解还是 1 小时，但代码实现只需要 2 小时（Review），测试调试只需要 3 小时（Review），文档编写只需要 1 小时（Review），总计 13 小时。节省了 62 小时，效率提升大约 85%。



但注意，前期工作（需求、架构、任务分解）无法省略，Review 时间也不能压缩，因为这是质量把关的关键。人类仍然需要投入 13 小时，只是这 13 小时都花在了更有价值的事情上，不是在写重复代码。



如何确保不跑偏？
我又问了一个关键问题：“如何确保 AI 不会跑偏？

比如实现了一个功能但方向完全错了？”Claude 说有几个机制保证这一点。



第一是：任务粒度任务足够具体，AI 就没有太大发挥空间。

如果你只说"实现用户系统"，AI 可能会做出各种猜测。但如果你说"实现用户注册功能，包含 A、B、C、D 四个具体要求"，AI 就只能照着做，不太可能跑偏。



第二是：多代理验证。

Planner 会先分析任务，制定详细计划，这个计划其实就是对任务的理解。Worker 按照计划执行。Evaluator 最后验证执行结果是否符合任务要求。这三个环节相互校验，大幅降低了出错概率。



第三是：人类 Review。

每个 PR 都需要人类审核。如果发现方向错了，立刻打回重做。因为任务颗粒度小，每个任务只需要几分钟到十几分钟，即使做错了，返工成本也不高。



第四是快速迭代。

不要一次性提交 20 个任务，应该每次提交 3 到 5 个，快速得到反馈，及时调整方向。这样即使前面几个任务方向有偏差，也能马上纠正，不会影响后续任务。



Slack 集成
我还问了一个实用问题：“CLI 模式每次都要手动提交任务，有没有更方便的方式？”Claude 说可以用 Slack 集成。Sleepless Agent 支持 Slack Bot，你可以在手机上直接发消息提交任务。晚上躺在床上，掏出手机，在 Slack 里发几条消息：

/think -p my-project 实现功能 A/think -p my-project 实现功能 B/think -p my-project 实现功能 C
然后就可以睡觉了，Agent 会自动处理。第二天早上起来，在手机上就能看到执行结果和 PR 链接。这比每次都要打开电脑、切换到终端、输入命令方便多了。

哪些项目适合用 Sleepless Agent
图片聊了这么多，我总结了一下什么样的项目适合用 Sleepless Agent。



个人 Side Project ：你有很多想法，但时间有限，想快速验证想法，持续迭代优化。这种场景下 Sleepless Agent 简直完美。



技术学习项目：你想学习新技术栈，实践最佳实践，创建示例代码。让 AI 帮你写代码，你专注于理解和学习。



技术债务清理：添加测试，重构代码，更新文档，依赖升级。这些事情重要但枯燥，让 AI 做最合适。



工具和脚本开发同样适合：

自动化脚本、CLI 工具、数据处理、爬虫程序。这些项目需求明确，逻辑清晰，AI 可以做得很好。



但也有一些场景需要谨慎。

企业级项目要小心。复杂流程和审批，多团队协作，严格的合规要求。这种项目不适合完全自动化。

实时协作场景也不太合适。需要即时沟通，频繁的需求变更，快速响应。这种场景下 AI 的滞后性会成为问题。

高度定制化需求也要谨慎。复杂的业务逻辑，大量人工决策，特殊的行业要求。AI 可能理解不了你的业务逻辑。

遇到的所有坑总结
测试了一整天，踩了不少坑，这里统一总结一下：



第一个坑是 SSH vs HTTPS。

最初配置了 SSH 地址，结果 push 的时候报权限错误。因为 GitHub CLI 已经用 HTTPS 认证了，SSH 需要单独配置密钥。解决办法就是直接用 HTTPS，省事。



第二个坑是文件创建位置。

Worker 创建的文件跑到了 /private/tmp/ 目录，而不是项目 workspace。导致文件没有被 Git 追踪。目前的临时解决办法是在任务描述里明确指定文件路径。根本原因可能是 Claude Code SDK 的工作目录配置问题，这个还需要进一步调查。



第三个坑是 PR 无法创建。

用 git push --all 推送的时候，所有提交都被推到了 main 分支，导致 feature 分支和 main 分支没有差异，无法创建 PR。解决办法是确保 feature 分支独立开发，或者手动创建差异化提交。



第四个坑是多代理工作流配置。

一开始我只开启了 Worker，结果任务执行得很敷衍，只生成了一个 README 就结束了，完全没有实际代码文件。后来把 Planner 和 Evaluator 都开启，执行质量立刻提升了。这三个 Agent 必须全开，缺一不可。

最后的思考
研究了几天，我对 Sleepless Agent 有了更深刻的理解。



它不是银弹，但是一个强大的生产力工具。



核心价值在于，充分利用 Claude Max 订阅，把人类时间从编码解放到决策和设计，实现 24/7 持续开发不浪费夜间时间，通过人类 Review 保持高质量。



使用要点是，人类负责"What"和"Why"，AI 负责"How"，通过 Review 保证质量，小步迭代快速反馈。时间上确实能节省大约 85% 的编码时间，但前期规划和 Review 不能省。实际人类投入大概是传统开发时间的 15% 到 20%，但这些时间都花在了更有价值的事情上。

最重要的认知是：AI Agent 是你的开发团队，不是魔法。



你仍然需要做产品经理、架构师和 Code Reviewer 的工作。你要定义需求，做技术选型，分解任务，Review 代码。但你不需要自己写那些重复的 CRUD 代码，不需要自己写单元测试，不需要自己写 API 文档。



这些重复性的、规范化的工作，AI 可以做得很好。而那些需要创造性思维、商业判断、用户洞察的工作，还是需要人类来做。



说到底，Sleepless Agent 改变的不是"能不能自动化开发"，而是"如何更高效地协作开发"。它让人类可以专注于更有价值的工作，把繁重的编码任务交给 AI。这才是 AI 辅助开发的正确打开方式。



测试用的仓库在这里：

https://github.com/yiancode/sleepless-workspace



第一个 Pull Request：

https://github.com/yiancode/sleepless-workspace/pull/1



项目还在持续完善中，如果你也在探索 AI 辅助开发，欢迎交流讨论，微信：20133213。

