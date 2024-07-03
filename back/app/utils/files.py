import os

def ler_arquivo_entrada(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()

    indice = 0
    numero_turmas = int(linhas[indice].strip())
    indice += 1

    numero_materias = int(linhas[indice].strip())
    indice += 1

    materias = []
    carga_horaria = {}
    for _ in range(numero_materias):
        linha = linhas[indice].strip().split()
        materias.append(linha[0])
        carga_horaria[linha[0]] = int(linha[1])
        indice += 1

    numero_professores = int(linhas[indice].strip())
    indice += 1

    professores = {}
    carga_professor = {}
    for _ in range(numero_professores):
        linha = linhas[indice].strip().split()
        professores[linha[1]] = linha[0]
        carga_professor[linha[0]] = int(linha[2])
        indice += 1

    disponibilidade = {}
    for _ in range(numero_professores):
        professor = linhas[indice].strip()
        indice += 1
        disponibilidade[professor] = [int(x) for x in linhas[indice].strip().split()]
        indice += 1

    turmas = [f'Turma{i+1}' for i in range(numero_turmas)]
    return materias, carga_horaria, professores, carga_professor, disponibilidade, turmas