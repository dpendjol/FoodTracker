from peewee import SqliteDatabase

# db = SqliteDatabase(':memory:', pragmas={'foreign_keys': 1})
db = SqliteDatabase('foodtracker.db', pragmas={'foreign_keys': 1})