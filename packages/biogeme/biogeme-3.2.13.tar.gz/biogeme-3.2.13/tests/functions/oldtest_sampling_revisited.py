import unittest
from unittest.mock import patch
import pandas as pd
from biogeme.sampling_revisited import (
    sample_alternatives,
    StratumTuple,
    choice_sets_generation,
)
from biogeme.exceptions import BiogemeError


class TestSampleAlternativesUpdated(unittest.TestCase):
    def setUp(self):
        # Common setup for all tests
        self.alt_df = pd.DataFrame(
            {'id_column': [1, 2, 3, 4, 5], 'data': ['A', 'B', 'C', 'D', 'E']}
        )

    def test_multiple_subsets(self):
        with self.assertRaises(BiogemeError):
            partition = (StratumTuple({1, 2}, 1), StratumTuple({2, 3, 4}, 2))
            sample_alternatives(self.alt_df, 'id_column', partition)

    def test_empty_stratum(self):
        with self.assertRaises(BiogemeError):
            partition = (StratumTuple(set(), 1), StratumTuple({3, 4, 5}, 2))
            sample_alternatives(self.alt_df, 'id_column', partition)

    def test_unknown_alternative(self):
        with self.assertRaises(BiogemeError):
            partition = (StratumTuple({1, 2}, 1), StratumTuple({3, 4, 5}, 2))
            sample_alternatives(self.alt_df, 'id_column', partition, 6)

    def test_large_sample_size(self):
        with self.assertRaises(BiogemeError):
            partition = (StratumTuple({1, 2}, 3), StratumTuple({3, 4, 5}, 2))
            sample_alternatives(self.alt_df, 'id_column', partition)

    def test_missing_alternative_in_partition(self):
        with self.assertRaises(BiogemeError):
            partition = (StratumTuple({1, 2}, 1), StratumTuple({3, 4}, 1))
            sample_alternatives(self.alt_df, 'id_column', partition)

    def test_duplicate_chosen_alternative(self):
        df = pd.concat([self.alt_df, self.alt_df.iloc[[2]]])
        with self.assertRaises(BiogemeError):
            partition = (StratumTuple({1, 2}, 1), StratumTuple({3, 4, 5}, 2))
            sample_alternatives(df, 'id_column', partition, 3)

    def test_chosen_in_last_stratum(self):
        partition = (
            StratumTuple({1, 2}, 1),
            StratumTuple({3, 4}, 1),
            StratumTuple({5}, 1),
        )
        sample_result, chosen_result = sample_alternatives(
            self.alt_df, 'id_column', partition, 5
        )
        self.assertTrue(5 in sample_result['id_column'].iloc[-1:].values)
        self.assertEqual(chosen_result.iloc[0]['id_column'], 5)

    def test_chosen_as_last_row(self):
        chosen = 4
        segment_1 = StratumTuple({1, 2}, 1)
        segment_2 = StratumTuple({3, 4, 5}, 2)
        partition = (segment_1, segment_2)
        sample_result, chosen_result = sample_alternatives(
            self.alt_df, 'id_column', partition, chosen=chosen
        )
        # The last alternative should belong to the group of the chosen alternative
        last_alternative = sample_result.iloc[-1]['id_column']
        self.assertIn(last_alternative, segment_2.subset)
        # If the chosen alternative is sampled, it must be the last.
        is_chosen_sampled = (sample_result['id_column'] == chosen).any()
        if is_chosen_sampled:
            self.assertEqual(sample_result.iloc[-1]['id_column'], chosen)

    def test_no_chosen(self):
        partition = (StratumTuple({1, 2}, 1), StratumTuple({3, 4, 5}, 2))
        sample_result, chosen_result = sample_alternatives(
            self.alt_df, 'id_column', partition
        )
        self.assertTrue(chosen_result is None)


