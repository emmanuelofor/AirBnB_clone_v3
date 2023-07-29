#!/usr/bin/python3
"""
This is the unit testing module for the BaseModel Class.
"""
import unittest
from datetime import datetime
from models import *
import inspect
from os import environ, stat
import pep8
from models.base_model import Base
from models.engine.db_storage import DBStorage

STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@unittest.skipIf(STORAGE_TYPE != 'db', 'Test skipped if storage type is not database')
class TestDBStorageDocs(unittest.TestCase):
    """This is the class for testing documentation of BaseModel"""

    all_funcs = inspect.getmembers(DBStorage, inspect.isfunction)

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For DB Storage Class .....')
        print('.................................\n\n')

    def tearDownClass():
        """Clean up after tests by removing storage objects"""
        storage.delete_all()

    def test_doc_file(self):
        """Test the documentation for the file"""
        expected = '\nDatabase engine\n'
        actual = db_storage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """Test the documentation for the class"""
        expected = ('\n        handles long term storage of all class instance'
                    's\n    ')
        actual = DBStorage.__doc__
        self.assertEqual(expected, actual)

    def test_all_function_docs(self):
        """Test the documentation for all functions in db_storage file"""
        all_functions = TestDBStorageDocs.all_funcs
        for function in all_functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8_db(self):
        """Test that db_storage.py conforms to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_file_is_executable(self):
        """Test that the file has the correct permissions for user execution"""
        file_stat = stat('models/engine/db_storage.py')
        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE != 'db', "DB Storage doesn't use FileStorage")
class TestTracebackNullError(unittest.TestCase):
    """Class for testing traceback errors due to:
    missing attributes that Cannot be NULL"""

    @classmethod
    def setUpClass(cls):
        """Setup for the class before starting the tests"""
        print('\n\n....................................')
        print('.......... Testing DBStorage .......')
        print('...... Trying to Throw Errors ......')
        print('....................................\n\n')

    def tearDownClass():
        """Clean up after tests by removing storage objects"""
        storage.delete_all()

    def tearDown(self):
        """Cleanup after tests that throw errors"""
        storage.rollback_session()

    def test_state_no_name(self):
        """Test creating a state without a name"""
        with self.assertRaises(Exception) as context:
            s = State()
            s.save()
        self.assertTrue('"Column \'name\' cannot be null"'
                        in str(context.exception))

    def test_city_no_state(self):
        """Test creating a city with an invalid state"""
        with self.assertRaises(Exception) as context:
            c = City(name="Tapioca", state_id="NOT VALID")
            c.save()
        self.assertTrue('a child row: a foreign key constraint fails'
                        in str(context.exception))

    def test_place_no_user(self):
        """Test creating a place without a city"""
        with self.assertRaises(Exception) as context:
            p = Place()
            p.save()
        self.assertTrue('"Column \'city_id\' cannot be null"'
                        in str(context.exception))

    def test_review_no_text(self):
        """Test creating a Review without text"""
        with self.assertRaises(Exception) as context:
            r = Review()
            r.save()
        self.assertTrue('"Column \'text\' cannot be null"'
                        in str(context.exception))

    def test_amenity_no_name(self):
        """Test creating an amenity without a name"""
        with self.assertRaises(Exception) as context:
            a = Amenity()
            a.save()
        self.assertTrue('"Column \'name\' cannot be null"'
                        in str(context.exception))

    def test_user_no_name(self):
        """Test creating a user without an email"""
        with self.assertRaises(Exception) as context:
            u = User()
            u.save()
        self.assertTrue('"Column \'email\' cannot be null"'
                        in str(context.exception))


@unittest.skipIf(STORAGE_TYPE != 'db', 'Test skipped if storage type is not database')
class TestStateDBInstances(unittest.TestCase):
    """Class for testing State class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('....... Testing DBStorage .......')
        print('........ For State Class ........')
        print('.................................\n\n')

    def tearDownClass():
        """Clean up after tests by removing storage objects"""
        storage.delete_all()

    def setUp(self):
        """Creates a new State instance for testing"""
        self.state = State()
        self.state.name = 'California'
        self.state.save()

    def test_state_all(self):
        """Confirms if the all() method retrieves the newly created State instance"""
        all_objs = storage.all()
        all_state_objs = storage.all('State')

        exist_in_all = False
        for k in all_objs.keys():
            if self.state.id in k:
                exist_in_all = True
        exist_in_all_states = False
        for k in all_state_objs.keys():
            if self.state.id in k:
                exist_in_all_states = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_states)

    def test_new_state(self):
        """Validates if the new() method functions as expected after instantiation and save()"""
        actual = False
        self.s_new = State(name="Illinois")
        self.s_new.save()
        db_objs = storage.all()
        for obj in db_objs.values():
            if obj.id == self.s_new.id:
                actual = True
        self.assertTrue(actual)

    def test_state_delete(self):
        """Verifies if the delete method removes the state instance as expected"""
        state_id = self.state.id
        storage.delete(self.state)
        storage.save()
        exist_in_all = False
        for k in storage.all().keys():
            if state_id in k:
                exist_in_all = True
        self.assertFalse(exist_in_all)


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestUserDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('.......... User  Class ..........')
        print('.................................\n\n')

    def tearDownClass():
        """Cleans up after tests by removing storage objects"""
        storage.delete_all()

    def setUp(self):
        """Creates a new User instance for testing"""
        self.user = User()
        self.user.email = 'test'
        self.user.password = 'test'
        self.user.save()

    def test_user_all(self):
        """Confirms if the all() method retrieves the newly created User instance"""
        all_objs = storage.all()
        all_user_objs = storage.all('User')
        exist_in_all = False
        for k in all_objs.keys():
            if self.user.id in k:
                exist_in_all = True
        exist_in_all_users = False
        for k in all_user_objs.keys():
            if self.user.id in k:
                exist_in_all_users = True
        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_users)

    def test_user_delete(self):
        """Verifies if the delete method removes the User instance as expected"""
        user_id = self.user.id
        storage.delete(self.user)
        self.user = None
        storage.save()
        exist_in_all = False
        for k in storage.all().keys():
            if user_id in k:
                exist_in_all = True
        self.assertFalse(exist_in_all)


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestCityDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing DBStorage ......')
        print('.......... City  Class ..........')
        print('.................................\n\n')

    def tearDownClass():
        """Cleans up after tests by removing storage objects"""
        storage.delete_all()

    def setUp(self):
        """Creates a new City instance for testing"""
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city = City()
        self.city.name = 'Fremont'
        self.city.state_id = self.state.id
        self.city.save()

    def test_city_all(self):
        """Confirms if the all() method retrieves the newly created City instance"""
        all_objs = storage.all()
        all_city_objs = storage.all('City')

        exist_in_all = False
        for k in all_objs.keys():
            if self.city.id in k:
                exist_in_all = True
        exist_in_all_city = False
        for k in all_city_objs.keys():
            if self.city.id in k:
                exist_in_all_city = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_city)


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestCityDBInstancesUnderscore(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing DB Storage ......')
        print('.......... City Class ..........')
        print('.................................\n\n')

    def tearDownClass():
        """Cleans up the testing environment by removing storage objects"""
        storage.delete_all()

    def setUp(self):
        """Sets up a new City instance for testing"""
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city = City()
        self.city.name = 'San_Francisco'
        self.city.state_id = self.state.id
        self.city.save()

    def test_city_underscore_all(self):
        """Verifies if the all() function retrieves the newly created City instance"""
        all_objs = storage.all()
        all_city_objs = storage.all('City')

        exist_in_all = False
        for k in all_objs.keys():
            if self.city.id in k:
                exist_in_all = True
        exist_in_all_city = False
        for k in all_city_objs.keys():
            if self.city.id in k:
                exist_in_all_city = True
        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_city)


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestPlaceDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing DBStorage ......')
        print('.......... Place  Class ..........')
        print('.................................\n\n')

    def tearDownClass():
        """Cleans up the testing environment by removing storage objects"""
        storage.delete_all()

    def setUp(self):
        """Sets up a new Place instance for testing"""
        self.user = User()
        self.user.email = 'test'
        self.user.password = 'test'
        self.user.save()
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city = City()
        self.city.name = 'San_Mateo'
        self.city.state_id = self.state.id
        self.city.save()
        self.place = Place()
        self.place.city_id = self.city.id
        self.place.user_id = self.user.id
        self.place.name = 'test_place'
        self.place.description = 'test_description'
        self.place.number_rooms = 2
        self.place.number_bathrooms = 1
        self.place.max_guest = 4
        self.place.price_by_night = 100
        self.place.latitude = 120.12
        self.place.longitude = 101.4
        self.place.save()

    def test_place_all(self):
        """Verifies if the all() function retrieves the newly created Place instance"""
        all_objs = storage.all()
        all_place_objs = storage.all('Place')

        exist_in_all = False
        for k in all_objs.keys():
            if self.place.id in k:
                exist_in_all = True
        exist_in_all_place = False
        for k in all_place_objs.keys():
            if self.place.id in k:
                exist_in_all_place = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_place)


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestCountGet(unittest.TestCase):
    """testing Count and Get methods"""

    @classmethod
    def setUpClass(cls):
        """Prepares the testing class with required objects"""
        print('\n\n....................................')
        print('.......... Evaluating DBStorage .......')
        print('. State, City, User, Place Amenity .')
        print('....................................')
        storage.delete_all()
        cls.s = State(name="California")
        cls.c = City(state_id=cls.s.id,
                     name="San Francisco")
        cls.u = User(email="betty@holbertonschool.com",
                     password="pwd")
        cls.p1 = Place(user_id=cls.u.id,
                       city_id=cls.c.id,
                       name="a house")
        cls.p2 = Place(user_id=cls.u.id,
                       city_id=cls.c.id,
                       name="a house two")
        cls.a1 = Amenity(name="Wifi")
        cls.a2 = Amenity(name="Cable")
        cls.a3 = Amenity(name="Bucket Shower")
        objs = [cls.s, cls.c, cls.u, cls.p1, cls.p2, cls.a1, cls.a2, cls.a3]
        for obj in objs:
            obj.save()

    def setUp(self):
        """Sets up new instances for testing from the TestCountGet class"""
        self.s = TestCountGet.s
        self.c = TestCountGet.c
        self.u = TestCountGet.u
        self.p1 = TestCountGet.p1
        self.p2 = TestCountGet.p2
        self.a1 = TestCountGet.a1
        self.a2 = TestCountGet.a2
        self.a3 = TestCountGet.a3

    def test_all_reload_save(self):
        """Verifies if all(), save(), and reload functions operate correctly with a new instance.
        This method also serves to test the reload function."""
        actual = 0
        db_objs = storage.all()
        for obj in db_objs.values():
            for x in [self.s.id, self.c.id, self.u.id, self.p1.id]:
                if x == obj.id:
                    actual += 1
        self.assertTrue(actual == 4)

    def test_get_pace(self):
        """Checks if the get() function retrieves the appropriate instance"""
        duplicate = storage.get('Place', self.p1.id)
        expected = self.p1.id
        self.assertEqual(expected, duplicate.id)

    def test_count_amenity(self):
        """Validates if the count() function returns the correct count when given a Class as input"""
        count_amenity = storage.count('Amenity')
        expected = 3
        self.assertEqual(expected, count_amenity)

    def test_count_all(self):
        """Assesses if the count() function works properly when not provided with a class"""
        count_all = storage.count()
        expected = 8
        self.assertEqual(expected, count_all)

if __name__ == '__main__':
    unittest.main
