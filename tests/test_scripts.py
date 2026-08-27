# -*- coding: utf-8 -*-
"""基础冒烟测试：验证 skill 内置脚本可加载、核心函数可运行。"""

import contextlib
import importlib.util
import io
import pathlib
import unittest

SKILL_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_ROOT / "scripts"


def load_script(name):
    path = SCRIPTS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestBaguaLookup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_script("bagua_lookup")

    def test_64_hexagrams(self):
        self.assertEqual(len(self.mod.LIUSHISI_GUA), 64)

    def test_all_have_trigrams(self):
        for seq, gua in self.mod.LIUSHISI_GUA.items():
            self.assertIsNotNone(gua.get("shang"), seq)
            self.assertIsNotNone(gua.get("xia"), seq)

    def test_lookup_by_full_and_short_name(self):
        self.assertEqual(self.mod.get_gua_by_name("乾为天")[0], 1)
        self.assertEqual(self.mod.get_gua_by_name("乾")[0], 1)
        self.assertEqual(self.mod.get_gua_by_name("火水未济")[0], 64)
        self.assertEqual(self.mod.get_gua_by_name("未济")[0], 64)

    def test_lookup_by_trigrams(self):
        self.assertEqual(self.mod.get_gua_by_shangxia(3, 6)[0], 64)


class TestXiaoLiuRen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_script("xiaoliuren_calc")

    def test_month_day_hour(self):
        with contextlib.redirect_stdout(io.StringIO()):
            pos, gong = self.mod.xiaoliuren_month_day_hour(1, 1, "子")
        self.assertIn(pos, range(1, 7))
        self.assertIn("name", gong)

    def test_number(self):
        with contextlib.redirect_stdout(io.StringIO()):
            pos, gong = self.mod.xiaoliuren_number(1, 2, 3)
        self.assertIn(pos, range(1, 7))
        self.assertIn("name", gong)


class TestLiuRenPaiPan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_script("liuren_paipan")

    def test_ganzhi_basics(self):
        self.assertEqual(self.mod.get_ganzhi_year(2024), "甲辰")
        self.assertEqual(self.mod.get_ganzhi_month(2024, 1), "丙寅")
        self.assertEqual(self.mod.get_ganzhi_day(2024, 1, 1), "甲子")

    def test_print_paipan(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.mod.print_paipan(2024, 1, 1, 0)


class TestHeHunScore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_script("hehun_score")

    def test_score_and_grade(self):
        score = self.mod.calc_hehun_score([3] * 9)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        self.assertTrue(self.mod.get_grade(score))


if __name__ == "__main__":
    unittest.main()
