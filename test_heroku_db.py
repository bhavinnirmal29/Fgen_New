#!/usr/bin/env python
"""
Script to test Heroku PostgreSQL database connection directly
"""
import os
import psycopg2
from urllib.parse import urlparse

# Heroku DATABASE_URL from config
DATABASE_URL = "postgres://uc8bdr2fg33rn6:p376745114295f79b372a7a631410db0c9e81814862e9b59f654a0fd9695a2152@c9mq4861d16jlm.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dfe673gjjcluri"

def test_database_connection():
    print("=== TESTING HEROKU DATABASE CONNECTION ===\n")
    
    try:
        # Parse the DATABASE_URL
        url = urlparse(DATABASE_URL)
        
        print(f"Database Host: {url.hostname}")
        print(f"Database Port: {url.port}")
        print(f"Database Name: {url.path[1:]}")
        print(f"Database User: {url.username}")
        print(f"Password: {'*' * len(url.password) if url.password else 'None'}")
        
        # Test connection
        print("\nAttempting to connect...")
        conn = psycopg2.connect(DATABASE_URL)
        
        print("✓ Successfully connected to Heroku database!")
        
        # Get database info
        cursor = conn.cursor()
        
        # Check PostgreSQL version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"\nPostgreSQL Version: {version[0]}")
        
        # Check current database
        cursor.execute("SELECT current_database();")
        current_db = cursor.fetchone()
        print(f"Current Database: {current_db[0]}")
        
        # Check tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print(f"\nTables found: {len(tables)}")
        if tables:
            print("First 10 tables:")
            for i, table in enumerate(tables[:10]):
                print(f"  {i+1}. {table[0]}")
            if len(tables) > 10:
                print(f"  ... and {len(tables) - 10} more")
        
        # Check if auth_user table exists and has data
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_name = 'auth_user'
        """)
        auth_user_exists = cursor.fetchone()[0] > 0
        
        if auth_user_exists:
            cursor.execute("SELECT COUNT(*) FROM auth_user")
            user_count = cursor.fetchone()[0]
            print(f"\nAuth User table exists with {user_count} users")
            
            # Check for superusers
            cursor.execute("SELECT username, email, is_superuser FROM auth_user WHERE is_superuser = true")
            superusers = cursor.fetchall()
            if superusers:
                print("Superusers found:")
                for user in superusers:
                    print(f"  - {user[0]} ({user[1]}) - Superuser: {user[2]}")
            else:
                print("No superusers found")
        else:
            print("\nAuth User table does not exist")
        
        cursor.close()
        conn.close()
        print("\n✓ Database connection test completed successfully!")
        
    except psycopg2.Error as e:
        print(f"✗ Database connection failed: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    test_database_connection()
