class QueryBuilder(object):

    SELECT_KIND = 1
    UPDATE_KIND = 2
    DELETE_KIND = 3
    INSERT_KIND = 4

    def __init__(self, table, columns=[]):
        self.__table = table
        self.__columns = columns
        self.__kind = self.SELECT_KIND
        self.__where = []
        self.__or_where = []
        self.__returning = []
        self.__order_by = []
        self.__limit = None
        self.__offset = None
        self.__join_kind = None
        self.__join_table = None
        self.__join_columns = []
        self.__join_on_conditions = []

    def insert(self):
        self.__kind = self.INSERT_KIND
        return self

    def delete(self):
        self.__kind = self.DELETE_KIND
        return self

    def update(self):
        self.__kind = self.UPDATE_KIND
        return self

    def select(self):
        self.__kind = self.SELECT_KIND
        return self

    def limit(self, limit):
        self.__limit = limit
        return self

    def offset(self, offset):
        self.__offset = offset
        return self

    def order_by(self, column, direction='ASC'):
        self.__order_by.append((column, direction))
        return self

    def where(self, column, condition='=', value='%s'):
        self.__where.append((column, condition, value))
        return self

    def or_where(self, column, condition='=', value='%s'):
        self.__or_where.append((column, condition, value))
        return self

    def returning(self, columns):
        self.__returning = list(columns)
        return self
    
    def join(self, table, columns=[], kind='INNER'):
        self.__join_table = table
        self.__join_kind = kind
        self.__join_columns = ['{}.{}'.format(table, c) for c in columns]
        return self
    
    def on(self, column, condition='=', value='%s'):
        self.__join_on_conditions.append((column, condition, value))
        return self
    
    def sql(self):
        if self.__kind == self.INSERT_KIND:
            query = self.sql_insert()

        elif self.__kind == self.UPDATE_KIND:
            query = self.sql_update()

        elif self.__kind == self.DELETE_KIND:
            query = self.sql_delete()

        elif self.__kind == self.SELECT_KIND:
            query = self.sql_select()

        return query

    def sql_insert(self):
        query = '''
        INSERT INTO {} ({})
        VALUES ({})
        '''.format(
            self.__table,
            ', '.join(self.__columns),
            ', '.join(['%s' for c in self.__columns])
        )

        if self.returning:
            query += '''
            RETURNING {}
            '''.format(', '.join(self.__returning))

        return query

    def sql_update(self):
        query = '''
        UPDATE {}
        SET {}
        '''.format(
            self.__table,
            ', '.join(['{} = %s'.format(c) for c in self.__columns])
        )

        if self.__where:
            query = self.sql_inject_wheres(query)

        return query

    def sql_delete(self):
        query = '''
        DELETE FROM {}
        '''.format(self.__table)

        if self.__where:
            query = self.sql_inject_wheres(query)

        return query

    def sql_select(self):
        query = '''
        SELECT {}
        FROM {}
        '''.format(
            ', '.join(self.__columns + self.__join_columns),
            self.__table
        )
        
        if self.__join_table:
            query += '''
            {} JOIN {}
            ON ({})
            '''.format(
                self.__join_kind,
                self.__join_table,
                ' AND '.join(['{} {} {}'.format(*o) for o in self.__join_on_conditions])
            )

        if self.__where:
            query = self.sql_inject_wheres(query)

        if self.__order_by:
            query += '''
            ORDER BY {}
            '''.format(', '.join(['{} {}'.format(*o) for o in self.__order_by]))

        if self.__limit is not None:
            query += '''
            LIMIT {}
            '''.format(self.__limit)

        if self.__offset is not None:
            query += '''
            OFFSET {}
            '''.format(self.__offset)

        return query

    def sql_inject_wheres(self, query):
        query += '''
        WHERE ({})
        '''.format(
            ' AND '.join(['{} {} {}'.format(*w) for w in self.__where])
        )

        if self.__or_where:
            query += '''
            OR ({})
            '''.format(
                ' AND '.join(['{} {} {}'.format(*w) for w in self.__or_where])
            )

        return query
