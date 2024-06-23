import csv
import pulp

# Dados de entrada
professores = {'Matematica': 'ProfA', 'Portugues': 'ProfB', 'Historia': 'ProfC'}
materias = ['Matematica', 'Portugues', 'Historia']
turmas = ['Turma1', 'Turma2', 'Turma3']
dias_semana = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta']
horarios_por_dia = 6
total_horarios = len(dias_semana) * horarios_por_dia
horarios = range(total_horarios)
carga_horaria = {'Matematica': 5, 'Portugues': 5, 'Historia': 5}
disponibilidade = {
    'ProfA': [1] * total_horarios,
    'ProfB': [1] * total_horarios,
    'ProfC': [1] * total_horarios
}
carga_professor = {'ProfA': 15, 'ProfB': 15, 'ProfC': 15}

# Problema de otimização
prob = pulp.LpProblem("GradeHoraria", pulp.LpMaximize)

# Variáveis de decisão
x = pulp.LpVariable.dicts("x", (turmas, materias, horarios), cat='Binary')

# Função Objetivo (Aqui podemos definir uma função objetivo simples ou apenas satisfazer as restrições)
prob += pulp.lpSum(x[t][m][h] for t in turmas for m in materias for h in horarios)

# Restrições de Carga Horária das Matérias
for t in turmas:
    for m in materias:
        prob += pulp.lpSum(x[t][m][h] for h in horarios) == carga_horaria[m]

# Restrições de Disponibilidade dos Professores
for p in professores.values():
    for h in horarios:
        if disponibilidade[p][h] == 0:
            for t in turmas:
                for m in materias:
                    prob += x[t][m][h] == 0

# Restrições de Carga Horária dos Professores
for p in professores.values():
    for m in materias:
        prob += pulp.lpSum(x[t][m][h] for t in turmas for h in horarios) <= carga_professor[p]

# Conflitos de Horário (Evitar que um professor esteja em dois lugares ao mesmo tempo)
for h in horarios:
    for p in professores.values():
        prob += pulp.lpSum(x[t][m][h] for t in turmas for m in materias if professores[m] == p) <= 1

# Restrição para alocar todas as aulas de cada disciplina
for m in materias:
    prob += pulp.lpSum(x[t][m][h] for t in turmas for h in horarios) >= carga_horaria[m] * len(turmas)

# Resolver o problema
prob.solve()

# Função para combinar matéria e professor responsável
def materia_professor(materia):
    return f"{materia} ({professores[materia]})"

for turma in turmas:
    print(f"Prévia dos Horários para {turma}:")
    print('\t' + '\t'.join(dias_semana))
    for i in range(horarios_por_dia):
        linha = [f'Horário {i+1}']
        for j in range(len(dias_semana)):
            materia = ''
            for m in materias:
                if pulp.value(x[turma][m][i + j * horarios_por_dia]) == 1:
                    materia = materia_professor(m)
                    break
            linha.append(materia)
        print('\t'.join(linha))

print("\nHorários de cada professor:")
for professor, disponibilidade_horarios in disponibilidade.items():
    horarios_alocados = [i + 1 for i, disp in enumerate(disponibilidade_horarios) if disp == 1 and any(pulp.value(x[t][m][i]) == 1 for t in turmas for m in materias if professores[m] == professor)]
    if horarios_alocados:
        print(f"{professor}: {horarios_alocados}")

for turma in turmas:
    total_aulas = sum(pulp.value(pulp.lpSum(x[turma][m][h] for m in materias for h in horarios)) for turma in turmas)
    print(f"Total de aulas semanais para {turma}: {total_aulas}")

with open('grade_horaria.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    for turma in turmas:
        writer.writerow([f"Tabela para {turma}"] + [""] * (len(dias_semana) + 2))
        writer.writerow([''] + dias_semana + ['', 'Matéria', 'Professor'])  # Cabeçalho
        for i in range(horarios_por_dia):
            linha = [f'Horário {i+1}']
            for j in range(len(dias_semana)):
                materia = ''
                for m in materias:
                    if pulp.value(x[turma][m][i + j * horarios_por_dia]) == 1:
                        materia = materia_professor(m)
                        break
                linha.append(materia)
            writer.writerow(linha + ['', '', ''])  # Adiciona células vazias para separar matéria e professor
        writer.writerow([])  # Linha em branco entre as tabelas
