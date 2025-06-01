from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    registration_date = Column(Date, default=datetime.now)
    
    bookings = relationship("Booking", back_populates="student")
    complaints = relationship("Complaint", back_populates="student")
    
    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', email='{self.email}')>"

class Room(Base):
    __tablename__ = 'rooms'
    
    id = Column(Integer, primary_key=True)
    room_number = Column(String, unique=True)
    capacity = Column(Integer)
    current_occupancy = Column(Integer, default=0)
    price = Column(Integer)
    is_available = Column(Boolean, default=True)
    
    bookings = relationship("Booking", back_populates="room")
    
    def __repr__(self):
        return f"<Room(id={self.id}, number='{self.room_number}', available={self.is_available})>"

class Manager(Base):
    __tablename__ = 'managers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    
    complaints = relationship("Complaint", back_populates="manager")
    
    def __repr__(self):
        return f"<Manager(id={self.id}, name='{self.name}')>"

class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    booking_date = Column(Date, default=datetime.now)
    check_in_date = Column(Date)
    check_out_date = Column(Date)
    status = Column(String, default='confirmed')  # confirmed, cancelled, completed
    
    student = relationship("Student", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
    
    def __repr__(self):
        return f"<Booking(id={self.id}, student={self.student_id}, room={self.room_id})>"

class Complaint(Base):
    __tablename__ = 'complaints'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    manager_id = Column(Integer, ForeignKey('managers.id'))
    title = Column(String)
    description = Column(String)
    date = Column(Date, default=datetime.now)
    status = Column(String, default='open')  # open, in-progress, resolved
    
    student = relationship("Student", back_populates="complaints")
    manager = relationship("Manager", back_populates="complaints")
    
    def __repr__(self):
        return f"<Complaint(id={self.id}, title='{self.title}', status='{self.status}')>"

# Database connection
engine = create_engine('sqlite:///hostel.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()