#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Test for sacrud.common.sa_helpers
"""
from sacrud.common.sa_helpers import pk_to_list
from sacrud.tests import BaseSacrudTest, MultiPK, User


class SQLAlchemyHelpersTest(BaseSacrudTest):

    def test_table_property(self):
        user = User(u'Vasya', u'Pupkin', u"123")
        self.assertEqual(user.foo, "I'm property")

    def test_pk_to_list(self):
        user = User(u'Vasya', u'Pupkin', u"123")
        self.assertEqual(pk_to_list(user), ['id', None])
        self.assertEqual(pk_to_list(user, as_json=True),
                         '["id", null]')
        user.id = 100500
        self.assertEqual(pk_to_list(user), ['id', 100500])

        multipk = MultiPK(id=1, id2=1, id3=2, fk=1)
        self.assertEqual(pk_to_list(multipk),
                         ['id', 1, 'id2', 1, 'id3', 2])

        # JSON
        self.assertEqual(pk_to_list(multipk, as_json=True),
                         '["id", 1, "id2", 1, "id3", 2]')
