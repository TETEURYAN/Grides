import csv
import pulp

def materia_professor(materia, professor):
    return f"{materia} ({professor})"

def justify(text, width):
    return text.ljust(width)

def imprimir_previa_horarios(turmas, dias_semana, horarios_por_dia, horarios, materias, professores, x):
    col_width = 20
    for turma in turmas:
        print(f"\nPrévia dos Horários para {turma}:")
        print('\t'.join([justify(dia, col_width) for dia in [''] + dias_semana]))
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

def imprimir_horarios_professores(alocacao_professores):
    print("\nHorários de cada professor:")
    for professor in alocacao_professores.keys():
        if alocacao_professores[professor]:
            print(f"{professor}: {', '.join(alocacao_professores[professor])}")

def imprimir_total_aulas(turmas, materias, horarios, x):
    for turma in turmas:
        total_aulas = sum(pulp.value(x[turma][m][h]) for m in materias for h in horarios)
        print(f"Total de aulas semanais para {turma}: {total_aulas}")

def salvar_tabela_csv(turmas, dias_semana, horarios_por_dia, horarios, materias, professores, x):
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
