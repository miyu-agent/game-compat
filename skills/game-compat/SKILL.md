---
name: game-compat
description: "Check how a PC game runs on Linux (ProtonDB, anti-cheat, caniplayonlinux) or on Apple Silicon Macs (MacGamingDB player reports). Use when asked whether a game works on Linux, Steam Deck or a Mac: 能不能在 Linux 上玩、Mac 能玩吗、苹果电脑能不能跑、Steam Deck 能玩吗、兼容性."
metadata:
  display_name: Game compatibility
  summary: Whether a game runs on Linux or an Apple Silicon Mac
  display_name_zh: 游戏兼容性
  summary_zh: 查游戏在 Linux、Apple 芯片 Mac 上能不能玩
---

# Game compatibility

Run `scripts/game_compat.py` from the folder this SKILL.md is in, through `shell`:

```sh
python3 <folder of this SKILL.md>/scripts/game_compat.py "<game>" --platform linux|mac|all [--chip M1] [--reports N] [--json]
```

- `<game>`: the English title or the Steam App ID. A Chinese name only matches when it is the game's Chinese Steam store name; when it misses, search for the English title and run again.
- `--platform`: `linux` for Linux and the Steam Deck, `mac` for a Mac, `all` when the user did not say. Default `all`.
- `--chip`: on a Mac, the user's chip when they said it (`M1`, `M2 Pro`, `M4 Max`); only reports from that chip are listed, with their count. `M1` includes M1 Pro, Max and Ultra.
- `--reports`: recent player reports per source, 0-20, default 6. Use 0 for the ratings alone.

The first line is the game it matched. Check that it is the game the user meant: a game that is not on Steam (League of Legends, Valorant) can match a different Steam game whose title contains the name. If it is wrong, say so and use the exact title or App ID; for the Mac part, MacGamingDB is still searched by name.

## Reading the result

Linux and Steam Deck:
- Steam Deck (Valve's own test): Verified (已验证), Playable (可游玩), Unsupported (不支持) or not tested (还没测), with the reasons Valve gives. For a Steam Deck question this is the first thing to say.
- ProtonDB tier, best to worst: Native, Platinum, Gold, Silver, Bronze, Borked. "Trending" is the recent reports, which matter more than the overall tier for a game that changed. Reports give the Proton version and launch options that worked.
- Anti-cheat (AreWeAntiCheatYet): Supported or Running means online play works; Denied or Broken means it does not. Not listed is not the same as no anti-cheat.
- caniplayonlinux: a one-line verdict and when it was last checked.

Mac (MacGamingDB, Apple Silicon only):
- Rating, best to worst: 极好 (Excellent), 很好 (Very good), 好 (Good), 能玩 (Playable), 勉强能玩 (Barely playable), 玩不了 (Unplayable); the report count, and how players ran it: native, CrossOver (Windows games through Wine, often with D3DMetal or DXVK), Parallels.
- Each report names the chip (M1 to M5, with Pro, Max, Ultra). Performance on an older or base chip can be much lower than a report from a newer one.
- A native Mac build on Steam is shown on the first line when there is one.

A source that failed says so; do not read a failure as "does not run". Say only what the script printed; if something the user asked about is not in it, say it was not found rather than filling it in. Player reports are quoted in the language they were written in; translate what you use. Give the user the answer in their language, the platform they asked about first, with the links.
