import sqlite3
import os

def get_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS customers (
                       customer_id UUID PRIMARY KEY,
                       email TEXT NOT NULL UNIQUE,
                       first_name TEXT,
                       last_name TEXT,
                       created_at TIMESTAMP
                       )
        """)
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS plans (
                       plan_id UUID PRIMARY KEY,
                       period_days INTEGER NOT NULL,
                       amount DECIMAL
                       )
                       """)
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS subscriptions (
                       subscription_id UUID PRIMARY KEY,
                       customer_id UUID FOREIGN KEY REFERENCES customers(customer_id),
                       start_date TIMESTAMP,
                       plan UUID FOREIGN KEY REFERENCES plans(plan_id),
                       invoice_periods INTEGER TIMESTAMP FOREIGN 
                       KEY REFERENCES invoices(invoice_periods)
                       )
                       """)
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS invoices (
                       invoice_id TEXT PRIMARY KEY,
                       customer_id UUID FOREIGN KEY REFERENCES customers(customer_id),
                       period_start TIMESTAMP,
                       period_end TIMESTAMP,
                       status TEXT,
                       line_items TEXT FOREIGN KEY REFERENCES line_items(LineItem)
                       )
                       """)
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS line_items (
                       line_item_id TEXT NOT NULL PRIMARY KEY,
                       description TEXT,
                       amount DECIMAL,
                       quantity INTEGER
                       )
                       """)