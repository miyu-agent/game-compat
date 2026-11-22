# game_compat.py 的测试（审计 2026-11-18）。
#
# 跑法（在仓库根）：
#   python3 -I -B -m unittest discover -s .github/tests
# （不加 -t .：.github 不是合法的包名，加了 unittest 会报 Start directory is not importable。）
#
# 只用标准库；不联网：fetch/fetch_json/algolia/steam_details 换成桩，断网也能跑。HOME、XDG_*、MIYU_* 都指到临时目录。
# 放在 .github/tests/ 而不是 tests/：打包会跳过 .github，测试不会进包。

import importlib.util
import os
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "skills" / "game-compat" / "scripts" / "game_compat.py"


def load():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("game_compat_under_test", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Sandbox(unittest.TestCase):
    """每条测试一个临时目录，环境里去掉所有 MIYU_*，网络函数先换成直接失败的桩。"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = pathlib.Path(self.tmp.name)
        env = {k: v for k, v in os.environ.items() if not k.startswith(("MIYU_", "XDG_"))}
        env.update(HOME=str(root / "home"), XDG_CONFIG_HOME=str(root / "cfg"),
                   XDG_CACHE_HOME=str(root / "xdg-cache"), XDG_STATE_HOME=str(root / "xdg-state"),
                   XDG_DATA_HOME=str(root / "xdg-data"))
        patcher = mock.patch.dict(os.environ, env, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.root = root
        self.mod = load()

        def no_network(url, body=None, headers=None, limit=0):
            raise AssertionError(f"测试里不该联网：{url}")

        self.mod.fetch = no_network


class ChineseNameReverseLookup(Sandbox):
    # 审计 #178 game_compat：中文名查询时，Algolia 头一条是英文名就去 steam_details 取它的中文商店名来对。
    # 分支条件是 name.isascii()，名字里带 ’、®、™ 这类非 ASCII 符号时两个分支都不进，
    # 一次反查都不做，直接报「没对上这个中文名」。
    QUERY = "刺客信条：幻景"

    def stub(self, algolia_name):
        self.details_calls = []
        # Steam 中文商店搜索什么都没搜到，只能靠 Algolia 头条 + 反查
        self.mod.fetch_json = lambda url, **kw: {"items": []}
        self.mod.algolia = lambda query, hits=5: [{"name": algolia_name, "objectID": "2608970"}]

        def steam_details(app_id, language="english"):
            self.details_calls.append((app_id, language))
            return {"name": self.QUERY, "linux": False}

        self.mod.steam_details = steam_details

    def test_title_with_typographic_symbols(self):
        self.stub("Assassin’s Creed® Mirage")
        result = self.mod.identify(self.QUERY)
        self.assertEqual(result.get("app_id"), 2608970, result)
        self.assertIn((2608970, "schinese"), self.details_calls)

    # 防改坏（现在就绿）：纯 ASCII 的英文名照旧能反查认出来。
    def test_plain_ascii_title(self):
        self.stub("Assassins Creed Mirage")
        result = self.mod.identify(self.QUERY)
        self.assertEqual(result.get("app_id"), 2608970, result)


if __name__ == "__main__":
    unittest.main()
