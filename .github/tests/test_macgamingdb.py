# MacGamingDB 那一段的测试（0.2.0）：不联网，网络函数换成桩。跑法同 test_game_compat.py。

import importlib.util
import pathlib
import sys
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "skills" / "game-compat" / "scripts" / "game_compat.py"


def load():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("game_compat_mac_under_test", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


GAME = {
    "game": {"name": "Hollow Knight", "slug": "hollow-knight", "aggregatedPerformance": "EXCELLENT", "reviewCount": 2},
    "reviews": [
        {"createdAt": "2026-04-06T00:00:00Z", "playMethod": "NATIVE", "performance": "VERY_GOOD", "fps": 60,
         "chipset": "M3", "chipsetVariant": "BASE", "graphicsSettings": "HIGH", "notes": "- stutters sometimes"},
        {"createdAt": "2026-06-24T00:00:00Z", "playMethod": "CROSSOVER", "translationLayer": "D3D_METAL",
         "performance": "EXCELLENT", "chipset": "M1", "chipsetVariant": "MAX"},
    ],
    "stats": {"methods": {"native": 1, "crossover": 1, "parallels": 0}},
}


class MacGamingDB(unittest.TestCase):
    def setUp(self):
        self.mod = load()
        self.asked = []

        def fetch_json(url, **kw):
            self.asked.append(url)
            if url.endswith("/games/367520"):
                return GAME
            if "/games/search" in url:
                return [{"ref": "999", "name": "Other Game"}, {"ref": "367520", "name": "Hollow Knight"}]
            raise self.mod.HttpError("404", 404)

        self.mod.fetch_json = fetch_json

    def test_by_app_id_newest_report_first(self):
        data = self.mod.macgamingdb(367520, "Hollow Knight", 5)
        self.assertEqual(data["rating"], "极好")
        self.assertEqual(data["methods"], {"原生": 1, "CrossOver": 1})
        self.assertEqual([r["date"] for r in data["recent"]], ["2026-06-24", "2026-04-06"])
        self.assertEqual(data["recent"][0]["chip"], "M1 Max")
        self.assertEqual(data["recent"][1]["chip"], "M3", "BASE 不写")
        self.assertTrue(data["recent"][1]["note"].startswith("\\-"), "备注开头的 Markdown 符号转义")
        text = "\n".join(self.mod.mgdb_render(data))
        self.assertIn("CrossOver + D3D_METAL · M1 Max", text)

    def test_falls_back_to_an_exact_name_in_the_search(self):
        data = self.mod.macgamingdb(None, "hollow knight", 1)
        self.assertEqual(data["name"], "Hollow Knight")
        self.assertTrue(any("/games/search" in url for url in self.asked))

    def test_a_page_without_reports_is_not_listed(self):
        empty = dict(GAME, game=dict(GAME["game"], reviewCount=0), reviews=[])
        self.mod.fetch_json = lambda url, **kw: empty
        self.assertIsNone(self.mod.macgamingdb(367520, "Hollow Knight", 3))

    def test_unknown_game_is_not_listed(self):
        self.assertIsNone(self.mod.macgamingdb(1, "Nothing Like It", 3))

    def test_platform_mac_skips_the_linux_sources(self):
        self.mod.identify = lambda q: {"app_id": 367520, "name": "Hollow Knight", "linux": True, "mac": True}
        query, ident, proton, cheat, site, mac = self.mod.check("Hollow Knight", 1, "mac")
        self.assertEqual((proton, cheat, site), (None, None, None))
        self.assertEqual(mac[0], "ok")
        out = self.mod.to_json(query, ident, proton, cheat, site, mac)
        self.assertEqual(out["protondb"], {"status": "skipped"})
        self.assertTrue(out["game"]["mac_native"])
        self.assertEqual(out["macgamingdb"]["status"], "ok")


if __name__ == "__main__":
    unittest.main()
