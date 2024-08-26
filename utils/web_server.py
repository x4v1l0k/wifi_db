#!/bin/python3
''' Utils to Web Viewer '''
# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, render_template_string
import pandas as pd

# HTML Template with Bootstrap for rendering tables
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Wifi_db Viewer</title>
    <style>
        .tab-pane {
            overflow: scroll;
        }

        .table tbody tr.highlight td {
            background-color: lightblue;
        }
    </style>
</head>
<body>
<div class="container-fluid">
    <h1 class="mt-4 mb-4">Wifi_db Viewer</h1>
    <ul class="nav nav-tabs" id="tab" role="tablist">
        {% for table in tables %}
        <li class="nav-item" role="presentation">
            <button class="nav-link {% if loop.first %}active{% endif %}" id="{{ table }}-tab" data-bs-toggle="tab" data-bs-target="#{{ table }}" type="button" role="tab" aria-controls="{{ table }}" aria-selected="true">{{ table }}</button>
        </li>
        {% endfor %}
    </ul>
    <div class="tab-content mt-3" id="tableContent">
        {% for table, data in table_data.items() %}
        <div class="tab-pane fade {% if loop.first %}show active{% endif %}" id="{{ table }}" role="tabpanel" aria-labelledby="{{ table }}-tab">
            <input class="form-control mb-3" id="searchInput{{ loop.index }}" type="text" placeholder="Search in {{ table }}">
            <table class="table table-bordered table-hover">
                <thead class="table-light">
                    <tr>
                        {% for column in data.columns %}
                        <th>{{ column }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody id="tableBody{{ loop.index }}">
                    {% for row in data.itertuples(index=False) %}
                    <tr>
                        {% for value in row %}
                        <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endfor %}
    </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        {% for table in tables %}
        document.getElementById('searchInput{{ loop.index }}').addEventListener('keyup', function() {
            var value = this.value.toLowerCase();
            var rows = document.querySelectorAll("#tableBody{{ loop.index }} tr");
            rows.forEach(function(row) {
                row.style.display = row.innerText.toLowerCase().includes(value) ? "" : "none";
            });
        });
        {% endfor %}
        const rows = document.querySelectorAll('tbody tr');

        rows.forEach(function(row) {
            row.addEventListener('click', function() {
                rows.forEach(function(r) {
                    r.classList.remove('highlight');
                });
                this.classList.add('highlight');
            });
        });
    });
</script>
</body>
</html>
"""

def start(db_path, host, port):
    app = Flask(__name__)

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
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            table_data[table] = df

        conn.close()
        return render_template_string(HTML_TEMPLATE, tables=tables, table_data=table_data)

    app.run(host=host, port=port)