#!/usr/bin/python3
"""A module that creates the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """A class which represents a review.
    """

    place_id = ""
    user_id = ""
    text = ""
