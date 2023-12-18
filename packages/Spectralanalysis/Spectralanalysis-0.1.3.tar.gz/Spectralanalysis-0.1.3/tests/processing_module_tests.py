# TESTS
class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        self.data_proc = data
        self.sample_data = pd.DataFrame(
            {"spectral_intensity": np.random.rand(100), "noise": np.random.rand(100)}
        )

    # Check how clean_data is implemented
    def test_clean_data(self):
        cleaned_data = self.data_proc.clean_data(self.sample_data)
        self.assertIsInstance(cleaned_data, pd.DataFrame)

    def test_clean_data_with_empty_columns(self):
        data_with_empty_col = self.sample_data.assign(empty_col=np.nan)
        cleaned_data = self.data_proc.clean_data(data_with_empty_col)
        self.assertNotIn("empty_col", cleaned_data.columns)

    # Check if data is normalized (e.g., min-max normalization)
    def test_normalize_data(self):
        normalized_data = self.data_proc.normalize_data(self.sample_data)
        self.assertAlmostEqual(normalized_data.min(), 0)
        self.assertAlmostEqual(normalized_data.max(), 1)

    # Check if data is transformed correctly (e.g., type, shape)
    def test_transform_data_fourier(self):
        transformed_data = self.data_proc.transform_data(self.sample_data, "Fourier")
        self.assertIsInstance(transformed_data, np.ndarray)

    def test_normalize_data_with_constant_values(self):
        constant_data = pd.DataFrame({"constant": [5] * 100})
        normalized_data = self.data_proc.normalize_data(constant_data)
        self.assertTrue((normalized_data["constant"] == 0).all())

    def test_normalize_data_integrity(self):
        normalized_data = self.data_proc.normalize_data(self.sample_data)
        self.assertEqual(len(normalized_data), len(self.sample_data))

    def test_transform_data_invalid_method(self):
        with self.assertRaises(NotImplementedError):
            self.data_proc.transform_data(self.sample_data, "invalid_method")

    def test_handling_invalid_input(self):
        with self.assertRaises(TypeError):
            self.data_proc.clean_data("not a dataframe")

    def test_empty_dataframe_handling(self):
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.data_proc.clean_data(empty_df)

    # Test cleaning data with non-numeric columns
    def test_clean_data_non_numeric_columns(self):
        data_with_text = self.sample_data.assign(text_col=["text"] * 100)
        cleaned_data = self.data_proc.clean_data(data_with_text)
        self.assertIn("text_col", cleaned_data.columns)

    # Test normalizing data containing negative values
    def test_normalize_data_negative_values(self):
        data_with_negatives = pd.DataFrame({"negatives": range(-50, 50)})
        normalized_data = self.data_proc.normalize_data(data_with_negatives)
        self.assertTrue(normalized_data["negatives"].min() >= 0)

    # Test transforming data with multiple columns
    def test_transform_data_multiple_columns(self):
        transformed_data = self.data_proc.transform_data(self.sample_data, "Fourier")
        self.assertEqual(transformed_data.shape[1], self.sample_data.shape[1])

    # Test normalization with max equals min in a column
    def test_normalize_data_edge_cases(self):
        constant_data = pd.DataFrame({"constant": [5, 5, 5]})
        with self.assertRaises(ZeroDivisionError):
            self.data_proc.normalize_data(constant_data)

    # Test cleaning data where all values are missing
    def test_clean_data_all_missing_values(self):
        all_missing_data = pd.DataFrame(
            {"col1": [np.nan] * 100, "col2": [np.nan] * 100}
        )
        cleaned_data = self.data_proc.clean_data(all_missing_data)
        self.assertTrue(cleaned_data.empty)

    # Test transforming an empty DataFrame
    def test_transform_data_empty_dataframe(self):
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.data_proc.transform_data(empty_df, "Fourier")

    # Test different data types
    def test_mixed_data_types_handling(self):
        mixed_data = self.sample_data.assign(text_col=["text"] * 100)
        with self.assertRaises(Exception):
            self.data_proc.normalize_data(mixed_data)


if __name__ == "__main__":
    unittest.main()