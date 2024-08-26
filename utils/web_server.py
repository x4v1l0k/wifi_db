#!/bin/python3
''' Utils to Web Viewer '''
# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, render_template
import pandas as pd
from os import path

def start(db_path, host, port):
    template_dir = path.join(path.dirname(path.abspath(__file__)), '..', 'templates')
    app = Flask(__name__, template_folder=template_dir)

    @app.route('/')
    def index():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]

        # Retrieve table data
        table_data = {}
        for table in tables:
            if table.isidentifier():
                df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
                table_data[table] = df

        conn.close()
        return render_template('index.html', tables=tables, table_data=table_data)

    app.run(host=host, port=port)