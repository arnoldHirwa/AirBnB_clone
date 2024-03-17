#!/usr/bin/python3
"""A module for storing and restoring json format of a class"""


import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage():
    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        """Initialize the class"""
        pass

    def all(self):
        """A method for returning all objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Add an object to all objects"""
        FileStorage.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """serializes __objects to the JSON file"""
        path = FileStorage.__file_path
        objects = FileStorage.__objects
        objDict = {k: objects[k].to_dict() for k in objects}
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(json.dumps(objDict))

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
