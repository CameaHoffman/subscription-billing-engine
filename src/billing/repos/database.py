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
                       customer_id TEXT PRIMARY KEY,
                       email TEXT NOT NULL UNIQUE,
                       first_name TEXT,
                       last_name TEXT,
                       created_at TIMESTAMP
                       )
        """)
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS plans (
                       plan_id TEXT PRIMARY KEY,
                       plan_name TEXT,
                       period_days INTEGER NOT NULL,
                       amount DECIMAL
                       )
                       """)
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS subscriptions (
                       subscription_id TEXT PRIMARY KEY,
                       customer_id TEXT NOT NULL,
                       start_date TIMESTAMP,
                       plan_id TEXT NOT NULL,
                       FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                       FOREIGN KEY (plan_id) REFERENCES plans(plan_id)
                       )
                       """)
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS invoices (
                       invoice_id TEXT PRIMARY KEY,
                       customer_id TEXT NOT NULL,
                       period_start TIMESTAMP,
                       period_end TIMESTAMP,
                       status TEXT,
                       FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                       """)
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS line_items (
                       line_item_id TEXT NOT NULL PRIMARY KEY,
                       invoice_id TEXT,
                       description TEXT,
                       amount DECIMAL,
                       quantity INTEGER,
                       FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id)
                       )
                       """)