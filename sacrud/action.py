#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
CREATE, READ, DELETE, UPDATE actions for SQLAlchemy models
"""
import transaction

from .common import columns_by_group, get_obj, get_pk
from .preprocessing import ObjPreprocessing

prefix = 'crud'


class CRUD(object):
    """ Main class for CRUD actions

        :Parameters:

            - `session`: SQLAlchemy DBSession
            - `table`: SQLAlchemy model
            - `pk`: obj primary keys
            - `request`: web request
    """
    def __init__(self, session, table, pk=None, request=None):
        self.pk = get_pk(table)
        self.table = table
        self.request = request
        self.session = session
        self.obj = get_obj(session, table, pk)

    def rows_list(self):
        """
        Return a list of table rows.

        :Parameters:

            - `order_by`: name ordered row.
            - `paginator`: see sacrud.common.paginator.get_paginator.
        """
        table = self.table
        session = self.session
        col = [c for c in getattr(table, 'sacrud_list_col',
                                  table.__table__.columns)]
        row = session.query(table)
        return {'row': row,
                'pk': self.pk,
                'col': col,
                'table': table,
                'prefix': prefix,
                }

    def add(self):
        """ Update row of table.

        :Example:

        .. code-block:: python

            resp = action.CRUD(dbsession, table, pk)
            resp.request = params
            resp.add()
        """
        if self.request:
            self.obj = ObjPreprocessing(obj=self.obj or self.table)\
                .add(self.session, self.request, self.table)
            self.session.add(self.obj)
            transaction.commit()
            return self.obj
        columns = columns_by_group(self.table)
        return {'obj': self.obj,
                'pk': self.pk,
                'col': columns,
                'table': self.table,
                'prefix': prefix}

    def delete(self, commit=True):
        """ Delete row by pk.

        :Example:

        .. code-block:: python

            action.CRUD(dbsession, table, pk=pk).delete()

        If you no needed commit session

        .. code-block:: python

            action.CRUD(dbsession, table, pk=pk).delete(commit=False)
        """
        obj = ObjPreprocessing(obj=self.obj).delete()
        self.session.delete(obj)
        if commit is True:
            transaction.commit()
        return self.pk
