#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Test for sacrud.common
"""
from sacrud.common import import_from_string
from sacrud.tests.test_models import User


class CommonTest(object):

    def test_import_from_string(self):
        self.assertEqual(User,
                         import_from_string('sacrud.tests.test_models:User'))
