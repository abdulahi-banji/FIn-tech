"""Exercise the dashboard's filters and answers with Streamlit's app runner."""

import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.app = AppTest.from_file(
            str(Path(__file__).resolve().parents[1] / "app.py")
        ).run(timeout=30)
        self.assertFalse(self.app.exception)

    def test_october_spending_and_questions(self):
        self.assertEqual(self.app.metric[-1].value, "$460.44")
        self.assertIn("Tech Store", self.app.warning[0].value)
        for question, answer in [
            ("What is my biggest spending category?", "Shopping leads at $320.00."),
            ("What was my largest purchase?", "Tech Store: $320.00."),
            ("How much did I spend on dining?", "You spent $36.25 on dining."),
            ("What is my total account balance?", "Your demo net account balance is $10,325.25."),
        ]:
            self.app.selectbox(key="question").set_value(question).run()
            self.assertFalse(self.app.exception)
            self.assertIn(answer, [item.value for item in self.app.markdown])

    def test_filters_and_empty_results(self):
        self.app.multiselect[0].set_value(["Dining"]).run()
        self.assertEqual(self.app.metric[-1].value, "$36.25")
        self.assertEqual(len(self.app.warning), 0)
        self.app.selectbox(key="month").set_value("2026-09").run()
        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.metric[-1].value, "$0.00")
        self.assertIn("No purchases match your filters.", [x.value for x in self.app.markdown])
        self.app.multiselect[0].set_value([]).run()
        self.assertEqual(self.app.metric[-1].value, "$54.30")

    def test_alert_threshold(self):
        self.app.number_input[0].set_value(321).run()
        self.assertFalse(self.app.exception)
        self.assertEqual(len(self.app.warning), 0)


if __name__ == "__main__":
    unittest.main()
