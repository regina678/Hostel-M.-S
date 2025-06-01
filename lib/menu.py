import click
from datetime import datetime
from .models import session, Student, Room, Manager, Booking, Complaint
from .helpers import display_table, validate_email, validate_phone

def clear_screen():
    click.clear()

def show_menu():
    while True:
        clear_screen()
        click.echo("╔══════════════════════════════╗")
        click.echo("║  TACHBEL HOSTEL MANAGEMENT    ║")
        click.echo("╠══════════════════════════════╣")
        click.echo("║ 1. Student Management        ║")
        click.echo("║ 2. Room Management           ║")
        click.echo("║ 3. Booking Management        ║")
        click.echo("║ 4. Complaint Management      ║")
        click.echo("║ 5. Manager Management        ║")
        click.echo("║ 6. View Reports              ║")
        click.echo("║ 0. Exit                      ║")
        click.echo("╚══════════════════════════════╝")
        
        choice = click.prompt("Enter your choice", type=click.IntRange(0, 6))
        
        if choice == 0:
            break
        elif choice == 1:
            manage_students()
        elif choice == 2:
            manage_rooms()
        elif choice == 3:
            manage_bookings()
        elif choice == 4:
            manage_complaints()
        elif choice == 5:
            manage_managers()
        elif choice == 6:
            view_reports()

def manage_students():
    while True:
        clear_screen()
        click.echo("╔══════════════════════════════╗")
        click.echo("║      STUDENT MANAGEMENT      ║")
        click.echo("╠══════════════════════════════╣")
        click.echo("║ 1. Add New Student          ║")
        click.echo("║ 2. View All Students        ║")
        click.echo("║ 3. View Student Details     ║")
        click.echo("║ 4. Update Student           ║")
        click.echo("║ 5. Delete Student           ║")
        click.echo("║ 0. Back to Main Menu        ║")
        click.echo("╚══════════════════════════════╝")
        
        choice = click.prompt("Enter your choice", type=click.IntRange(0, 5))
        
        if choice == 0:
            break
        elif choice == 1:
            clear_screen()
            click.echo("╔══════════════════════════════╗")
            click.echo("║       ADD NEW STUDENT        ║")
            click.echo("╚══════════════════════════════╝")
            name = click.prompt("Full Name")
            email = click.prompt("Email")
            phone = click.prompt("Phone (07XXXXXXXX)")
            
            if not validate_phone(phone):
                click.echo("Invalid phone number! Must start with 07 and be 10 digits.")
                click.pause()
                continue
                
            if session.query(Student).filter_by(email=email).first():
                click.echo("Error: A student with this email already exists!")
                click.pause()
                continue
                
            student = Student(name=name, email=email, phone=phone)
            session.add(student)
            session.commit()
            click.echo(f"\nStudent {name} added successfully!")
            click.pause()
            
        elif choice == 2:
            clear_screen()
            students = session.query(Student).all()
            if students:
                data = [(s.id, s.name, s.email, s.phone) for s in students]
                display_table("ALL STUDENTS", ["ID", "Name", "Email", "Phone"], data)
            else:
                click.echo("No students found!")
            click.pause()
            
        elif choice == 3:
            clear_screen()
            student_id = click.prompt("Enter Student ID to view", type=int)
            student = session.query(Student).get(student_id)
            if student:
                click.echo(f"\nStudent Details (ID: {student.id})")
                click.echo(f"Name: {student.name}")
                click.echo(f"Email: {student.email}")
                click.echo(f"Phone: {student.phone}")
                click.echo(f"Registration Date: {student.registration_date}")
                
                if student.bookings:
                    click.echo("\nCurrent Bookings:")
                    for booking in student.bookings:
                        room = session.query(Room).get(booking.room_id)
                        click.echo(f"- Room {room.room_number if room else 'N/A'} ({booking.status})")
            else:
                click.echo(f"Student with ID {student_id} not found!")
            click.pause()
            
        elif choice == 4:
            clear_screen()
            student_id = click.prompt("Enter Student ID to update", type=int)
            student = session.query(Student).get(student_id)
            if student:
                click.echo(f"\nCurrent Details for {student.name}:")
                click.echo(f"1. Name: {student.name}")
                click.echo(f"2. Email: {student.email}")
                click.echo(f"3. Phone: {student.phone}")
                
                field = click.prompt("\nEnter field number to update (1-3)", type=click.IntRange(1, 3))
                if field == 1:
                    student.name = click.prompt("New name", default=student.name)
                elif field == 2:
                    new_email = click.prompt("New email", default=student.email)
                    if validate_email(new_email):
                        student.email = new_email
                    else:
                        click.echo("Invalid email format!")
                elif field == 3:
                    new_phone = click.prompt("New phone", default=student.phone)
                    if validate_phone(new_phone):
                        student.phone = new_phone
                    else:
                        click.echo("Invalid phone number!")
                
                session.commit()
                click.echo("Student updated successfully!")
            else:
                click.echo(f"Student with ID {student_id} not found!")
            click.pause()
            
        elif choice == 5:
            clear_screen()
            student_id = click.prompt("Enter Student ID to delete", type=int)
            student = session.query(Student).get(student_id)
            if student:
                if click.confirm(f"Are you sure you want to delete {student.name}?"):
                    session.delete(student)
                    session.commit()
                    click.echo("Student deleted successfully!")
            else:
                click.echo(f"Student with ID {student_id} not found!")
            click.pause()

