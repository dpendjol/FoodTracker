from foodtracker.models import Food
from peewee import SqliteDatabase

def other_db(dbs):
    test_db = SqliteDatabase(":memory:")
    with test_db.bind_ctx(dbs):
        test_db.create_tables(dbs)
        try:
            food, create = Food.get_or_create(name="Food", protein=10, carbs=10, fats=10)
            print(food.name)
            print(food.carbs)
            query = Food.select()
            for item in query:
                print(item)
        except:
            print("Something went wrong")
            
if __name__ == "__main__":
    other_db(Food)