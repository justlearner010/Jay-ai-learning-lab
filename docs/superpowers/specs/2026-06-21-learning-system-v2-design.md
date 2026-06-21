# Learning System v2 设计说明

## 目标

将 `Jay-ai-learning-lab` 建立为唯一活跃的学习系统入口，让日常记录保持轻量，将复盘与日志分离，并安全归档已不再适用的 `jay-ai-agent-learning-system`。

## 仓库职责

### `Jay-ai-learning-lab`

作为唯一活跃学习入口，管理阶段路线、轻量日志、周期总结、学习笔记和项目关联。

### `jay-ai-agent-roadmap-archive`

作为历史归档仓库。在 `learning-system-archive/` 中保存旧学习系统的完整受跟踪文件快照，并记录来源仓库、归档日期和最后提交。

### `jay-ai-agent-learning-system`

迁移完成后只保留迁移说明和新旧入口链接，随后在 GitHub 上标记为 Archived，不再接受日常更新。

## Learning Lab 目录结构

```text
logs/
summary/
  weekly/
  monthly/
  phases/
templates/
  daily-log.md
  weekly-summary.md
  phase-summary.md
roadmap.md
```

- `logs/` 保存可选的轻量日志。
- `summary/weekly/` 保存周总结。
- `summary/monthly/` 保存月度总结。
- `summary/phases/` 保存阶段总结。
- `templates/` 只保留服务于当前自由学习流程的模板。
- `roadmap.md` 只维护阶段方向与验收结果，不生成每日作业。

## 模板设计

### 轻量日志

```markdown
# YYYY-MM-DD

- 今天推进了什么：
- 证据或结果：
- 下一步最自然的动作：
```

日志不强制每天填写，不统计时长，不形成补记债务。

### 周总结

周总结只回答：

1. 本周真正推进了什么？
2. 有哪些可验证成果？
3. 哪个知识点变清楚了？
4. 哪些计划被删除或调整了？
5. 下周只保留哪个重点？

### 阶段总结

阶段总结记录阶段目标、主要成果、能力变化、放弃事项与下一阶段方向。它不评价每日任务完成率。

## 信息流

```text
可选日志 → 周总结 → 月度/阶段总结 → 更新 roadmap
```

日志只记录当下状态；总结负责提炼结论；`roadmap.md` 只接收经过复盘后确认的方向调整。

## 归档流程

1. 记录旧学习系统的最后提交哈希。
2. 检查受跟踪文件中的密钥、`.env` 和其他敏感信息。
3. 将受 Git 跟踪的文件快照复制到归档仓库的 `learning-system-archive/`。
4. 新增 `learning-system-archive/ARCHIVE-METADATA.md`，记录来源 URL、日期、提交哈希和归档原因。
5. 更新归档仓库 README 中的导航入口并推送。
6. 验证 GitHub 上的快照内容与源提交清单一致。
7. 更新旧学习系统 README，指向 Learning Lab 和归档快照，然后推送。
8. 在上述推送全部成功后，将旧学习系统标记为 Archived。

## 安全与失败处理

- 只复制 `git ls-files` 列出的受跟踪文件，不复制 `.git/`、未跟踪文件或本机环境文件。
- 任何敏感信息扫描异常都会阻止归档推送。
- 归档仓库或旧仓库推送失败时，不执行 GitHub Archived 状态变更。
- 原仓库在最后一步之前始终保持可写，以便修正迁移说明或快照问题。
- 归档后不删除原仓库，保留完整 Git 历史。

## 验证标准

- 归档快照文件清单与旧学习系统的 `git ls-files` 输出一致，只多出归档元数据文件。
- 归档仓库和旧仓库远程主分支均与本地提交一致。
- 旧学习系统 README 能够访问 Learning Lab 和归档快照。
- GitHub 上的 `jay-ai-agent-learning-system` 最终显示为 Archived。
- Learning Lab 中的三类模板和 `summary/` 分层目录可直接使用。
