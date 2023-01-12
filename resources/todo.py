from flask import Blueprint, request, jsonify

from models.todoModel import todoModel

todo = Blueprint('todo', __name__, url_prefix="/todos")


# GET REQUEST
@todo.get("/")
def get_todos():
    try:
        todos = todoModel.query.all()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        'message': "Todo Get",
        'todos': [todo.serialize() for todo in todos]
    }), 200

# POST REQUEST


@todo.post("/")
def create_todo():
    _todo = request.json["_todo"]
    _duration = request.json["_duration"]

    todo = todoModel(todo=_todo, duration=_duration)

    todo.save_to_db()

    return jsonify({
        'message': "Todo Post",
        'todo': todo.serialize()
    }), 201

# DELETE REQUEST


@todo.delete("/<id>")
def delete_todo(id):
    todo = todoModel.query.filter_by(id=id).first()

    todo.delete_from_db()

    return jsonify({
        'message': "Todo Deleted",
    })

# PUT REQUEST


@todo.put("/")
def update_todo():
    id = request.args.get('id', '')
    duration = request.json.get('_duration', '')

    todo = todoModel.query.filter_by(id=id).first()

    todo.duration = duration

    todo.save_to_db()

    return jsonify({
        'message': "Todo updated",
        'todo': todo.serialize()
    })
