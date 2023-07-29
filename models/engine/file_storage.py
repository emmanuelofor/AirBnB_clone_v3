#!/usr/bin/python3
'''
    This module defines the FileStorage class for serializing and deserializing instances.
'''
import json
import models


class FileStorage:
    '''
        Manages serialization and deserialization of instances to a JSON file.
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''
            Returns the dictionary of objects, optionally filtered by class name.
        '''
        new_dict = {}
        if cls is None:
            return self.__objects

        if cls != "":
            for k, v in self.__objects.items():
                if cls == k.split(".")[0]:
                    new_dict[k] = v
            return new_dict
        else:
            return self.__objects

    def new(self, obj):
        '''
            Stores new instance object in the objects dictionary with key as <class name>.<id>.
        '''
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        FileStorage.__objects[key] = value_dict

    def save(self):
        '''
            Writes the object dictionary to the JSON file.
        '''
        objects_dict = {}
        for key, val in FileStorage.__objects.items():
            objects_dict[key] = val.to_dict()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objects_dict, fd)

    def reload(self):
        '''
            Loads the object dictionary from the JSON file.
        '''
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                FileStorage.__objects = json.load(fd)
            for key, val in FileStorage.__objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
                FileStorage.__objects[key] = class_name(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''
        Deletes specified instance object from the storage.
        '''
        if obj is not None:
            key = str(obj.__class__.__name__) + "." + str(obj.id)
            FileStorage.__objects.pop(key, None)
            self.save()

    def close(self):
        '''
        Calls the reload method for deserialization of JSON file to objects.
        '''
        self.reload()

    def get(self, cls, id):
        '''
            Retrieves a single object of the given class with the specified id.
        '''
        result = None

        try:
            for v in self.__objects.values():
                if v.id == id:
                    result = v
        except BaseException:
            pass

        return result

    def count(self, cls=None):
        '''
            Counts the number of instances of a specified class in the storage, or total number of all instances if no class is specified.
        '''
        cls_counter = 0

        if cls is not None:
            for k in self.__objects.keys():
                if cls in k:
                    cls_counter += 1
        else:
            cls_counter = len(self.__objects)
        return cls_counter
