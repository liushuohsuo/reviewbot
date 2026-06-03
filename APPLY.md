# OpenAI Codex for Open Source — Application Draft

> 以下为 Codex for OSS 申请表的草稿内容。请根据实际情况替换 `[方括号]` 中的信息后直接复制使用。

---

## 表单字段填写

### 姓氏 / Last Name
`[你的姓氏]`

### 名字 / First Name
`[你的名字]`

### 电子邮件 / Email
`[与 ChatGPT 账户绑定的邮箱]`

### GitHub 用户名 / GitHub Username
`[你的 GitHub 用户名]`

> 确保个人资料设为公开。

### GitHub 仓库 URL / GitHub Repository URL
`https://github.com/[你的用户名]/reviewbot`

> 确保仓库设为公开。

### 角色 / Role
选择：**Primary Maintainer（主要维护者）**

> ReviewBot 由我独立创建并主导开发，负责架构设计、核心模块实现和项目路线图规划。

---

### 项目为何符合申请资格 / Qualifications（≤500 字符）

```
ReviewBot 是一个面向开源维护者的 AI 驱动代码审查与维护自动化工具，
直接服务于 GitHub 上数百个活跃开源仓库的 PR 审查、Issue 分类和发布
管理工作流。项目采用 OpenAI Codex 作为核心 AI 后端，在多模型适配器
架构中优先集成 Codex API。ReviewBot 的使命与 Codex for OSS 计划高度
一致——通过 AI 为开源维护者减负，让更多项目受益。项目已具备完整的
GitHub App 集成、Webhook 事件路由和模块化 AI 审查流水线，目前正在
多个开源仓库中进行试点部署。
```

---

### 感兴趣的方面 / Interest
勾选以下两项：

- [x] **Codex Security** — 为安全扫描模块提供深度代码安全检测能力
- [x] **为我的项目申请 API 额度 / API credits for my project**

---

### OpenAI 组织 ID / OpenAI Organization ID
`[你的 Organization ID]`

> 获取方式：登录 platform.openai.com → Settings → Organization → Organization ID

---

### 如何使用 API 额度 / API Usage Plan（≤500 字符）

```
API 额度将用于 ReviewBot 的三大核心模块：

1) PR 智能审查：每次 Pull Request 触发时，Codex 分析代码差异
   并生成结构化审查报告，涵盖 bug 检测、性能问题、安全漏洞和
   代码风格建议。按日均处理 20-50 个 PR 估算，月消耗约
   2-5M tokens。

2) Issue 自动分类：Codex 分析新 Issue 内容，自动打标签、
   判重和推荐优先级排序，减少维护者的手动分流工作。

3) Release Notes 生成：汇总合并的 PR，用 Codex 自动生成
   分类清晰的结构化 Changelog，提升发布效率。
```

---

### 还有其他想补充的吗 / Additional Info（≤500 字符）

```
ReviewBot 项目本身也是 Codex for OSS 理念的最佳实践——
我们用 AI 帮助开源维护者做维护工作，让技术社区的整体效率
得到提升。项目已规划支持 GitLab 和 Gitee 平台扩展，未来
将进一步扩大生态覆盖范围。目前项目采用 MIT 许可证，欢迎
社区贡献。如果获得 API 额度支持，我们计划在 3 个月内完成
正式版发布并在至少 10 个活跃开源仓库中稳定运行。
```

---

## 提交前检查清单

- [ ] GitHub 仓库已创建并设为 **Public**
- [ ] GitHub 个人资料设为 **Public**
- [ ] 仓库包含完整的 README、LICENSE 和代码
- [ ] 已在 platform.openai.com 获取 Organization ID
- [ ] 邮箱与 ChatGPT 账户一致
- [ ] 每个必填字段不超过 500 字符限制