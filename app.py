import os
from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

# Tasks

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html",
                           tasks=mongo.db.tasks.find())


@app.route('/add_task')
def add_task():
    return render_template('addtask.html',
                           categories=mongo.db.categories.find(), module=mongo.db.modules.find(), unit=mongo.db.units.find())


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks =  mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    all_modules = mongo.db.modules.find()
    all_units = mongo.db.units.find()
    return render_template('edittask.html', task=the_task,
                           categories=all_categories, modules=all_modules, units=all_units)


@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)},
    {
        'task_name': request.form.get('task_name'),
        'category_name': request.form.get('category_name'),
        'module_name': request.form.get('module_name'),
        'unit_name': request.form.get('unit_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))

# Courses

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
                           categories=mongo.db.categories.find())

@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))


@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')


# Modules

@app.route('/get_modules')
def get_modules():
    return render_template('modules.html',
                           modules=mongo.db.modules.find())

@app.route('/delete_module/<module_id>')
def delete_module(module_id):
    mongo.db.modules.remove({'_id': ObjectId(module_id)})
    return redirect(url_for('get_modules'))


@app.route('/edit_module/<module_id>')
def edit_module(module_id):
    return render_template('editmodule.html',
    module=mongo.db.modules.find_one({'_id': ObjectId(module_id)}))


@app.route('/update_module/<module_id>', methods=['POST'])
def module_category(module_id):
    mongo.db.modules.update(
        {'_id': ObjectId(module_id)},
        {'module_name': request.form.get('module_name')})
    return redirect(url_for('get_modules'))


@app.route('/insert_module', methods=['POST'])
def insert_module():
    module_doc = {'module_name': request.form.get('module_name')}
    mongo.db.modules.insert_one(module_doc)
    return redirect(url_for('get_modules'))


@app.route('/add_module')
def add_module():
    return render_template('addmodule.html')


# units

@app.route('/get_units')
def get_units():
    return render_template('units.html',
                           units=mongo.db.units.find())

@app.route('/delete_unit/<unit_id>')
def delete_unit(unit_id):
    mongo.db.units.remove({'_id': ObjectId(unit_id)})
    return redirect(url_for('get_units'))


@app.route('/edit_unit/<unit_id>')
def edit_unit(unit_id):
    return render_template('editunit.html',
    unit=mongo.db.units.find_one({'_id': ObjectId(unit_id)}))


@app.route('/update_unit/<unit_id>', methods=['POST'])
def update_unit(unit_id):
    mongo.db.units.update(
        {'_id': ObjectId(unit_id)},
        {'unit_name': request.form.get('unit_name')})
    return redirect(url_for('get_units'))


@app.route('/insert_unit', methods=['POST'])
def insert_unit():
    unit_doc = {'unit_name': request.form.get('unit_name')}
    mongo.db.units.insert_one(unit_doc)
    return redirect(url_for('get_units'))


@app.route('/add_unit')
def add_unit():
    return render_template('addunit.html')

# sound advice static html page

@app.route('/get_soundadvice')
def get_soundadvice():
    return render_template('soundadvice.html')

@app.route('/get_index')
def get_index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '127.0.0.1'),
            port=int(os.environ.get('PORT', '8080')),
            debug=True)