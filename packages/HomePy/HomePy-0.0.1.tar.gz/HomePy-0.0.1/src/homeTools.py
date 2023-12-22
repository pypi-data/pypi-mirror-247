#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-12-22 16:55
# @Author  : Jack
# @File    : homeTools.py

"""
homeTools
"""
import random
import string


def getRandomId(length=10):
    """
    getRandomId
    :param length:
    :return:
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
