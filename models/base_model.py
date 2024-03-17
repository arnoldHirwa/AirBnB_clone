#!/usr/bin/python3
import uuid
from datetime import datetime
import models


class BaseModel():
    "A base class for other classes"
    def __init__(self, *args, **kwargs):
        if (kwargs and kwargs != {}):
            format = "%Y-%m-%dT%H:%M:%S.%f"
            for key, value in kwargs.items():
                # print("key: ", key, "value: ", value)
                if key == "created_at":
                    self.created_at = datetime.strptime(value, format)
                elif key == "updated_at":
                    self.updated_at = datetime.strptime(value, format)
                elif key == "id":
                    self.id = value
                elif key == "my_number":
                    self.my_number = value
                elif key == "name":
                    self.name = value
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.today()
            self.updated_at = datetime.today()
            models.storage.new(self)

    def save(self):
        "A method for saving the current state of class"
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        "A method for returning a json representation of a class"
        allInstances = self.__dict__.copy()
        allInstances["__class__"] = self.__class__.__name__
        allInstances["created_at"] = self.created_at.isoformat()
        allInstances["updated_at"] = self.updated_at.isoformat()
        return allInstances

    def __str__(self):
        "A method for printing a string representation of a class"
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
