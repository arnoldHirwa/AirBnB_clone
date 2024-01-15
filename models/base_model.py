#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """A class for the BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """creates a new BaseModel.
        """
        form_t = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, form_t)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        """Update updated_at basing on time"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Provides dictionary of the BaseModel instance.
        """
        dict_r = self.__dict__.copy()
        dict_r["created_at"] = self.created_at.isoformat()
        dict_r["updated_at"] = self.updated_at.isoformat()
        dict_r["__class__"] = self.__class__.__name__
        return dict_r

    def __str__(self):
        """Provides the print/str representation of the BaseModel instance."""
        str_name = self.__class__.__name__
        return "[{}] ({}) {}".format(str_name, self.id, self.__dict__)
