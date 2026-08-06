"""Unit tests for Table.to_list()."""

import os
import unittest

from textractor.entities.document import Document


class TestTableToList(unittest.TestCase):
    def setUp(self):
        fixture = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "fixtures/saved_api_responses/test_table.json",
        )
        self.table = Document.open(fixture).tables[0]

    def test_to_list_dimensions_match_table(self):
        result = self.table.to_list()
        self.assertEqual(len(result), self.table.row_count)
        self.assertTrue(
            all(len(row) == self.table.column_count for row in result)
        )

    def test_to_list_returns_list_of_lists_of_str(self):
        result = self.table.to_list()
        self.assertIsInstance(result, list)
        for row in result:
            self.assertIsInstance(row, list)
            self.assertTrue(all(isinstance(cell, str) for cell in row))

    def test_to_list_empty_cell_is_empty_string(self):
        # The fixture's (row 1, col 3) cell has no content.
        result = self.table.to_list()
        self.assertEqual(result[0][2], "")

    def test_to_list_is_consistent_with_to_txt(self):
        result = self.table.to_list()
        rebuilt = os.linesep.join(["\t".join(row) for row in result])
        self.assertEqual(rebuilt, self.table.to_txt())


if __name__ == "__main__":
    unittest.main()
