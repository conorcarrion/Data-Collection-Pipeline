import unittest
import os
from lib.FileManager import FileManager
from lib.Spirit import Spirit


class FileManagerTestCase(unittest.TestCase):
    def test_unpack_inverts_output_list(self):
        test_list = ["x", "y", "z"]
        FileManager.output_list_to_text_file(test_list, "tests")
        actual_list = FileManager.unpack_text_to_python_list("tests/url_list.text")
        self.assertEqual(["x", "y", "z"], actual_list)
        os.remove("tests/url_list.text")

    def test_unpack_inverts_output_json(self):
        test_spirit = Spirit()
        test_spirit.name = "test"
        test_spirit.brand_name = "test"
        test_spirit.subname = "test"
        test_spirit.product_id = "test"
        test_spirit.product_uuid = "test"
        test_spirit.contents_liquid_volume = "70cl"
        test_spirit.alcohol_by_volume = "40%"
        test_spirit.price = 50
        test_spirit.description = "tasteless"
        test_spirit.facts = {"x": 1, "y": 2, "z": 3}
        test_spirit.flavour_style = {"x": 1, "y": 2, "z": 3}
        test_spirit.flavour_character = ["x", "y", "z"]
        test_spirit.filepath = "tests"
        expected_dict = test_spirit.__dict__

        FileManager.output_spirit_to_data_file(test_spirit, "")
        actual_dict = FileManager.unpack_json_file("tests/data.json")

        self.assertDictEqual(expected_dict, actual_dict)
        os.remove("tests/data.json")


unittest.main(argv=[""], verbosity=3, exit=False)
