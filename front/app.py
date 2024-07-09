# from flask import Flask, request, render_template, redirect, url_for, send_file
import os
# import pandas as pd
import csv

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'back', 'app')))

from manager.controll import ScheduleController
import utils.files as fl
import utils.settings as st

from flask import Flask, render_template, request, redirect
# from back.src.manager.controll import ScheduleController

app = Flask(__name__)

if not os.path.exists('./front/uploads'):
    os.makedirs('./front/uploads')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # num_turmas = int(request.form['num_turmas'])
        # num_materias = int(request.form['num_materias'])

        # print('Numero de turmas:   ', num_turmas)
        # print('Numero de materias:   ', num_materias)

        # materias_input = request.form['materias'].strip().split('\n')
        # materias = []
        # carga_horaria = {}
        # for mat in materias_input:
        #     parts = mat.split()
        #     materias.append(parts[0])
        #     carga_horaria[parts[0]] = int(parts[1])

        # num_professores = int(request.form['num_professores'])

        # professores_input = request.form['professores'].strip().split('\n')
        # professores = {}
        # carga_professor = {}
        # for prof in professores_input:
        #     print("valro em professores_inpu: ", prof)

        # for prof in professores_input:
        #     parts = prof.split()
        #     print("partes: ", parts)
        #     professores[parts[1]] = parts[0]
        #     carga_professor[parts[0]] = int(parts[2])
        #     print("valores na procaria do array: ", parts[0], " ", parts[1], " ", parts[2])

        # for line in carga_professor:
        #     print("carga horaria do professor: ", line)

        # disponibilidade_input = request.form['disponibilidade'].strip().split('\n')
        # disponibilidade = {}
        # current_prof = None
        # for line in disponibilidade_input:
        #     print("disponibilidade vamos ver: ",line)

        # for line in professores:
        #     print("nome do professor: ", line)

        # for line in materias:
        #     print("nome da materia: ", line)
        # # index = 0
        # for line in range(num_professores):
        #         # if line%2 == 0:
        #     disponibilidade[disponibilidade_input[index].strip()].extend([int(x) for x in disponibilidade_input[index+1].split()])
        #     # if line.startswith('Prof'):
        #     #     current_prof = line
        #     #     disponibilidade[current_prof] = []
        #     # else:
        #             # index = index + 2

        # turmas = [f'Turma {i+1}' for i in range(num_turmas)]

        num_turmas1 = int(request.form['num_turmas'])
        num_materias1 = int(request.form['num_materias'])
        materias1 = request.form['materias'].strip().split('\n')
        num_professores1 = int(request.form['num_professores'])
        professores1 = request.form['professores'].strip().split('\n')
        disponibilidade1 = request.form['disponibilidade'].strip().split('\n')

        with open(st.ROOT_UPLOADED, 'w') as f:
            f.write(f"{num_turmas1}\n")
            f.write(f"{num_materias1}\n")
            for materia in materias1:
                f.write(f"{materia}\n")
            f.write(f"{num_professores1}\n")
            for professor in professores1:
                f.write(f"{professor}\n")
            for disponibilidade_prof in disponibilidade1:
                f.write(f"{disponibilidade_prof}\n")

        materias, carga_horaria, professores, carga_professor, disponibilidade, turmas = fl.ler_arquivo_entrada(st.ROOT_UPLOADED)
        schedule_controller = ScheduleController(materias, carga_horaria, professores, carga_professor, disponibilidade, turmas)

        # materias, carga_horaria, professores, carga_professores, disponibilidade, turmas

        # resultado = schedule_controller.create_schedule(
        #     num_turmas=num_turmas,
        #     num_materias=num_materias,
        #     materias=materias,
        #     carga_horaria=carga_horaria,
        #     num_professores=num_professores,
        #     professores=professores,
        #     carga_professor=carga_professor,
        #     disponibilidade=disponibilidade
        # )

        # Salvar o resultado para ser exibido na tabela
        return redirect('/view')
    return render_template('table.html')

@app.route('/view', methods=['GET'])
def view():
    csv_file = './back/src/grade_horaria.csv'
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
    app.run(debug=True)