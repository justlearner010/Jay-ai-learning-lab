# Notes 导航设计说明

## 目标

将 Learning Lab 定位为笔记地图和导航入口，而不是笔记内容的第二份副本。所有历史笔记和后续笔记继续在 `justlearner010/jay-ai-engineering-notes` 独立仓库中维护。

## 架构

```text
notes/
  README.md
  library/                 # Git submodule
    python/
    testing/
    algorithms/
    ai-engineering/
    web/typescript/
    journey/
    indexes/
```

- `notes/library/` 通过 Git submodule 指向 `https://github.com/justlearner010/jay-ai-engineering-notes.git`。
- 笔记源文件、提交和历史只属于子模块仓库。
- Learning Lab 只保存子模块提交指针与分类导航。
- 本地 Obsidian 可通过 `notes/library/` 直接浏览笔记。

## 分类导航

`notes/README.md` 提供以下入口：

| 分类 | 源路径 |
| --- | --- |
| Python 基础 | `python/basics/` |
| Python 工具链 | `python/tooling/` |
| 测试 | `testing/` |
| 算法 | `algorithms/` |
| AI 工程 | `ai-engineering/` |
| TypeScript | `web/typescript/` |
| 历史学习复盘 | `journey/weekly-reviews/` |
| 按主题索引 | `indexes/by-topic.md` |
| 按日期索引 | `indexes/by-date.md` |

导航页为每个分类提供 GitHub 绝对链接，并标注子模块内的本地路径。GitHub 用户使用绝对链接，Obsidian 用户通过本地路径浏览。

## 根 README 调整

Learning Lab 根 `README.md` 中的 `notes/` 项改为可点击入口，并明确说明：

- Learning Lab 是笔记导航层。
- 实际笔记位于独立的 `jay-ai-engineering-notes` 仓库。
- 完整克隆 Learning Lab 时应使用 `--recurse-submodules`。

## 子模块工作流

查看内容：

```bash
git submodule update --init --recursive
```

在 `notes/library/` 中修改笔记时，必须先在子模块仓库中提交并推送，然后再在 Learning Lab 中更新子模块提交指针。不在 Learning Lab 中复制笔记内容。

## 边界与失败处理

- 不复制或移动旧笔记，避免双份内容分叉。
- 不为每个分类创建重复子模块或符号链接。
- 只有当目标仓库可访问且默认分支已成功检出时，才提交 `.gitmodules` 和子模块指针。
- 现有的空目录 `notes/algorithm notes`、`notes/python notes` 和 `notes/typescript notes` 不包含文件，实施时删除，避免与真实分类混淆。
- 如果子模块添加或远程验证失败，不推送 Learning Lab。

## 验证标准

- `.gitmodules` 包含 `notes/library` 与正确的 GitHub URL。
- `git submodule status` 显示 `notes/library` 已检出 `main` 提交。
- 笔记分类、主题索引和日期索引在子模块中存在。
- `notes/README.md` 的 GitHub 链接都指向存在的分类路径。
- Learning Lab 根 README 能导航到 `notes/`。
- 子模块工作区干净，Learning Lab 提交只包含导航、`.gitmodules` 和子模块指针。
