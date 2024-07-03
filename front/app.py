from flask import Flask, request, render_template, redirect, url_for, send_file
import os
import pandas as pd
import sys
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'back', 'app')))

from manager.controll import ScheduleController

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            # Geração da grade horária
            controller = ScheduleController(file_path)
            csv_file = controller.gerar_grade()
            return redirect('/view')
    return render_template('index.html')

@app.route('/view', methods=['GET'])
def view():
    # csv_file = 'grade_horaria.csv'
    csv_file = '../back/src/grade_horaria.csv'
    tables = []
    current_table = None
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                if row[0].startswith('Tabela para'):
                    if current_table is not None:
                        tables.append(current_table)
                    current_table = {'title': row[0], 'headers': next(reader, []), 'rows': []}
                elif current_table is not None:
                    if len(row) == len(current_table['headers']):
                        current_table['rows'].append(row)
        if current_table is not None:
            tables.append(current_table)
    return render_template('table.html', tables=tables)



if __name__ == '__main__':
    app.run(port=5001,debug=True)