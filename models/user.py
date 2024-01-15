#!/usr/bin/python3
"""A module that creates the User class."""
from models.base_model import BaseModel


class User(BaseModel):
    """A class for new created User.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
