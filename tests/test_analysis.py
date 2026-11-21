import tempfile
import unittest
from pathlib import Path
import pandas as pd
from src.analyze import anomaly_flags, load_logs

class TestAnalysis(unittest.TestCase):
    def test_flags_only_above_threshold(self):
        values = pd.Series([0, 12, 13])
        self.assertEqual(anomaly_flags(values, 12).tolist(), [False, False, True])

    def test_missing_required_field(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "bad.csv"
            pd.DataFrame({"timestamp": ["2026-01-01"]}).to_csv(p, index=False)
            with self.assertRaisesRegex(ValueError, "Missing required columns"):
                load_logs(p)

if __name__ == "__main__":
    unittest.main()
