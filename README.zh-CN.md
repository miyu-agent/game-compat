<p align="center">
  <a href="README.md">English</a> | 简体中文
</p>

# 游戏兼容性

> <sub>本文档由 Anthropic 的 Claude Fable 5.2 生成。</sub>

这是 Miyu 的一个技能软件包，提供一个技能 `game-compat`，用来查询一款游戏在 Linux（包括 Steam Deck）和 Apple 芯片的 Mac 上能不能玩。当你问「这游戏 Mac 能玩吗」「Linux 上能跑吗」时，AI 会用这个技能查询，并把几个来源的结果并排返回。

| 平台 | 来源 | 提供的内容 |
|---|---|---|
| Linux | ProtonDB | 评级（总评、最近、最好）、报告数、最近几份玩家报告：结论、Proton 版本、遇到的问题、启动参数、备注 |
| Linux | AreWeAntiCheatYet | 反作弊状态（`Supported`、`Denied`……）、使用的是哪家的反作弊、最近的变动 |
| Linux | caniplayonlinux | 一句话的结论和最后核实的日期 |
| Steam Deck | Steam（Valve 的测试） | `已验证`、`可游玩`、`不支持`，以及 Valve 给出的原因 |
| Mac | MacGamingDB | 评级、报告数、玩家使用的运行方式（原生、CrossOver、Parallels），以及最近几份报告：使用的芯片、转译层、帧数、画质、备注 |

技能里的脚本由 AI 在 `shell` 里运行，你也可以自己运行，例如：

```sh
python3 skills/game-compat/scripts/game_compat.py "Elden Ring" --platform mac
```

| 参数 | 说明 |
|---|---|
| 游戏 | Steam App ID 或者游戏名，必填。用英文原名查询最准确；中文名需要和 Steam 的中文商店名对得上 |
| `--platform` | `linux`、`mac`、`all`，默认是 `all` |
| `--chip` | 只看 Mac 上某一种芯片的报告，例如 `M1`、`M2 Pro`；`M1` 包括 Pro、Max 和 Ultra |
| `--reports` | 每个来源列出的玩家报告份数，0–20，默认 6；0 表示只给出评级 |
| `--json` | 输出 JSON，供代码使用 |

- 脚本先识别是哪款游戏，再查询：App ID 通过 Steam 查出名字；英文名通过 ProtonDB 的搜索索引识别；中文名先找 Steam 中文商店名完全对得上的游戏，再看搜索索引给出的结果，英文的结果要和那款游戏的中文商店名对得上才算数。如果对不上，脚本不会强行查询，而是返回搜到了什么，让你换成英文原名。
- 不在 Steam 上的游戏没有 ProtonDB 的数据，但是反作弊、caniplayonlinux 和 MacGamingDB 仍然可以按名字查询。这类游戏有时会被识别成标题里带有它名字的另一款 Steam 游戏，输出的第一行写着识别成了哪一款，技能会让 AI 先核对这一点。
- 如果某个来源没有收录这款游戏，结果里写 `没收录`；如果查询出错，写 `出错`，两种情况不会混在一起：没有收录不等于没有反作弊。
- AreWeAntiCheatYet 的总表和 caniplayonlinux 的站点地图会缓存一天，放在 `MIYU_CACHE_DIR` 里；没有这个目录时，放在 `~/.cache/miyu-game-compat`。
- 脚本只使用 Python 标准库。

这个软件包提供的是技能，所以平时不占用工具说明，用到时 AI 才读取它。MacGamingDB 的数据来自它公开的接口（项目 [neo773/macgamingdb](https://github.com/neo773/macgamingdb)，MIT 许可证）。
