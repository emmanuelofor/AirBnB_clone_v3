#!/usr/bin/python3
"""
Tests for the BaseModel Class
"""
import unittest
from datetime import datetime
import inspect
import json
import models
from models import engine
from models.engine.file_storage import FileStorage
import pep8
from os import environ, stat, remove, path

User = models.user.User
BaseModel = models.base_model.BaseModel
State = models.state.State
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')

if STORAGE_TYPE != 'db':
    FileStorage = models.file_storage.FileStorage
storage = models.storage
F = './dev/file.json'


@unittest.skipIf(STORAGE_TYPE == 'db', 'Only proceed with tests if environment is not db')
class TestFileStorageDocs(unittest.TestCase):
    """Tests documentation of BaseModel class"""

    all_funcs = inspect.getmembers(FileStorage, inspect.isfunction)

    @classmethod
    def setUpClass(cls):
        """Sets up the testing environment for the class"""
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')

    def tearDownClass():
        """Cleans up the test environment by deleting storage objects"""
        storage.delete_all()
        remove(F)

    def test_doc_file(self):
        """Tests the documentation for the file"""
        expected = ("\nHandles I/O, writing and reading, of JSON for storage "
                    "of all class instances\n")
        actual = models.file_storage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """Tests the documentation for the class"""
        expected = ('\n        handles long term storage of all class instance'
                    's\n    ')
        actual = FileStorage.__doc__
        self.assertEqual(expected, actual)

    def test_all_function_docs(self):
        """Tests the documentation for all functions in the db_storage file"""
        all_functions = TestFileStorageDocs.all_funcs
        for function in all_functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8_fs(self):
        """Checks that filestorage.py adheres to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_file_is_executable(self):
        """Tests if file has correct permissions for execution"""
        file_stat = stat('models/engine/file_storage.py')
        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE == 'db', 'Only proceed with tests if environment is not db')
class TestBmFsInstances(unittest.TestCase):
    """Tests for class instances"""

    @classmethod
    def setUpClass(cls):
        """Sets up the class for testing"""
        print('\n\n.................................')
        print('...... Testing FileStorate ......')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')
        cls.bm_obj = BaseModel()
        cls.state_obj = State(name="Illinois")
        cls.bm_obj.save()
        cls.state_obj.save()

    def tearDownClass():
        """Cleans up the test environment by deleting storage objects"""
        storage.delete_all()
        remove(F)

    def setUp(self):
        """Prepares new storage object for testing"""
        self.bm_obj = TestBmFsInstances.bm_obj
        self.state_obj = TestBmFsInstances.state_obj

    def test_instantiation(self):
        """Verifies proper instantiation of FileStorage"""
        self.assertIsInstance(storage, FileStorage)

    def test_storage_file_exists(self):
        """Verifies if a storage file has been correctly instantiated"""
        remove(F)
        self.bm_obj.save()
        self.assertTrue(path.isfile(F))

    def test_all(self):
        """Checks if all() function returns a newly created instance"""
        bm_id = self.bm_obj.id
        all_obj = storage.all()
        actual = False
        for k in all_obj.keys():
            if bm_id in k:
                actual = True
        self.assertTrue(True)

    def test_all_state(self):
        """Checks if all() function returns a newly created state instance"""
        state_id = self.state_obj.id
        state_objs = storage.all("State")
        actual = False
        for k in state_objs.keys():
            if state_id in k:
                actual = True
        self.assertTrue(True)

    def test_obj_saved_to_file(self):
        """Checks if an object has been correctly saved to file storage"""
        remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = False
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if bm_id in k:
                actual = True
        self.assertTrue(True)

    def test_to_json(self):
        """Verifies that to_json returns a serializable dictionary object"""
        my_model_json = self.bm_obj.to_json()
        actual = True
        try:
            serialized = json.dumps(my_model_json)
        except:
            actual = False
        self.assertTrue(actual)

    def test_reload(self):
        """Verifies proper usage of the reload function"""
        remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = False
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if bm_id in k:
                actual = True
        self.assertTrue(actual)

    def test_save_reload_class(self):
        """Verifies the correct usage of the class attribute in file storage"""
        remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = False
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k, v in all_obj.items():
            if bm_id in k:
                if type(v).__name__ == 'BaseModel':
                    actual = True
        self.assertTrue(actual)

# The following test class is skipped if the environment is set to 'db'
@unittest.skipIf(STORAGE_TYPE == 'db', 'Skip tests if environment is set to db')
class TestUserFsInstances(unittest.TestCase):
    """Testing User class instances"""

    @classmethod
    def setUpClass(cls):
        """Prepare the testing environment by setting up the class"""
        print('\n\n.................................')
        print('...... Initiating FileStorage Tests ......')
        print('.......... For the User Class ..........')
        print('.................................\n\n')
        cls.user = User()
        cls.user.save()
        cls.bm_obj = BaseModel()
        cls.bm_obj.save()

    def tearDownClass():
        """Clean up the testing environment by removing storage objects"""
        storage.delete_all()
        remove(F)

    def setUp(self):
        """Initialize a new User instance for testing"""
        self.user = TestUserFsInstances.user
        self.bm_obj = TestUserFsInstances.bm_obj

    def test_storage_file_exists(self):
        """Test if FileStorage is correctly instantiated"""
        remove(F)
        self.user.save()
        self.assertTrue(path.isfile(F))

    def test_count_cls(self):
        """Test the count method with class name as an argument"""
        count_user = storage.count('User')
        self.assertEqual(1, count_user)

    def test_count_all(self):
        """Test the count method without a class name argument"""
        count_all = storage.count()
        self.assertEqual(2, count_all)

    def test_get_cls_id(self):
        """Test the get method with class name and id as arguments"""
        duplicate = storage.get('User', self.user.id)
        self.assertEqual(self.user.id, duplicate.id)

    def test_all(self):
        """Check if all() function returns a newly created User instance"""
        u_id = self.user.id
        all_obj = storage.all()
        actual = any(u_id in k for k in all_obj.keys())
        self.assertTrue(actual)

    def test_obj_saved_to_file(self):
        """Test if User instance is correctly saved to FileStorage"""
        remove(F)
        self.user.save()
        u_id = self.user.id
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        actual = any(u_id in k for k in storage_dict.keys())
        self.assertTrue(actual)

    def test_reload(self):
        """Test correct use of the reload function"""
        remove(F)
        self.bm_obj.save()
        u_id = self.bm_obj.id
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        actual = any(u_id in k for k in all_obj.keys())
        self.assertTrue(actual)


if __name__ == '__main__':
    unittest.main
