from db import db


class todoModel(db.Model):
    """ TODO MODEL SCHEMA """
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(255), nullable=False, unique=True)
    duration = db.Column(db.String(255), nullable=False)

    def __init__(self, todo, duration):
        self.todo = todo
        self.duration = duration

    def serialize(self):
        return {
            'id': self.id,
            'todo': self.todo,
            'duration': self.duration
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
