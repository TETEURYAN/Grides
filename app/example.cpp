from ortools.sat.python import cp_model

def main():
    # Dados de entrada ajustados
    professores = {
        'Prof1': {'disciplinas': ['Mat1', 'Mat2'], 'horarios': list(range(1, 13)), 'carga_horaria': 6},
        'Prof2': {'disciplinas': ['Mat3', 'Mat4'], 'horarios': list(range(1, 13)), 'carga_horaria': 6},
        'Prof3': {'disciplinas': ['Mat5', 'Mat6'], 'horarios': list(range(1, 13)), 'carga_horaria': 6}
    }

    turmas = {
        'T1': ['Mat1', 'Mat2', 'Mat3'],
        'T2': ['Mat1', 'Mat4', 'Mat5'],
        'T3': ['Mat2', 'Mat3', 'Mat5']
    }

    horarios = list(range(1, 13))  # 12 horários (6 de manhã e 6 de tarde)

    # Carga horária das disciplinas
    carga_horaria_disciplinas = {
        'Mat1': 2,
        'Mat2': 2,
        'Mat3': 2,
        'Mat4': 2,
        'Mat5': 2,
        'Mat6': 2
    }

    # Criação do modelo CP-SAT
    model = cp_model.CpModel()

    # Variáveis de decisão
    x = {}
    for prof in professores:
        for turma in turmas:
            for disciplina in professores[prof]['disciplinas']:
                for horario in horarios:
                    x[(prof, turma, disciplina, horario)] = model.NewBoolVar(f'x_{prof}_{turma}_{disciplina}_{horario}')

    # Restrições
    # Cada disciplina de cada turma deve ser lecionada exatamente uma vez
    for turma in turmas:
        for disciplina in turmas[turma]:
            model.Add(sum(x[(prof, turma, disciplina, horario)]
                          for prof in professores
                          if disciplina in professores[prof]['disciplinas']
                          for horario in professores[prof]['horarios']
                          if (prof, turma, disciplina, horario) in x) == 1)

    # Um professor não pode lecionar mais de uma disciplina no mesmo horário
    for prof in professores:
        for horario in horarios:
            model.Add(sum(x[(prof, turma, disciplina, horario)]
                          for turma in turmas
                          for disciplina in professores[prof]['disciplinas']
                          if (prof, turma, disciplina, horario) in x) <= 1)

    # Restrições de carga horária dos professores
    for prof in professores:
        carga_horaria_max = professores[prof]['carga_horaria']
        model.Add(sum(x[(prof, turma, disciplina, horario)] * carga_horaria_disciplinas[disciplina]
                      for turma in turmas
                      for disciplina in professores[prof]['disciplinas']
                      for horario in horarios
                      if (prof, turma, disciplina, horario) in x) <= carga_horaria_max)

    # Resolver o modelo
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Solução encontrada:")
        for turma in turmas:
            print(f"Turma {turma}:")
            for disciplina in turmas[turma]:
                alocado = False
                for prof in professores:
                    for horario in horarios:
                        if (prof, turma, disciplina, horario) in x and solver.BooleanValue(x[(prof, turma, disciplina, horario)]):
                            print(f"  Disciplina {disciplina} ministrada por {prof} no horário {horario}")
                            alocado = True
                if not alocado:
                    print(f"  Disciplina {disciplina} não foi alocada")
    else:
        print("Nenhuma solução encontrada.")
        # Adiciona informações detalhadas sobre as variáveis e restrições para depuração
        for turma in turmas:
            for disciplina in turmas[turma]:
                for prof in professores:
                    for horario in horarios:
                        if (prof, turma, disciplina, horario) in x:
                            print(f'x_{prof}_{turma}_{disciplina}_{horario} = {solver.BooleanValue(x[(prof, turma, disciplina, horario)])}')

        print("\nVerifique os horários e cargas horárias para garantir consistência.")

if __name__ == '__main__':
    main()
