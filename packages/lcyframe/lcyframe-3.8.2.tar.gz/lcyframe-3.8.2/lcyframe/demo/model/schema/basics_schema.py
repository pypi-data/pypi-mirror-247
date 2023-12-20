#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bson.objectid import ObjectId
from base import BaseSchema, utils
import time, datetime


class BasicsSchema(BaseSchema):
    """
    基础功能
    """

    collection = "basics"

    def __init__(self):
        self._id = ObjectId()

