import csv
import pulp
import os
import files.files as fl

# Caminho para o arquivo de entrada
caminho_arquivo = os.path.join('..', 'tests', 'ex01.in')

# Função para combinar matéria e professor responsável
def materia_professor(materia, professor):
    return f"{materia} ({professor})"

# Leitura dos dados de entrada
materias, carga_horaria, professores, carga_professor, disponibilidade, turmas = fl.ler_arquivo_entrada(caminho_arquivo)

dias_semana = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta']
horarios_por_dia = 6
total_horarios = len(dias_semana) * horarios_por_dia
horarios = range(total_horarios)

# Problema de otimização
prob = pulp.LpProblem("GradeHoraria", pulp.LpMaximize)

# Variáveis de decisão
x = pulp.LpVariable.dicts("x", (turmas, materias, horarios), cat='Binary')

# Função Objetivo (Aqui podemos definir uma função objetivo simples ou apenas satisfazer as restrições)
prob += pulp.lpSum(x[t][m][h] for t in turmas for m in materias for h in horarios)

# Restrições de Carga Horária das Matérias por Turma
for t in turmas:
    for m in materias:
        prob += pulp.lpSum(x[t][m][h] for h in horarios) == carga_horaria[m]

# Restrições de Disponibilidade dos Professores
for p in professores.values():
    for h in horarios:
        if disponibilidade[p][h] == 0:
            for t in turmas:
                for m in materias:
                    if professores[m] == p:
                        prob += x[t][m][h] == 0

# Restrições de Carga Horária dos Professores
for p in professores.values():
    for t in turmas:
        for h in horarios:
            prob += pulp.lpSum(x[t][m][h] for m in materias if professores[m] == p) <= carga_professor[p]

# Conflitos de Horário (Evitar que um professor esteja em dois lugares ao mesmo tempo)
for h in horarios:
    for p in professores.values():
        prob += pulp.lpSum(x[t][m][h] for t in turmas for m in materias if professores[m] == p) <= 1

# Restrições para evitar que duas matérias diferentes sejam ministradas no mesmo horário para a mesma turma
for t in turmas:
    for h in horarios:
        prob += pulp.lpSum(x[t][m][h] for m in materias) <= 1

# Restrições para evitar que a carga horária total das matérias exceda a capacidade disponível
for m in materias:
    prob += pulp.lpSum(x[t][m][h] for t in turmas for h in horarios) <= carga_horaria[m] * len(turmas)

# Resolver o problema
prob.solve()

# Função para justificar texto na impressão
def justify(text, width):
    return text.ljust(width)

# Largura máxima para colunas na impressão
col_width = 20

# Vetor de alocação para contar os horários de cada professor
alocacao_professores = {p: [] for p in professores.values()}

# Preenchimento do vetor de alocação com base nos valores das variáveis de decisão
for t in turmas:
    for h in horarios:
        for m in materias:
            if pulp.value(x[t][m][h]) == 1:
                professor = professores[m]
                dia_semana = dias_semana[h // horarios_por_dia]
                horario = (h % horarios_por_dia) + 1
                alocacao_professores[professor].append(f"{dia_semana} Horário {horario} - {t}")

# Imprimir prévia dos horários na tela para as três turmas
for turma in turmas:
    print(f"\nPrévia dos Horários para {turma}:") print('\t'.join([justify(dia, col_width) for dia in [''] + dias_semana]))
    for i in range(horarios_por_dia):
        linha = [justify(f'Horário {i+1}', col_width)]
        for j in range(len(dias_semana)):
            materia = ''
            for m in materias:
                if pulp.value(x[turma][m][i + j * horarios_por_dia]) == 1:
                    materia = materia_professor(m, professores[m])
                    break
            linha.append(justify(materia, col_width))
        print('\t'.join(linha))

# Imprimir horários de cada professor

print("\nHorários de cada professor:")
for professor in alocacao_professores.keys():
    if alocacao_professores[professor]:
        print(f"{professor}: {', '.join(alocacao_professores[professor])}")

# Imprimir total de aulas semanais de cada turma
for turma in turmas:
    total_aulas = sum(pulp.value(x[turma][m][h]) for m in materias for h in horarios)
    print(f"Total de aulas semanais para {turma}: {total_aulas}")

# Criar e salvar a tabela em um arquivo .csv
with open('grade_horaria.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Escrever tabelas para cada turma
    for turma in turmas:
        writer.writerow([f"Tabela para {turma}"] + [""] * (len(dias_semana) - 1))
        writer.writerow([''] + dias_semana)  # Cabeçalho
        for i in range(horarios_por_dia):
            linha = [f'Horário {i+1}']
            for j in range(len(dias_semana)):
                materia = ''
                for m in materias:
                    if pulp.value(x[turma][m][i + j * horarios_por_dia]) == 1:
                        materia = materia_professor(m, professores[m])
                        break
                linha.append(materia)
            writer.writerow(linha)
        writer.writerow([])  # Linha em branco entre as tabelas