def manage_rooms():
    while True:
        clear_screen()
        click.echo("╔══════════════════════════════╗")
        click.echo("║       ROOM MANAGEMENT        ║")
        click.echo("╠══════════════════════════════╣")
        click.echo("║ 1. Add New Room             ║")
        click.echo("║ 2. View All Rooms           ║")
        click.echo("║ 3. View Room Details        ║")
        click.echo("║ 4. Update Room              ║")
        click.echo("║ 5. Delete Room              ║")
        click.echo("║ 0. Back to Main Menu        ║")
        click.echo("╚══════════════════════════════╝")
        
        choice = click.prompt("Enter your choice", type=click.IntRange(0, 5))
        
        if choice == 0:
            break
        elif choice == 1:
            clear_screen()
            click.echo("╔══════════════════════════════╗")
            click.echo("║        ADD NEW ROOM          ║")
            click.echo("╚══════════════════════════════╝")
            number = click.prompt("Room Number")
            capacity = click.prompt("Capacity", type=int)
            price = click.prompt("Price per semester (KES)", type=int)
            
            if session.query(Room).filter_by(room_number=number).first():
                click.echo("Error: A room with this number already exists!")
                click.pause()
                continue
                
            room = Room(room_number=number, capacity=capacity, price=price)
            session.add(room)
            session.commit()
            click.echo(f"\nRoom {number} added successfully!")
            click.pause()
            
        elif choice == 2:
            clear_screen()
            rooms = session.query(Room).all()
            if rooms:
                data = [(r.id, r.room_number, r.capacity, r.current_occupancy, 
                        f"KES {r.price}", "Yes" if r.is_available else "No") 
                       for r in rooms]
                display_table("ALL ROOMS", ["ID", "Room No", "Capacity", "Occupancy", "Price", "Available"], data)
            else:
                click.echo("No rooms found!")
            click.pause()
            
        elif choice == 3:
            clear_screen()
            room_id = click.prompt("Enter Room ID to view", type=int)
            room = session.query(Room).get(room_id)
            if room:
                click.echo(f"\nRoom Details (ID: {room.id})")
                click.echo(f"Room Number: {room.room_number}")
                click.echo(f"Capacity: {room.capacity}")
                click.echo(f"Current Occupancy: {room.current_occupancy}")
                click.echo(f"Price: KES {room.price}")
                click.echo(f"Available: {'Yes' if room.is_available else 'No'}")
                
                if room.bookings:
                    click.echo("\nCurrent Bookings:")
                    for booking in room.bookings:
                        student = session.query(Student).get(booking.student_id)
                        click.echo(f"- Student: {student.name if student else 'N/A'} ({booking.status})")
            else:
                click.echo(f"Room with ID {room_id} not found!")
            click.pause()
            
        elif choice == 4:
            clear_screen()
            room_id = click.prompt("Enter Room ID to update", type=int)
            room = session.query(Room).get(room_id)
            if room:
                click.echo(f"\nCurrent Details for Room {room.room_number}:")
                click.echo(f"1. Room Number: {room.room_number}")
                click.echo(f"2. Capacity: {room.capacity}")
                click.echo(f"3. Price: KES {room.price}")
                
                field = click.prompt("\nEnter field number to update (1-3)", type=click.IntRange(1, 3))
                if field == 1:
                    new_number = click.prompt("New room number", default=room.room_number)
                    if not session.query(Room).filter_by(room_number=new_number).first():
                        room.room_number = new_number
                    else:
                        click.echo("Error: Room number already exists!")
                elif field == 2:
                    room.capacity = click.prompt("New capacity", type=int, default=room.capacity)
                elif field == 3:
                    room.price = click.prompt("New price (KES)", type=int, default=room.price)
                
                session.commit()
                click.echo("Room updated successfully!")
            else:
                click.echo(f"Room with ID {room_id} not found!")
            click.pause()
            
        elif choice == 5:
            clear_screen()
            room_id = click.prompt("Enter Room ID to delete", type=int)
            room = session.query(Room).get(room_id)
            if room:
                if click.confirm(f"Are you sure you want to delete Room {room.room_number}?"):
                    session.delete(room)
                    session.commit()
                    click.echo("Room deleted successfully!")
            else:
                click.echo(f"Room with ID {room_id} not found!")
            click.pause()

