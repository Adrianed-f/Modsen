import unittest
import os
import shutil
from PIL import Image
from compare_folders import compare_folders

class TestCompareFoldersWithDuplicates(unittest.TestCase):

    def setUp(self):
        self.folder1 = 'tests/test_images_folder1'
        self.folder2 = 'tests/test_images_folder2'
        os.makedirs(self.folder1, exist_ok=True)
        os.makedirs(self.folder2, exist_ok=True)
        # Create identical dummy images
        img = Image.new('RGB', (10, 10), color = 'red')
        img.save(os.path.join(self.folder1, 'test_image.jpg'))
        img.save(os.path.join(self.folder2, 'test_image.jpg'))

    def tearDown(self):
        shutil.rmtree(self.folder1)
        shutil.rmtree(self.folder2)

    def test_compare_folders_with_duplicates(self):
        duplicates = compare_folders(self.folder1, self.folder2)
        self.assertEqual(len(duplicates), 1)

if __name__ == '__main__':
    unittest.main()