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
    publicity_check = db.Column(db.Boolean, unique=False, default=False)
    on_admin_check = db.Column(db.Boolean, unique=False, default=True)
    yes_ans = db.Column(db.Integer, default=0)
    no_ans = db.Column(db.Integer, default=0)
    user = db.relationship('User', backref=db.backref('survey_list', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Surveys {} {} {} {} {} {} {} {}>'.format(self.id, self.title, self.category, self.publicity_check, self.on_admin_check, self.yes_ans, self.no_ans, self.user_id)

    @staticmethod
    def add(title, category, publicity_check, on_admin_check, user):
        survey = Surveys(title=title, category=category, publicity_check=publicity_check, on_admin_check=on_admin_check, user=user)
        db.session.add(survey)
        db.session.commit()

    @staticmethod
    def delete(survey):
        db.session.delete(survey)
        db.session.commit()

    @staticmethod
    def show(survey):
        survey.publicity_check = True
        db.session.commit()

    @staticmethod
    def hide(survey):
        survey.publicity_check = False
        db.session.commit()

    @staticmethod
    def mark_as_checked(survey):
        survey.on_admin_check = False
        db.session.commit()

    @staticmethod
    def plus_yes(survey):
        survey.yes_ans += 1
        db.session.commit()

    @staticmethod
    def plus_no(survey):
        survey.no_ans += 1
        db.session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'on_admin_check': self.on_admin_check,
            'yes_ans': self.yes_ans,
            'no_ans': self.no_ans,
            'publicity_check': self.publicity_check,
            'user_id': self.user_id
        }
