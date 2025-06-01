import click
from datetime import datetime
from .helpers import display_table, validate_email, validate_phone
from .models import session, Student, Room, Manager, Booking, Complaint
from .menu import show_menu

@click.group()
def cli():
    """Hostel Management System CLI"""
    pass

@cli.command()
def menu():
    """Start interactive menu"""
    show_menu()

# Student commands
@cli.group()
def student():
    """Manage students"""
    pass

@student.command()
@click.option('--name', prompt=True, help="Student's full name")
@click.option('--email', prompt=True, help="Student's email")
@click.option('--phone', prompt=True, help="Student's phone number")
def add(name, email, phone):
    """Add a new student"""
    if not validate_email(email):
        click.echo("Invalid email format!")
        return
        
    if not validate_phone(phone):
        click.echo("Invalid phone number!")
        return
        
    student = Student(name=name, email=email, phone=phone)
    session.add(student)
    session.commit()
    click.echo(f"Student {name} added successfully!")

@student.command()
def list():
    """List all students"""
    students = session.query(Student).all()
    if not students:
        click.echo("No students found!")
        return
        
    data = [(s.id, s.name, s.email, s.phone) for s in students]
    headers = ["ID", "Name", "Email", "Phone"]
    display_table("Students", headers, data)

@student.command()
@click.argument('student_id', type=int)
def view(student_id):
    """View student details"""
    student = session.query(Student).get(student_id)
    if not student:
        click.echo(f"Student with ID {student_id} not found!")
        return
        
    click.echo(f"\nStudent Details (ID: {student.id})")
    click.echo(f"Name: {student.name}")
    click.echo(f"Email: {student.email}")
    click.echo(f"Phone: {student.phone}")
    click.echo(f"Registration Date: {student.registration_date}")
    
    if student.bookings:
        click.echo("\nBookings:")
        for booking in student.bookings:
            click.echo(f"- Room {booking.room.room_number} ({booking.status})")

@student.command()
@click.argument('student_id', type=int)
def delete(student_id):
    """Delete a student"""
    student = session.query(Student).get(student_id)
    if not student:
        click.echo(f"Student with ID {student_id} not found!")
        return
        
    session.delete(student)
    session.commit()
    click.echo(f"Student {student.name} deleted successfully!")

# Room commands (similar structure for other entities)
# ... [keep all your existing room, booking, manager, complaint commands]

# Initialize database command
@cli.command()
def initdb():
    """Initialize the database"""
    from .models import Base, engine
    Base.metadata.create_all(engine)
    
    # Add Kenyan sample data
    if not session.query(Student).first():
        kenyan_students = [
            Student(name="Wanjiku Mwangi", email="wanjiku@student.ku.ac.ke", phone="0712345678"),
            Student(name="Otieno Owino", email="owino@student.uonbi.ac.ke", phone="0723456789")
        ]
        
        kenyan_rooms = [
            Room(room_number="G12", capacity=4, price=15000),
            Room(room_number="T7", capacity=2, price=25000)
        ]
        
        kenyan_managers = [
            Manager(name="Kamau Githinji", email="k.githinji@uonhostels.com", phone="0701234567"),
            Manager(name="Nyambura Wairimu", email="n.wairimu@kuhostels.co.ke", phone="0712345678")
        ]
        
        session.add_all(kenyan_students + kenyan_rooms + kenyan_managers)
        session.commit()
    
    click.echo("Database initialized with Kenyan sample data!")

if __name__ == '__main__':
    cli()