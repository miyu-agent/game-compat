# 游戏兼容性

Miyu 技能包，带一个技能 `game-compat`：查一款游戏在 Linux（含 Steam Deck）、Apple 芯片的 Mac 上能不能玩。你问「这游戏 Mac 能玩吗」「Linux 上能跑吗」时，AI 会用它查，几个来源并排交回。

| 平台 | 来源 | 给什么 |
|---|---|---|
| Linux | ProtonDB | 评级（总评、最近、最好）、报告数、最近几份玩家报告：结论、Proton 版本、出的问题、启动参数、备注 |
| Linux | AreWeAntiCheatYet | 反作弊状态（Supported、Denied……）、用的是哪家反作弊、最近的变动 |
| Linux | caniplayonlinux | 一句话结论和最后核实的日期 |
| Mac | MacGamingDB | 评级、报告数、玩家怎么跑的（原生、CrossOver、Parallels），最近几份报告：用的芯片、转译层、帧数、画质、备注 |

技能里的脚本由 AI 在 `shell` 里运行，也可以自己运行：

```sh
python3 skills/game-compat/scripts/game_compat.py "Elden Ring" --platform mac
```

| 参数 | 说明 |
|---|---|
| 游戏 | Steam App ID 或游戏名，必填。英文原名最准；中文名照 Steam 的中文商店名对 |
| `--platform` | `linux`、`mac`、`all`，默认 `all` |
| `--reports` | 每个来源列几份玩家报告，0–20，默认 6；0 只给评级 |
| `--json` | 输出 JSON，给代码用 |

- 先认游戏再查：App ID 经 Steam 查名字；英文名经 ProtonDB 的搜索索引；中文名先找 Steam 中文商店名完全对得上的，再看搜索索引给的，英文结果要和那款游戏的中文商店名对得上才算。对不上的不硬查，交回搜到了什么、让换英文原名。
- 不在 Steam 上的游戏没有 ProtonDB，反作弊、caniplayonlinux、MacGamingDB 照名字还能查。这类游戏有时会被认成标题里带它名字的另一款 Steam 游戏，第一行写着认成了哪一款，技能会让 AI 先核对。
- 某个来源没收录写「没收录」，出错写「出错」，两样不混：没收录不等于没有反作弊。
- AreWeAntiCheatYet 的总表和 caniplayonlinux 的站点地图缓存一天，放在 `MIYU_CACHE_DIR`，没有时放在 `~/.cache/miyu-game-compat`。
- 只用 Python 标准库。

0.2.0 起从脚本工具改成技能（平时不占工具说明，用到时才读），并加上 Mac。MacGamingDB 的数据来自它公开的接口（项目 [neo773/macgamingdb](https://github.com/neo773/macgamingdb)，MIT 许可）。
