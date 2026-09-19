# Acahti — SAIDC workspace

Version: `1.6.1+saidc.gitfd7aef424f78`

MCP endpoint: `https://acahti.s-aidc.com/mcp`

## 首次使用

1. 安装插件，打开插件详情 → MCP 服务器 → 连接设置（齿轮）。
2. 如果提示未连接，选择 Authenticate / 登录，完成自己的 OAuth 授权。网页登录不等于 MCP 授权，无需发送密码或 Token。
3. 返回本地 Codex 任务；工具未刷新时新建任务，发送：通过 MCP 检查我的 Acahti 身份和待处理事项。
4. 验收必须成功调用 whoami 和 inbox；失败时提供连接状态/错误，不改用网页查数据。

## Author 提醒

可在 /hooks 审查并信任提醒 hook，需要 Python 3。它只注入规则，不读取凭据、不改 Git、不强制拦截提交。Skill 要求 Acahti 提交前核验当前 MCP 身份、按 remote host 限定范围、设置并检查有效 author。

## 发布维护

从最新通用源码用 scripts/package_workspace.py 重新生成包，不在旧 ZIP 上累积修改。release.json 记录源码文件哈希和包内文件哈希，用来核对发布内容。每次修改必须使用新版本。
