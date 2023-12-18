# Tests
class TestDataIO(unittest.TestCase):
    def setUp(self):
        # Initialize the DataIO object
        self.data_io = data

    # Test loading valid file
    def test_load_valid_file(self):
        data = self.data_io.load_data("csv", self.valid_csv)
        self.assertIsInstance(data, pd.DataFrame)

    # Test file not found error
    def test_file_not_found(self):
        with self.assertRaises(Exception):
            self.data_io.load_data("csv", self.invalid_file)

    # Test unsupported file format
    def test_unsupported_format_load(self):
        with self.assertRaises(Exception):
            self.data_io.load_data("unsupported", self.valid_csv)

    # Test loading a corrupt file
    def test_corrupt_file_handling(self):
        with self.assertRaises(Exception):
            self.data_io.load_data("csv", self.corrupt_csv)

    # Test loading an empty file
    def test_empty_file_handling(self):
        with self.assertRaises(Exception):
            self.data_io.load_data("csv", self.empty_csv)

    # Test saving data
    def test_saving_data(self):
        data = pd.DataFrame({"col1": [5, 6], "col2": [7, 8]})
        self.data_io.save_data(data, "csv", "output.csv")
        self.assertTrue(os.path.exists("output.csv"))

    # Test handling of invalid data input
    def test_invalid_data_handling(self):
        invalid_data = "this is not a dataframe"
        with self.assertRaises(Exception):
            self.data_io.save_data(invalid_data, "csv", "output.csv")

    # Test unsupported format for saving
    def test_unsupported_format_save(self):
        data = pd.DataFrame({"col1": [5, 6], "col2": [7, 8]})
        with self.assertRaises(Exception):
            self.data_io.save_data(data, "unsupported", "output.csv")

    # Test overwriting an existing file
    def test_overwriting_existing_file(self):
        data = pd.DataFrame({"col1": [9, 10], "col2": [11, 12]})
        self.data_io.save_data(data, "csv", self.valid_csv)
        self.assertTrue(os.path.exists(self.valid_csv))

    # Test if csv has the right delimiter
    def test_different_csv_formats(self):
        with self.assertRaises(Exception):
            self.data_io.load_data("csv", self.delimiter_csv)

    # Test is large csvs can be imported
    def test_large_data_file(self):
        data = self.data_io.load_data("csv", self.large_csv)
        self.assertTrue(len(data) > 0)

    # test that file has the right permission
    def test_file_permissions(self):
        with self.assertRaises(Exception):
            self.data_io.load_data("csv", self.read_only_csv)

    # Test that there is no missing values in data
    def test_missing_values(self):
        data = self.data_io.load_data("csv", self.missing_values_csv)
        self.assertTrue(pd.isna(data).any().any())


if __name__ == "__main__":
    unittest.main()