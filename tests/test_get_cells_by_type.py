"""Regression tests for Table.get_cells_by_type() across all cell types.

Guards against the bug where only COLUMN_HEADER cells were returned because
TableCell._update_response_metadata compared Textract EntityTypes against the
wrong string literals for section-title/summary/title/footer cells.
"""

import os
import unittest

from textractor.entities.document import Document
from textractor.data.constants import CellTypes


def _fixture(name):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "fixtures/saved_api_responses",
        name,
    )


class TestGetCellsByType(unittest.TestCase):
    def setUp(self):
        # This fixture contains COLUMN_HEADER, TABLE_SUMMARY and
        # TABLE_SECTION_TITLE cells in its tables.
        self.document = Document.open(
            _fixture("test_table_with_title_and_footers.json")
        )

    def _total(self, cell_type):
        return sum(
            len(table.get_cells_by_type(cell_type))
            for table in self.document.tables
        )

    def test_section_title_cells_are_returned(self):
        self.assertGreater(self._total(CellTypes.SECTION_TITLE), 0)

    def test_summary_cells_are_returned(self):
        self.assertGreater(self._total(CellTypes.SUMMARY_CELL), 0)

    def test_column_header_still_works(self):
        # COLUMN_HEADER was the only type working before the fix; ensure it
        # did not regress.
        self.assertGreater(self._total(CellTypes.COLUMN_HEADER), 0)


if __name__ == "__main__":
    unittest.main()
