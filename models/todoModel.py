from db import db


class todoModel(db.Model):
    """ TODO MODEL SCHEMA """
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(255), nullable=False, unique=True)
    duration = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))

    def __init__(self, todo, duration, user_id):
        self.todo = todo
        self.duration = duration
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'todo': self.todo,
            'duration': self.duration,
            'user_id': self.user_id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