def manage_bookings():
    while True:
        clear_screen()
        click.echo("╔══════════════════════════════╗")
        click.echo("║      BOOKING MANAGEMENT      ║")
        click.echo("╠══════════════════════════════╣")
        click.echo("║ 1. Create New Booking       ║")
        click.echo("║ 2. View All Bookings        ║")
        click.echo("║ 3. Cancel Booking           ║")
        click.echo("║ 0. Back to Main Menu        ║")
        click.echo("╚══════════════════════════════╝")
        
        choice = click.prompt("Enter your choice", type=click.IntRange(0, 3))
        
        if choice == 0:
            break
        elif choice == 1:
            clear_screen()
            click.echo("╔══════════════════════════════╗")
            click.echo("║       CREATE BOOKING         ║")
            click.echo("╚══════════════════════════════╝")
            
            # List students
            students = session.query(Student).all()
            if not students:
                click.echo("No students available!")
                click.pause()
                continue
                
            display_table("STUDENTS", ["ID", "Name"], [(s.id, s.name) for s in students])
            
            # List available rooms
            rooms = session.query(Room).filter(Room.is_available == True).all()
            if not rooms:
                click.echo("No available rooms!")
                click.pause()
                continue
                
            display_table("AVAILABLE ROOMS", ["ID", "Room No", "Price (KES)"], 
                         [(r.id, r.room_number, r.price) for r in rooms])
            
            student_id = click.prompt("Enter Student ID", type=int)
            room_id = click.prompt("Enter Room ID", type=int)
            check_in = click.prompt("Check-in date (YYYY-MM-DD)")
            check_out = click.prompt("Check-out date (YYYY-MM-DD)")
            
            try:
                booking = Booking(
                    student_id=student_id,
                    room_id=room_id,
                    check_in_date=datetime.strptime(check_in, "%Y-%m-%d").date(),
                    check_out_date=datetime.strptime(check_out, "%Y-%m-%d").date(),
                    status='confirmed'
                )
                
                room = session.query(Room).get(room_id)
                room.current_occupancy += 1
                if room.current_occupancy >= room.capacity:
                    room.is_available = False
                
                session.add(booking)
                session.commit()
                click.echo("Booking created successfully!")
            except Exception as e:
                session.rollback()
                click.echo(f"Error creating booking: {str(e)}")
            
            click.pause()
            
        elif choice == 2:
            clear_screen()
            bookings = session.query(Booking).all()
            if bookings:
                data = []
                for booking in bookings:
                    student = session.query(Student).get(booking.student_id)
                    room = session.query(Room).get(booking.room_id)
                    data.append((
                        booking.id,
                        student.name if student else "N/A",
                        room.room_number if room else "N/A",
                        booking.check_in_date,
                        booking.check_out_date,
                        booking.status
                    ))
                display_table("ALL BOOKINGS", 
                             ["ID", "Student", "Room", "Check-in", "Check-out", "Status"], 
                             data)
            else:
                click.echo("No bookings found!")
            click.pause()
            
        elif choice == 3:
            clear_screen()
            booking_id = click.prompt("Enter Booking ID to cancel", type=int)
            booking = session.query(Booking).get(booking_id)
            if booking:
                if booking.status == 'cancelled':
                    click.echo("This booking is already cancelled!")
                else:
                    if click.confirm("Are you sure you want to cancel this booking?"):
                        booking.status = 'cancelled'
                        room = session.query(Room).get(booking.room_id)
                        if room:
                            room.current_occupancy -= 1
                            if not room.is_available:
                                room.is_available = True
                        session.commit()
                        click.echo("Booking cancelled successfully!")
            else:
                click.echo(f"Booking with ID {booking_id} not found!")
            click.pause()

