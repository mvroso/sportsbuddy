from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from website import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# PROXIMOS PASSOS
# CRIAR CLASSES EVENTO E INGRESSO
# INSTALAR A CLASSE FLASK BOOTSTRAP DO VIDEO TEMPLATES E VER SE FAZ ALGUMA DIFERENCA

# Class description
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    # Choices (Male = 1, Female = 2, Not applicable = 3)
    gender_id = db.Column(db.Integer, nullable=False, default=1)

    # user image hash
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    # foreign key = Role
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=1)

    # relationship = User | one to Many | Match
    matches = db.relationship('Match', backref='owner', lazy=True)

    '''
     ***** ALTERAR NO FUTURO QUANDO DECIDIRMOS SE VAMOS IMPLEMENTAR MENSAGENS (OU NAO) *****
    # relationship = User | one to Many | Message
    messages = db.relationship('User', backref='role', lazy=True)
    '''

    # generate a reset password token that expires in 10 minutes
    def get_reset_token(self, expires_sec=600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # verifies the reset password token and returns the user_id or None
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}', '{self.role.name}')"

# Helper table for Coach sports
sports = db.Table('sports',
    db.Column('coach_id', db.Integer, db.ForeignKey('coach.id'), primary_key=True),
    db.Column('sport_id', db.Integer, db.ForeignKey('sport.id'), primary_key=True)
    )

# User = parent
class Coach(User):
    __tablename__ = 'coach'

    # primary key from parent User
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # unique attributes to coach
    sports = db.relationship('Sport', secondary=sports, lazy='subquery',
        backref=db.backref('coach', lazy=True))

    # card hash
    card_file = db.Column(db.String(20), nullable=False, default='card.jpg')

    hourly_rate = db.Column(db.Integer, nullable=False, default=15)

    description = db.Column(db.Text, nullable=True)

    phone_number = db.Column(db.String(20), nullable=True)

    # Choices (Free = 1, Premium = 2)
    plan_id = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"Coach('{self.name}', '{self.sports}', '{self.hourly_rate}', '{self.plan_id}')"


# Class description
class Role(db.Model):
    __tablename__ = 'role'

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), unique=True, nullable=False)

    # relationship = Role | one to Many | User
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f"Role('{self.id}', '{self.name}')"


# Helper table for Match players
players = db.Table('players',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True)
    )


# Class description
class Match(db.Model):
    __tablename__ = 'match'

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    players_maxnumber = db.Column(db.Integer, nullable=False, default=2)

    # ***** MUDAR PARA UM PONTO GEOGRAFICO DEPOIS ?????? *****
    location = db.Column(db.String(50), nullable=False, default='Torino')

    # foreign key = Sport
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'), nullable=False)

    # foreign key = User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # foreign key = Time_Period
    time_period_id = db.Column(db.Integer, db.ForeignKey('timeperiod.id'), nullable=False)

    # relationship = User | Many to Many | Match
    players = db.relationship('User', secondary=players, lazy='subquery',
        backref=db.backref('match', lazy=True))

    def __repr__(self):
        return f"Match('{self.title}', '{self.date}', '{self.sport.name}')"



# Class description
class Timeperiod(db.Model):
    __tablename__ = 'timeperiod'

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), unique=True, nullable=False)

    # relationship = Role | one to Many | Match
    time_periods = db.relationship('Match', backref='timeperiod', lazy=True)

    def __repr__(self):
        return f"Time Period('{self.id}', '{self.name}')"

# Class description
class Sport(db.Model):
    __tablename__ = 'sport'

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), unique=True, nullable=False)

    # relationship = Sport | one to Many | Match
    matches = db.relationship('Match', backref='sport', lazy=True)

    def __repr__(self):
        return f"Sport('{self.name}')"



'''
 ***** ALTERAR NO FUTURO QUANDO DECIDIRMOS SE VAMOS IMPLEMENTAR MENSAGENS (OU NAO) *****
#Class description
class Message(db.Model):
    # primary key
    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # foreign key = User
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # foreign key = User
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Message('{self.content}', '{self.date_posted}')"

'''