from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import sessionmaker



Base = declarative_base()



#################### SQLAlchemy models ####################

class AdminTable(Base):
    __tablename__ = 'admin_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo = Column(LargeBinary)
    description = Column(String)
    symbol = Column(String)
    button_1 = Column(String)
    button_2 = Column(String)
    button_3 = Column(String)
    correct_button = Column(Integer)

class UserTable(Base):
    __tablename__ = 'user_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    username = Column(String)
    correct_button = Column(Integer)

#################### SQLAlchemy models ####################



#################### SQLAlchemy admin database ####################

class AddInfo(StatesGroup):
    new_post = State()
    photo = State()
    description = State()
    button_1 = State()
    button_2 = State()
    button_3 = State()
    symbol = State()
    edit_photo = State()
    edit_description = State()
    edit_button_1 = State()
    edit_button_2 = State()
    edit_button_3 = State()
    edit_symbol = State()

class SQLAlchemy_Admindb:
    def __init__(self, database_url='sqlite:///admin_db.db'):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_info(self, photo, description, symbol, button_1, button_2, button_3, correct_button):
        photo_binary = photo.encode() 
        new_entry = AdminTable(
            photo=photo_binary,
            description=description,
            symbol=symbol,
            button_1=button_1,
            button_2=button_2,
            button_3=button_3,
            correct_button=correct_button
        )
        session = self.Session()
        session.add(new_entry)
        session.commit()
        session.close()

    def get_info(self):
        session = self.Session()
        entry = session.query(AdminTable).order_by(AdminTable.id.desc()).first()
        session.close()
        if entry:
            return entry.photo, entry.description, entry.symbol, entry.button_1, entry.button_2, entry.button_3, entry.correct_button
        return None

    def update_info(self, column, value):
        session = self.Session()
        latest_entry = session.query(AdminTable).order_by(AdminTable.id.desc()).first()
        if latest_entry:
            if column == 'photo':
                value = value.encode()
            setattr(latest_entry, column, value)
            session.commit()
        session.close()

admin_db = SQLAlchemy_Admindb()

saved_post_data = None

def save_post_data(data):
    global saved_post_data
    saved_post_data = data

def get_saved_post_data():
    return admin_db.get_info()

#################### SQLAlchemy admin database ####################



#################### SQLAlchemy user database ####################

class SQLAlchemy_Userdb:
    def __init__(self, database_url='sqlite:///user_db.db'):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine, tables=[UserTable.__table__])
        self.Session = sessionmaker(bind=self.engine)
        
    def add_info(self, user_id, username, correct_button):
        session = self.Session()
        new_entry = UserTable(user_id=user_id, username=username, correct_button=correct_button)
        session.add(new_entry)
        session.commit()
        session.close()

    def get_info(self):
        session = self.Session()
        entry = session.query(UserTable).order_by(UserTable.id.desc()).first()
        session.close()
        if entry:
            return entry.user_id, entry.username, entry.correct_button
        return None

    def update_info(self, column, value):
        session = self.Session()
        latest_entry = session.query(UserTable).order_by(UserTable.id.desc()).first()
        if latest_entry:
            setattr(latest_entry, column, value)
            session.commit()
        session.close()

user_db = SQLAlchemy_Userdb()

#################### SQLAlchemy user database ####################