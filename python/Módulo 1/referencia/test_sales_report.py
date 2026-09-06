import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from sales_report import ExcelSource, SalesAnalyzer


class SalesAnalyzerTests(unittest.TestCase):
    def test_totals_ignore_product_ids_and_normalize_headers(self):
        data = pd.DataFrame({
            " Valor.Final ": ["0.10", "0.20"],
            "Quantidade": [1, 2], "ID": [100, 200],
        })
        summary = SalesAnalyzer().summarize(data)
        self.assertEqual(summary.revenue, Decimal("0.30"))
        self.assertEqual(summary.quantity, 3)
        self.assertIn("R$ 0,30", summary.report())
        self.assertIn(" Valor.Final ", data.columns)

    def test_bad_data_is_not_silently_reported(self):
        cases = [
            pd.DataFrame({"QUANTIDADE": [1]}),
            pd.DataFrame(columns=["VALOR_FINAL", "QUANTIDADE"]),
            pd.DataFrame({"VALOR_FINAL": [None], "QUANTIDADE": [1]}),
            pd.DataFrame({"VALOR_FINAL": ["R$ 10"], "QUANTIDADE": [1]}),
            pd.DataFrame({"VALOR_FINAL": [10], "QUANTIDADE": [1.5]}),
            pd.DataFrame({"VALOR_FINAL": ["0.001"], "QUANTIDADE": [1]}),
            pd.DataFrame([[1, 1, 1]], columns=["Valor.Final", "VALOR_FINAL", "QUANTIDADE"]),
        ]
        for data in cases:
            with self.subTest(columns=list(data.columns)), self.assertRaises(ValueError):
                SalesAnalyzer().summarize(data)

    def test_reads_real_excel_and_formats_thousands(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "sales.xlsx"
            pd.DataFrame({"VALOR_FINAL": [1234.5], "QUANTIDADE": [2]}).to_excel(
                path, index=False
            )
            summary = SalesAnalyzer().summarize(ExcelSource().read(path))
        self.assertIn("R$ 1.234,50", summary.report())


if __name__ == "__main__":
    unittest.main()
