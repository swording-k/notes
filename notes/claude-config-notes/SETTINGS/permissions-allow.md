# Permissions Allow 配置

## 更新记录

### 2026-04-24 - 扩大权限 Allow 列表

**原因**：减少终端命令执行时的确认询问次数

**全局配置** (`~/.claude/settings.json`)：

```json
"permissions": {
  "allow": [
    "Bash(git:*)",
    "Bash(npm:*)",
    "Bash(node:*)",
    "Bash(curl:*)",
    "Bash(curl -s **)",
    "Bash(curl **)",
    "Bash(echo **)",
    "Bash(ls **)",
    "Bash(ps **)",
    "Bash(npx **)",
    "Bash(yarn **)",
    "Bash(pnpm **)",
    "Bash(pip **)",
    "Bash(python3 **)",
    "Bash(cd **)",
    "Read",
    "Glob",
    "Grep"
  ],
  "defaultMode": "plan"
}
```

**新增的允许规则**：
- `Bash(curl:*)` - 所有 curl 命令（冒号语法）
- `Bash(curl -s **)` - curl -s 变体
- `Bash(curl **)` - 所有 curl 命令
- `Bash(echo **)` - echo 命令
- `Bash(ls **)` - ls 命令
- `Bash(ps **)` - ps 命令
- `Bash(npx **)` - npx 命令
- `Bash(yarn **)` - yarn 命令
- `Bash(pnpm **)` - pnpm 命令
- `Bash(pip **)` - pip 命令
- `Bash(python3 **)` - python3 命令
- `Bash(cd **)` - cd 命令

**注意**：
- 危险的删除操作（如 `rm -rf`）即使在 allow 列表中也会额外要求确认
- 太宽泛的规则（如 `Bash(rm **)`）会因为安全原因仍要求确认

### 2026-04-26 - 继续扩大权限 Allow 列表

**原因**：日常开发中需要更多文件操作和命令执行权限

**新增的允许规则**：
- `Read(./*)` - 读取当前目录及子目录文件
- `Write(./*)` - 写入当前目录及子目录文件
- `Edit(./*)` - 编辑当前目录及子目录文件
- `Glob(./*)` - 匹配当前目录及子目录文件
- `Bash(ls:*)` - ls 命令（冒号语法）
- `Bash(cd:*)` - cd 命令（冒号语法）
- `Bash(grep:*)` - grep 命令（冒号语法）
- `WebFetch` - 网页抓取引擎
