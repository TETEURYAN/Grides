from models.schedule import ScheduleModel
from view.view import imprimir_previa_horarios, imprimir_horarios_professores, imprimir_total_aulas, salvar_tabela_csv
import utils.files as fl

class ScheduleController:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.materias, self.carga_horaria, self.professores, self.carga_professor, self.disponibilidade, self.turmas = fl.ler_arquivo_entrada(caminho_arquivo)
        self.model = ScheduleModel(self.materias, self.carga_horaria, self.professores, self.carga_professor, self.disponibilidade, self.turmas)

    def gerar_grade(self):
        self.model.solve()

    def mostrar_grade(self):
        imprimir_previa_horarios(self.turmas, self.model.dias_semana, self.model.horarios_por_dia, self.model.horarios, self.materias, self.professores, self.model.x)
        alocacao_professores = self.model.get_allocation()
        imprimir_horarios_professores(alocacao_professores)
        imprimir_total_aulas(self.turmas, self.materias, self.model.horarios, self.model.x)

    def salvar_grade_csv(self):
        salvar_tabela_csv(self.turmas, self.model.dias_semana, self.model.horarios_por_dia, self.model.horarios, self.materias, self.professores, self.model.x)