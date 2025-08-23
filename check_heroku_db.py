#!/usr/bin/env python
"""
Script to check Heroku PostgreSQL database for superusers and tables
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Fgen_New.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection

def check_database():
    print("=== CHECKING HEROKU DATABASE ===\n")
    
    # Check superusers
    print("1. SUPERUSERS:")
    superusers = User.objects.filter(is_superuser=True)
    if superusers:
        for user in superusers:
            print(f"   ✓ {user.username} ({user.email}) - Staff: {user.is_staff}, Superuser: {user.is_superuser}")
    else:
        print("   ✗ No superusers found!")
    
    print(f"\n2. TOTAL USERS: {User.objects.count()}")
    
    # Check all users (first 5)
    print("\n3. FIRST 5 USERS:")
    users = User.objects.all()[:5]
    for user in users:
        print(f"   - {user.username} ({user.email}) - Staff: {user.is_staff}, Superuser: {user.is_superuser}")
    
    # Check database tables
    print("\n4. DATABASE TABLES:")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        if tables:
            for table in tables:
                print(f"   ✓ {table[0]}")
        else:
            print("   ✗ No tables found!")
    
    print(f"\n5. TOTAL TABLES: {len(tables)}")

if __name__ == "__main__":
    check_database()
