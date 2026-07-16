## to do list 清单

### 近期要做的
---
#### Phase2任务 2026 06.21 - 2026 07.21
- [x] 2026-06-27：重构 `jay-first-cli-text-tool` 的 core layer，把纯文本处理逻辑和文件读取/Console 输出解耦
- [x] 2026-06-27：完善 Issue #7，重构 `build_parser()` / `parse_args(argv=None)`，让 pytest 可以传假参数测试 CLI parser
- [x] 2026-06-27：完善 Issue #2，补齐文件权限、解码失败、非法参数、无输出操作等错误处理与测试
- [ ] 为cli-text-tool 添加版本更新信息，记录下每个版本新增的内容、功能、测试
- [x] 增加 `--word`、`--top`
- [x] 补充错误处理和端到端测试
- [x] 拆分文件读取与纯文本处理
- [x] 明确 JSON/chunk 输出
- [ ] 更新 README 和版本号
- [ ] 为 CSAPP-Linux学习建立一个`csapp-linux-lab`仓库，记录着我们Phase2的副线路对于CS底层学习的产出
- [x] 算法 Week 1（06.22–06.28）：完成 Move Zeroes、Happy Number、Two Sum II，复刷 2 道 Hash Map 题
- [ ] 算法 Week 2（06.29–07.05）：完成 Container With Most Water、3Sum、4Sum，复刷 2 道 Hash Map 题
- [ ] 算法 Week 3（07.06–07.12）：完成 Minimum Size Subarray Sum、Longest Substring、Max Consecutive Ones III，复刷 2 道旧题
- [ ] 算法 Week 4（07.13–07.19）：完成 Fruit Into Baskets、Minimum Operations to Reduce X to Zero、Find All Anagrams，复刷 2 道旧题
- [ ] 07.20–07.21：更新[题集状态](./notes/library/algorithms/problem-set.md)，完成 Phase 2 算法复盘

#### Pytest 源码与开源协作副线（每周 5–7 小时，共 4 周）

- [x] Fork `pytest-dev/pytest` 为 `justlearner010/pytest`，配置 `origin` / `upstream` 并验证 `main` 零分叉
- [x] 建立 Python 3.14 editable 开发环境，通过 `testing/test_config.py`、tox py314 与完整 linting 基线
- [x] 将 pytest fork 以 `projects/pytest` 子模块关联到 Learning Lab，并建立[四周学习入口](./notes/library/testing/pytest-source-study/README.md)
- [ ] Week 1：完成命令入口、Config、Session 与 ExitCode 调用链，并运行生命周期黑盒实验
- [ ] Week 2：画出 Collector/Item 节点树，验证 node id、`--collect-only` 与 `-k`
- [ ] Week 3：验证 fixture 依赖、teardown 逆序及 pluggy hook 边界
- [ ] Week 4：复现历史 issue #13384，对照上游修复但不发布 PR，完成阶段复盘

#### 未来会做的：探索与思考

- [ ] 沉淀自己的学习系统，把每个新主题的学习沉淀成一个迅速搭建的**模版系统**，不需要自己一点一点搭建项目结构
- [x] 使用codex 进行每日学习的艾宾浩斯遗忘曲线的自动化，自动读取新增在GitHub上的新的笔记和内容，做好知识的retrieve、recall
- [ ] Phase3任务设计和构想，结合AI Agent学习路线以及自己感兴趣的进行任务方向确认
- [ ] 根据[立党AI学习研究完整教程第一期](https://www.youtube.com/watch?v=BqF6PUAXY1M)设计自己的minimal SW agent（可作为实际项目考虑）[视频总结](obsidian://open?vault=cs-ai-learning&file=incubator%2FMinimal%20SW%20Agent)
- [ ]
