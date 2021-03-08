from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Food, Log, log_food
from datetime import datetime

main = Blueprint("main", __name__)

@main.route('/')
def index():
    logs = Log.select().order_by(Log.date.desc())
    
    log_info = []
    
    for log in logs:
        proteins = 0
        carbs = 0
        fats = 0
        calories = 0
        
        for food in log.foods:
            proteins += food.protein
            carbs += food.carbs
            fats += food.fats
            calories += food.calories
        
        log_info.append({
            'id': log.id,
            'date': log.date,
            'proteins': proteins,
            'carbs': carbs,
            'fats': fats,
            'calories': calories
        })
            
    return render_template("index.html", logs=log_info)

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
        test, isCreated = Food.get_or_create(name=food,
                                        defaults={'protein': proteins,
                                                    'carbs': carbs,
                                                    'fats': fats})
        
        print(test)
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
        
@main.route('/view/<int:log_id>')
def view(log_id):
    foods = Food.select()
    dateobj = Log.select(Log.date).where(Log.id==log_id).get()
    date = dateobj.date.strftime('%B %d, %Y')
    log_foods = (Food.select()
                 .join(log_food, 
                       on=(Food.id == log_food.food_id))
                 .where(log_food.log_id==log_id))
    totals = {
        'protein': 0,
        'carbs': 0,
        'fats': 0,
        'calories': 0
    }
    for item in log_foods:
        totals['protein'] += item.protein
        totals['carbs'] += item.carbs
        totals['fats'] += item.fats
        totals['calories'] += item.calories
        
    return render_template("view.html", foods=foods, date=date, log_foods=log_foods, log_id=log_id, totals=totals)

@main.route('/create_log', methods=['POST'])
def create_log():
    date = request.form.get('date')
    dateobj = datetime.strptime(date, '%Y-%m-%d')
    log, isCreated = Log.get_or_create(date=dateobj)
    if isCreated:
        flash(f"log for date {date} created")
    return redirect(url_for("main.view", log_id=log.id))

@main.route('/add_food_to_log/<int:log_id>', methods=['POST'])
def add_food_to_log(log_id):
    food_id = int(request.form.get('food-select'))
    print(food_id, type(food_id))
    food_select = Food.select().where(Food.id==food_id).get()
    food_select.logs.add(Log.select().where(Log.id==log_id))
        
    return redirect(url_for("main.view", log_id=log_id))

@main.route('/delete_food_from_log/<int:log_id>/<int:food_id>')
def delete_food_from_log(log_id, food_id):
    food_select = Food.select().where(Food.id==food_id).get()
    food_select.logs.remove(Log.select().where(Log.id==log_id))
    return redirect(url_for("main.view", log_id=log_id))