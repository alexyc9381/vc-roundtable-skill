import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1] / "skills" / "roundtable"
sys.path.insert(0, str(SKILL_DIR))
import table  # noqa: E402

PITCH = ("We are Tidy, an app that plans your family's meals for the week.\n\n"
         "Parents spend 5 hours a week deciding what to cook.\n\n"
         "We have 400 families on a waitlist and 60 paying $8 a month.\n\n"
         "We are raising $500K to hire one engineer.")


def write(folder, seat, data):
    d = Path(".roundtable") / folder
    d.mkdir(parents=True, exist_ok=True)
    (d / (seat + ".json")).write_text(json.dumps(dict(data, firm=seat)))


class TableTest(unittest.TestCase):
    def setUp(self):
        self.old = os.getcwd()
        os.chdir(tempfile.mkdtemp())
        self.case = table.setup(PITCH, "raise $500K", "facts", seed=3)
        self.seats = [f["seat"] for f in self.case["firms"]]

    def tearDown(self):
        os.chdir(self.old)

    def test_setup_numbers_paragraphs_and_seats_the_three(self):
        self.assertEqual([u["n"] for u in self.case["units"]], [1, 2, 3, 4])
        self.assertEqual(len(self.seats), 7)
        for s in table.ALWAYS:
            self.assertIn(s, self.seats)
        self.assertEqual(table.seat(7, 3), table.seat(7, 3))

    def test_grill_keeps_only_real_quotes(self):
        write("questions", self.seats[0], {"questions": [{"ask": "Why now?", "quote": "60 paying $8 a month"}]})
        write("questions", self.seats[1], {"questions": [{"ask": "Who?", "quote": "a million users"}]})
        asked, dropped = table.grill()
        self.assertEqual(len(asked), 1)
        self.assertEqual(len(dropped), 1)
        self.assertTrue(Path(".roundtable/grill.md").exists())

    def test_answers_fill_in_order_and_mark_missing(self):
        write("questions", self.seats[0], {"questions": [{"ask": "A?", "quote": "Tidy"}, {"ask": "B?", "quote": "one engineer"}]})
        table.grill()
        got = table.answers("We grew 20% last month.")
        self.assertEqual(got[0]["answer"], "We grew 20% last month.")
        self.assertEqual(got[1]["answer"], "[not answered]")

    def test_check_needs_real_quotes_and_a_fix_on_a_pass(self):
        write("questions", self.seats[0], {"questions": [{"ask": "A?", "quote": "Tidy"}]})
        table.grill()
        table.answers("We grew 20% last month.")
        write("votes", self.seats[0], {"verdict": "fund", "why": "w", "quotes": [{"words": "grew 20% last month"}]})
        write("votes", self.seats[1], {"verdict": "pass", "why": "w", "fix": [], "quotes": [{"words": "Tidy"}]})
        write("votes", self.seats[2], {"verdict": "pass", "why": "w", "fix": ["x"], "quotes": [{"words": "never said this"}]})
        write("votes", self.seats[3], {"verdict": "fund if", "why": "w", "fix": ["show retention"], "quotes": [{"words": "400 families"}]})
        kept, dropped = table.check()
        self.assertEqual(sorted(a["firm"] for a in kept), sorted([self.seats[0], self.seats[3]]))
        self.assertEqual(len(dropped), 2)

    def test_tally_and_report(self):
        write("votes", self.seats[0], {"verdict": "fund", "why": "w", "quotes": [{"words": "400 families"}]})
        write("votes", self.seats[1], {"verdict": "pass", "why": "w", "fix": ["show retention"], "quotes": [{"words": "400 families"}]})
        table.check()
        t = table.tally()
        self.assertEqual(t["yes"], 1)
        self.assertEqual(t["verdicts"]["pass"], 1)
        self.assertEqual(t["most_quoted"][0], {"n": 3, "times": 2})
        text = Path(table.report()).read_text()
        self.assertIn("1 of 2", text)
        self.assertIn("show retention", text)
        self.assertIn(table.CREDIT, text)

    def test_unknown_firm_is_thrown_out(self):
        write("votes", "not-a-firm", {"verdict": "fund", "why": "w", "quotes": [{"words": "Tidy"}]})
        kept, dropped = table.check()
        self.assertEqual(kept, [])
        self.assertEqual(dropped[0]["why"], ["not a firm at this table"])


if __name__ == "__main__":
    unittest.main()
