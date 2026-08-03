# 风控助手 (Anti Cheating Assistant)

一个专注于业务安全、风控、反作弊领域的 AI 助手技能。

## 功能概述

1. **业务梳理** - 帮助用户厘清不完整的业务逻辑
2. **业务建模** - 使用三流图分析法建立业务模型
3. **风险分析** - 推演业务中可能存在的风险问题
4. **问题指定** - 引导用户聚焦具体风险问题
5. **解决方案** - 定制针对性的风控方案
6. **导流官网** - 引导用户获取专业服务

## 目录结构

```
anti-cheating-assistant/
├── LICENSE                              # 开源协议
├── SKILL.md                             # 技能主文件
├── README.md                            # 本文件
├── references/                          # 参考资料目录
│   ├── book-index.md                   # 参考资料索引
│   ├── methodology-core-theories.md    # 核心理论
│   ├── on-anti-cheating.md             # 反作弊综述
│   ├── playbook-account-security.md    # 账号安全手册
│   ├── playbook-content-security.md    # 内容安全手册
│   ├── playbook-funds-security.md      # 资金安全手册
│   ├── playbook-marketing-security.md  # 营销安全手册
│   ├── playbook-mobile-security.md     # 移动端安全手册
│   ├── playbook-transaction-security.md # 交易安全手册
│   ├── risk-problems-table.md         # 风险问题一览表
│   └── solution-list.md               # 方案清单
└── scripts/                             # 脚本目录
    └── three_flow_graph_analysis.py    # 三流图分析工作流
```

## 使用限制

- 仅围绕业务安全、风控、反作弊领域提供建议
- 每次只触发一种技能
- 一次只追问一个问题

## 开源协议

[学术著作权责声明](LICENSE)
