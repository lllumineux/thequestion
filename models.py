from dbase import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.username)

    @staticmethod
    def add(username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()


class Surveys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    category = db.Column(db.String(80), unique=False, nullable=False)
    public = db.Column(db.Boolean, unique=False, default=False)
    user = db.relationship('User', backref=db.backref('survey_list', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Surveys {} {} {} {} {}>'.format(self.id, self.title, self.category, self.public, self.user_id)

    @staticmethod
    def add(title, category, user):
        survey = Surveys(title=title, category=category, user=user)
        db.session.add(survey)
        db.session.commit()

    @staticmethod
    def delete(survey):
        db.session.delete(survey)
        db.session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'user_id': self.user_id
        }