def manage_complaints():
    while True:
        clear_screen()
        click.echo("╔══════════════════════════════╗")
        click.echo("║     COMPLAINT MANAGEMENT     ║")
        click.echo("╠══════════════════════════════╣")
        click.echo("║ 1. File New Complaint       ║")
        click.echo("║ 2. View All Complaints      ║")
        click.echo("║ 3. Update Complaint Status  ║")
        click.echo("║ 0. Back to Main Menu        ║")
        click.echo("╚══════════════════════════════╝")
        
        choice = click.prompt("Enter your choice", type=click.IntRange(0, 3))
        
        if choice == 0:
            break
        elif choice == 1:
            clear_screen()
            click.echo("╔══════════════════════════════╗")
            click.echo("║      FILE NEW COMPLAINT      ║")
            click.echo("╚══════════════════════════════╝")
            
            # List students
            students = session.query(Student).all()
            if not students:
                click.echo("No students available!")
                click.pause()
                continue
                
            display_table("STUDENTS", ["ID", "Name"], [(s.id, s.name) for s in students])
            
            # List managers
            managers = session.query(Manager).all()
            if not managers:
                click.echo("No managers available!")
                click.pause()
                continue
                
            display_table("MANAGERS", ["ID", "Name"], [(m.id, m.name) for m in managers])
            
            student_id = click.prompt("Enter Student ID", type=int)
            manager_id = click.prompt("Enter Manager ID", type=int)
            title = click.prompt("Complaint Title")
            description = click.prompt("Complaint Description")
            
            try:
                complaint = Complaint(
                    student_id=student_id,
                    manager_id=manager_id,
                    title=title,
                    description=description,
                    status='open'
                )
                
                session.add(complaint)
                session.commit()
                click.echo("Complaint filed successfully!")
            except Exception as e:
                session.rollback()
                click.echo(f"Error filing complaint: {str(e)}")
            
            click.pause()
            
        elif choice == 2:
            clear_screen()
            complaints = session.query(Complaint).all()
            if complaints:
                data = []
                for complaint in complaints:
                    student = session.query(Student).get(complaint.student_id)
                    manager = session.query(Manager).get(complaint.manager_id)
                    data.append((
                        complaint.id,
                        student.name if student else "N/A",
                        manager.name if manager else "N/A",
                        complaint.title,
                        complaint.status,
                        complaint.date
                    ))
                display_table("ALL COMPLAINTS",
                            ["ID", "Student", "Manager", "Title", "Status", "Date"],
                            data)
            else:
                click.echo("No complaints found!")
            click.pause()
            
        elif choice == 3:
            clear_screen()
            complaint_id = click.prompt("Enter Complaint ID to update", type=int)
            complaint = session.query(Complaint).get(complaint_id)
            if complaint:
                click.echo(f"\nCurrent Status: {complaint.status}")
                new_status = click.prompt("New status (open/in-progress/resolved)", 
                                        type=click.Choice(['open', 'in-progress', 'resolved']),
                                        default=complaint.status)
                complaint.status = new_status
                session.commit()
                click.echo("Complaint status updated successfully!")
            else:
                click.echo(f"Complaint with ID {complaint_id} not found!")
            click.pause()