class TestChoiceSetsGeneration(unittest.TestCase):
    # Setup sample data for the tests
    def setUp(self):
        self.individuals = pd.DataFrame({'individual_id': [1, 2], 'choice': [1, 2]})

        self.alternatives = pd.DataFrame(
            {'ID': [1, 2, 3, 4, 5], 'Attribute': ['A', 'B', 'C', 'D', 'E']}
        )

        self.partition = (
            StratumTuple(subset={1, 3, 4}, sample_size=2),
            StratumTuple(subset={2, 5}, sample_size=1),
        )
        self.choice_column = 'choice'
        self.id_column = 'ID'
        self.second_partition = (StratumTuple(subset={1, 2, 3, 4, 5}, sample_size=3),)

    def test_basic_functionality(self):
        result = choice_sets_generation(
            self.partition,
            self.individuals,
            self.choice_column,
            self.alternatives,
            self.id_column,
        )
        self.assertEqual(len(result), 2)
        self.assertIn('Attribute_0', result.columns)
        self.assertIn('Attribute_1', result.columns)

    def test_second_partition(self):
        result = choice_sets_generation(
            self.partition,
            self.individuals,
            self.choice_column,
            self.alternatives,
            self.id_column,
            second_partition=self.second_partition,
        )
        self.assertIn('MEV_Attribute_0', result.columns)

    def test_empty_df(self):
        empty_individuals = pd.DataFrame(columns=['individual_id', 'choice'])
        with self.assertRaises(BiogemeError):
            result = choice_sets_generation(
                self.partition,
                empty_individuals,
                self.choice_column,
                self.alternatives,
                self.id_column,
            )


class TestChoiceSetsGenerationInputValidation(unittest.TestCase):
    # Setup sample data for the tests
    def setUp(self):
        self.individuals = pd.DataFrame({'individual_id': [1, 2], 'choice': [1, 2]})

        self.alternatives = pd.DataFrame(
            {'ID': [1, 2, 3, 4, 5], 'Attribute': ['A', 'B', 'C', 'D', 'E']}
        )

        segment_1 = StratumTuple({1, 2}, 1)
        segment_2 = StratumTuple({3, 4, 5}, 2)
        self.partition = (segment_1, segment_2)
        self.choice_column = 'choice'
        self.id_column = 'ID'
        self.second_partition = (StratumTuple(subset={1, 2, 3, 4, 5}, sample_size=3),)

    def test_missing_columns(self):
        # Remove choice column
        individuals_missing_col = self.individuals.drop('choice', axis=1)
        with self.assertRaises(BiogemeError):
            choice_sets_generation(
                self.partition,
                individuals_missing_col,
                self.choice_column,
                self.alternatives,
                self.id_column,
            )

    def test_incorrect_data_types(self):
        # Change datatype of choice column to string
        individuals_wrong_dtype = self.individuals.copy()
        individuals_wrong_dtype['choice'] = individuals_wrong_dtype['choice'].astype(
            str
        )
        with self.assertRaises(BiogemeError):
            choice_sets_generation(
                self.partition,
                individuals_wrong_dtype,
                self.choice_column,
                self.alternatives,
                self.id_column,
            )

    def test_empty_strings(self):
        with self.assertRaises(BiogemeError):
            choice_sets_generation(
                self.partition,
                self.individuals,
                "",  # Empty choice column
                self.alternatives,
                self.id_column,
            )

    def test_invalid_partitions(self):
        invalid_partition = (StratumTuple(subset={10, 20, 30, 40, 50}, sample_size=3),)

        invalid_partition = [('NonexistentID', 2)]
        with self.assertRaises(BiogemeError):
            choice_sets_generation(
                invalid_partition,
                self.individuals,
                self.choice_column,
                self.alternatives,
                self.id_column,
            )

        another_invalid_partition = None
        with self.assertRaises(BiogemeError):
            choice_sets_generation(
                invalid_partition,
                self.individuals,
                self.choice_column,
                self.alternatives,
                self.id_column,
            )


if __name__ == '__main__':
    unittest.main()
