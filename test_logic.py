import io
import unittest
from datetime import date
from unittest.mock import patch

import pandas as pd
from streamlit.testing.v1 import AppTest

import logic

TODAY = date(2026, 11, 6)


class DetectionTests(unittest.TestCase):
    def test_sample_boundary_order_and_threshold(self):
        data = logic.read_csv('sample.csv')
        result = logic.detect_stalled(data, today=TODAY)
        self.assertEqual(result.candidate_name.tolist(), ['Alex Morgan', 'Casey Patel'])
        self.assertEqual(result.days_inactive.tolist(), [12, 7])
        self.assertTrue(result.next_action.str.len().gt(0).all())
        self.assertIn('7-day', result.explanation.iloc[1])
        self.assertEqual(len(logic.detect_stalled(data, 8, TODAY)), 1)
        self.assertTrue(logic.detect_stalled(data, 30, TODAY).empty)

    def test_closed_stages_and_fallback(self):
        data = pd.DataFrame([
            ['A', 'Role', stage, '2026-10-01']
            for stage in [' HIRED ', 'reJECTed', ' Withdrawn ', 'Custom', ' applied ']
        ], columns=['candidate_name', 'role', 'stage', 'last_activity_date'])
        result = logic.detect_stalled(data, today=TODAY)
        self.assertEqual(result.stage.tolist(), ['applied', 'Custom'])
        self.assertIn('confirm', result.next_action.iloc[1])
        self.assertIn('application', result.next_action.iloc[0])

    def test_follow_up_queue_ties_and_actions(self):
        stages = ['Custom', 'Applied', 'Screening', 'Interview', 'Offer', 'Offer']
        data = pd.DataFrame([
            [str(i), 'Role', stage, '2026-10-30']
            for i, stage in enumerate(stages)
        ] + [['Oldest', 'Role', 'Applied', '2026-10-29']],
            columns=['candidate_name', 'role', 'stage', 'last_activity_date'])
        result = logic.detect_stalled(data, today=TODAY)
        self.assertEqual(result.candidate_name.tolist(), ['Oldest', '4', '5', '3', '2', '1', '0'])
        self.assertEqual(result.follow_up_rank.tolist(), list(range(1, 8)))
        self.assertEqual(result.days_over_threshold.tolist(), [1, 0, 0, 0, 0, 0, 0])
        self.assertIn('candidate', result.follow_up_with.iloc[1])
        self.assertIn('interviewer', result.next_action.iloc[3])
        self.assertTrue(result.priority_reason.str.len().gt(0).all())
        empty = logic.detect_stalled(data, threshold=30, today=TODAY)
        self.assertTrue(empty.empty)
        self.assertIn('follow_up_rank', empty.columns)

    def test_validation(self):
        base = logic.read_csv('sample.csv').iloc[:1].copy()
        for value in ['', None, '2026-02-30', '11/3/2026', '2026-1-01', '2026-11-07']:
            with self.subTest(value=value):
                data = base.copy()
                data.loc[0, 'last_activity_date'] = value
                with self.assertRaisesRegex(logic.ValidationError, 'row\\(s\\): 2'):
                    logic.detect_stalled(data, today=TODAY)
        for column in ['candidate_name', 'role', 'stage']:
            data = base.copy()
            data.loc[0, column] = '  '
            with self.assertRaisesRegex(logic.ValidationError, 'Blank required'):
                logic.detect_stalled(data, today=TODAY)
        with self.assertRaisesRegex(logic.ValidationError, 'Missing required columns: stage'):
            logic.detect_stalled(base.drop(columns=['stage']), today=TODAY)
        with self.assertRaisesRegex(logic.ValidationError, 'no candidate rows'):
            logic.detect_stalled(base.iloc[:0], today=TODAY)
        for threshold in [0, -1, 1.5, True]:
            with self.assertRaises(logic.ValidationError):
                logic.detect_stalled(base, threshold, TODAY)
        with self.assertRaisesRegex(logic.ValidationError, 'Could not read'):
            logic.read_csv(io.StringIO(''))

    def test_app_uploaded_csv_reloads_stale_logic(self):
        # Reproduce an existing Streamlit process holding the old detector.
        import logic
        def old_detector(*args, **kwargs):
            raise AssertionError("Stale detector must be reloaded")

        with patch.object(logic, 'detect_stalled', old_detector):
            with patch('streamlit.file_uploader', return_value=io.StringIO(
                'candidate_name,role,stage,last_activity_date\n'
                'Alex Morgan,QA Engineer,Interview,2020-01-01\n'
            )):
                app = AppTest.from_file('app.py').run()
        self.assertEqual(len(app.exception), 0)
        self.assertIn('Follow up first: Alex Morgan', app.info[0].value)
        table = app.dataframe[0].value
        self.assertEqual(table['Follow-up order'].tolist(), [1])
        self.assertIn('Interviewer', table['Follow up with'].iloc[0])

    def test_app_starts(self):
        app = AppTest.from_file('app.py').run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.number_input[0].value, 7)
        self.assertIn('Upload a CSV', app.info[0].value)


if __name__ == '__main__':
    unittest.main()