def manage_managers():
    while True:
        clear_screen()
        click.echo("╔══════════════════════════════╗")
        click.echo("║      MANAGER MANAGEMENT      ║")
        click.echo("╠══════════════════════════════╣")
        click.echo("║ 1. Add New Manager          ║")
        click.echo("║ 2. View All Managers        ║")
        click.echo("║ 3. Update Manager           ║")
        click.echo("║ 4. Delete Manager           ║")
        click.echo("║ 0. Back to Main Menu        ║")
        click.echo("╚══════════════════════════════╝")
        
        choice = click.prompt("Enter your choice", type=click.IntRange(0, 4))
        
        if choice == 0:
            break
        elif choice == 1:
            clear_screen()
            click.echo("╔══════════════════════════════╗")
            click.echo("║       ADD NEW MANAGER        ║")
            click.echo("╚══════════════════════════════╝")
            name = click.prompt("Full Name")
            email = click.prompt("Email")
            phone = click.prompt("Phone (07XXXXXXXX)")
            
            if not validate_phone(phone):
                click.echo("Invalid  phone number! Must start with 07 and be 10 digits.")
                click.pause()
                continue
                
            if session.query(Manager).filter_by(email=email).first():
                click.echo("Error: A manager with this email already exists!")
                click.pause()
                continue
                
            manager = Manager(name=name, email=email, phone=phone)
            session.add(manager)
            session.commit()
            click.echo(f"\nManager {name} added successfully!")
            click.pause()
            
        elif choice == 2:
            clear_screen()
            managers = session.query(Manager).all()
            if managers:
                data = [(m.id, m.name, m.email, m.phone) for m in managers]
                display_table("ALL MANAGERS", ["ID", "Name", "Email", "Phone"], data)
            else:
                click.echo("No managers found!")
            click.pause()
            
        elif choice == 3:
            clear_screen()
            manager_id = click.prompt("Enter Manager ID to update", type=int)
            manager = session.query(Manager).get(manager_id)
            if manager:
                click.echo(f"\nCurrent Details for {manager.name}:")
                click.echo(f"1. Name: {manager.name}")
                click.echo(f"2. Email: {manager.email}")
                click.echo(f"3. Phone: {manager.phone}")
                
                field = click.prompt("\nEnter field number to update (1-3)", type=click.IntRange(1, 3))
                if field == 1:
                    manager.name = click.prompt("New name", default=manager.name)
                elif field == 2:
                    new_email = click.prompt("New email", default=manager.email)
                    if validate_email(new_email):
                        manager.email = new_email
                    else:
                        click.echo("Invalid email format!")
                elif field == 3:
                    new_phone = click.prompt("New phone", default=manager.phone)
                    if validate_phone(new_phone):
                        manager.phone = new_phone
                    else:
                        click.echo("Invalid phone number!")
                
                session.commit()
                click.echo("Manager updated successfully!")
            else:
                click.echo(f"Manager with ID {manager_id} not found!")
            click.pause()
            
        elif choice == 4:
            clear_screen()
            manager_id = click.prompt("Enter Manager ID to delete", type=int)
            manager = session.query(Manager).get(manager_id)
            if manager:
                if click.confirm(f"Are you sure you want to delete {manager.name}?"):
                    session.delete(manager)
                    session.commit()
                    click.echo("Manager deleted successfully!")
            else:
                click.echo(f"Manager with ID {manager_id} not found!")
            click.pause()

