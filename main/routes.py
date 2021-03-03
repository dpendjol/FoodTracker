from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Food

main = Blueprint("main", __name__)

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/add', methods=["GET"])
def add():
    foods = Food.select()
    return render_template("add.html", foods=foods, food=None)

@main.route('/add', methods=["POST"])
def add_post():
    food_id = request.form.get('food-id')
    food = request.form.get('food-name')
    proteins = request.form.get('protein')
    carbs = request.form.get('carbohydrates')
    fats = request.form.get('fat')
    
    if food_id:
        result = Food.update(name=food,
                              protein=proteins,
                              carbs=carbs,
                              fats=fats).where(Food.id==food_id).execute()
        
        if result == 1:
            flash("Food item is updated", "succes")
        elif result > 1:
            flash("Something strange happend, multiple items where updated", "warning")
        elif result < 1:
            flash("No item found", "error")
    else:
        _, isCreated = Food.get_or_create(name=food,
                                        defaults={'protein': proteins,
                                                    'carbs': carbs,
                                                    'fats': fats})
        if isCreated:
            flash("Food is created", "succes")
        else:
            flash("Food already exists", "error")
        
    return redirect(url_for("main.add"))

@main.route('/delete_food/<int:food_id>')
def delete_food(food_id):
    '''
    Deletes a row from the database and redirects to add page
    
    Arguments:
    food_id -- int: id of the row in de database
    
    '''
    
    result = Food.delete().where(Food.id == food_id).execute()
    
    if result == 1:
        flash("Food item is deleted", "succes")
    elif result > 1:
        flash("Something strange happend, multiple items where deleted", "warning")
    elif result < 1:
        flash("No item found", "error")
        
    return redirect(url_for("main.add"))

@main.route('/edit_food/<int:food_id>')
def edit_food(food_id):
    food = Food.get(Food.id == food_id)
    foods = Food.select()
    return render_template("add.html", foods=foods, food=food)
        
@main.route('/view')
def view():
    foods = Food.select()
    return render_template("view.html", foods=foods)