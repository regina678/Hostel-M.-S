from tabulate import tabulate
import re

def display_table(title, headers, data):
    """Display tabular data"""
    print(f"\n{title}")
    print(tabulate(data, headers=headers, tablefmt="grid"))

def validate_email(email):
    """Validate email including Kenyan domains"""
    pattern = r'^[\w\.-]+@([\w-]+\.)+(ac\.ke|com|org|co\.ke)$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate Kenyan phone numbers (07XXXXXXXX)"""
    pattern = r'^(07\d{8})$'
    return re.match(pattern, phone) is not None