def view_reports():
    while True:
        clear_screen()
        click.echo("╔══════════════════════════════╗")
        click.echo("║          REPORTS             ║")
        click.echo("╠══════════════════════════════╣")
        click.echo("║ 1. Room Occupancy           ║")
        click.echo("║ 2. Complaint Status         ║")
        click.echo("║ 3. Financial Summary        ║")
        click.echo("║ 0. Back to Main Menu        ║")
        click.echo("╚══════════════════════════════╝")
        
        choice = click.prompt("Enter your choice", type=click.IntRange(0, 3))
        
        if choice == 0:
            break
        elif choice == 1:
            clear_screen()
            rooms = session.query(Room).all()
            if rooms:
                data = []
                for room in rooms:
                    occupancy_percent = (room.current_occupancy / room.capacity) * 100
                    data.append((
                        room.room_number,
                        room.capacity,
                        room.current_occupancy,
                        f"{occupancy_percent:.1f}%",
                        f"KES {room.price}"
                    ))
                display_table("ROOM OCCUPANCY REPORT", 
                            ["Room No", "Capacity", "Occupied", "Occupancy %", "Price"], 
                            data)
            else:
                click.echo("No rooms found!")
            click.pause()
            
        elif choice == 2:
            clear_screen()
            complaints = session.query(Complaint).all()
            if complaints:
                status_counts = {'open': 0, 'in-progress': 0, 'resolved': 0}
                for complaint in complaints:
                    status_counts[complaint.status] += 1
                
                click.echo("\nCOMPLAINT STATUS SUMMARY:")
                click.echo(f"Open: {status_counts['open']}")
                click.echo(f"In Progress: {status_counts['in-progress']}")
                click.echo(f"Resolved: {status_counts['resolved']}")
                click.echo(f"Total: {sum(status_counts.values())}")
                
                # Detailed view
                if click.confirm("\nShow detailed complaint list?"):
                    data = []
                    for complaint in complaints:
                        student = session.query(Student).get(complaint.student_id)
                        manager = session.query(Manager).get(complaint.manager_id)
                        data.append((
                            complaint.id,
                            student.name if student else "N/A",
                            manager.name if manager else "N/A",
                            complaint.title,
                            complaint.status,
                            complaint.date
                        ))
                    display_table("ALL COMPLAINTS",
                                ["ID", "Student", "Manager", "Title", "Status", "Date"],
                                data)
            else:
                click.echo("No complaints found!")
            click.pause()
            
        elif choice == 3:
            clear_screen()
            rooms = session.query(Room).all()
            total_revenue = sum(room.price * room.current_occupancy for room in rooms)
            total_capacity = sum(room.capacity for room in rooms)
            total_occupied = sum(room.current_occupancy for room in rooms)
            
            click.echo("\nFINANCIAL SUMMARY")
            click.echo(f"Total Rooms: {len(rooms)}")
            click.echo(f"Total Capacity: {total_capacity}")
            click.echo(f"Total Occupied: {total_occupied}")
            click.echo(f"Occupancy Rate: {(total_occupied/total_capacity)*100:.1f}%")
            click.echo(f"Estimated Revenue: KES {total_revenue}")
            
            if rooms:
                data = [(r.room_number, r.capacity, r.current_occupancy, 
                        f"KES {r.price}", f"KES {r.price * r.current_occupancy}") 
                       for r in rooms]
                display_table("ROOM REVENUE DETAILS",
                            ["Room No", "Capacity", "Occupied", "Price", "Revenue"],
                            data)
            click.pause()

if __name__ == '__main__':
    show_menu()