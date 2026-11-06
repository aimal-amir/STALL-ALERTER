import io
import unittest
from datetime import date

import pandas as pd
from streamlit.testing.v1 import AppTest

from logic import ValidationError, detect_stalled, read_csv

TODAY = date(2026, 11, 6)


class DetectionTests(unittest.TestCase):
    def test_sample_boundary_order_and_threshold(self):
        data = read_csv('sample.csv')
        result = detect_stalled(data, today=TODAY)
        self.assertEqual(result.candidate_name.tolist(), ['Alex Morgan', 'Casey Patel'])
        self.assertEqual(result.days_inactive.tolist(), [12, 7])
        self.assertTrue(result.next_action.str.len().gt(0).all())
        self.assertIn('7-day', result.explanation.iloc[1])
        self.assertEqual(len(detect_stalled(data, 8, TODAY)), 1)
        self.assertTrue(detect_stalled(data, 30, TODAY).empty)

    def test_closed_stages_and_fallback(self):
        data = pd.DataFrame([
            ['A', 'Role', stage, '2026-10-01']
            for stage in [' HIRED ', 'reJECTed', ' Withdrawn ', 'Custom', ' applied ']
        ], columns=['candidate_name', 'role', 'stage', 'last_activity_date'])
        result = detect_stalled(data, today=TODAY)
        self.assertEqual(result.stage.tolist(), ['Custom', 'applied'])
        self.assertIn('confirm', result.next_action.iloc[0])
        self.assertIn('application', result.next_action.iloc[1])

    def test_validation(self):
        base = read_csv('sample.csv').iloc[:1].copy()
        for value in ['', None, '2026-02-30', '11/3/2026', '2026-1-01', '2026-11-07']:
            with self.subTest(value=value):
                data = base.copy()
                data.loc[0, 'last_activity_date'] = value
                with self.assertRaisesRegex(ValidationError, 'row\\(s\\): 2'):
                    detect_stalled(data, today=TODAY)
        for column in ['candidate_name', 'role', 'stage']:
            data = base.copy()
            data.loc[0, column] = '  '
            with self.assertRaisesRegex(ValidationError, 'Blank required'):
                detect_stalled(data, today=TODAY)
        with self.assertRaisesRegex(ValidationError, 'Missing required columns: stage'):
            detect_stalled(base.drop(columns=['stage']), today=TODAY)
        with self.assertRaisesRegex(ValidationError, 'no candidate rows'):
            detect_stalled(base.iloc[:0], today=TODAY)
        for threshold in [0, -1, 1.5, True]:
            with self.assertRaises(ValidationError):
                detect_stalled(base, threshold, TODAY)
        with self.assertRaisesRegex(ValidationError, 'Could not read'):
            read_csv(io.StringIO(''))

    def test_app_starts(self):
        app = AppTest.from_file('app.py').run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.number_input[0].value, 7)
        self.assertIn('Upload a CSV', app.info[0].value)


if __name__ == '__main__':
    unittest.main()
