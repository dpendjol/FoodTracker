from foodtracker import db
# from peewee import Model, CharField, IntegerField, DateField, ManyToManyField
from peewee import Model, CharField, IntegerField, DateField, ManyToManyField


class Food(Model):
    name = CharField(unique=True)
    protein = IntegerField()
    carbs = IntegerField()
    fats = IntegerField()

    @property
    def calories(self):
        return self.protein * 4 + self.carbs * 4 + self.fats * 9

    class Meta:
        database = db


class Log(Model):
    date = DateField()
    foods = ManyToManyField(Food, backref='logs')

    class Meta:
        database = db


log_food = Log.foods.get_through_model()

with db:
    db.create_tables([Food, Log, log_food])

if __name__ == "__main__":
    pass
