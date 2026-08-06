"""Tests for the SearchUtils word similarity functions."""

import unittest

from textractor.data.constants import SimilarityMetric
from textractor.utils.search_utils import SearchUtils


class TestSearchUtils(unittest.TestCase):
    def test_levenshtein_identical_words(self):
        """Identical words return maximum similarity of 1.0."""
        similarity = SearchUtils.get_word_similarity(
            "textract", "textract", SimilarityMetric.LEVENSHTEIN
        )
        self.assertEqual(similarity, 1.0)

    def test_levenshtein_is_case_insensitive(self):
        """Similarity is computed on lowercased inputs."""
        similarity = SearchUtils.get_word_similarity(
            "Textract", "textract", SimilarityMetric.LEVENSHTEIN
        )
        self.assertEqual(similarity, 1.0)

    def test_levenshtein_single_character_difference(self):
        """One edit over a length-4 string yields (4 - 1) / 4 = 0.75."""
        similarity = SearchUtils.get_word_similarity(
            "word", "ward", SimilarityMetric.LEVENSHTEIN
        )
        self.assertAlmostEqual(similarity, 0.75)

    def test_levenshtein_is_bounded(self):
        """Similarity always falls within the [0, 1] range."""
        similarity = SearchUtils.get_word_similarity(
            "abc", "xyz", SimilarityMetric.LEVENSHTEIN
        )
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)


if __name__ == "__main__":
    unittest.main()
