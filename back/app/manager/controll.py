from models.schedule import ScheduleModel
from view.view import imprimir_previa_horarios, imprimir_horarios_professores, imprimir_total_aulas, salvar_tabela_csv
import utils.files as fl

class ScheduleController:
    def __init__(self, materias, carga_horaria, professores, carga_professores, disponibilidade, turmas):
        # self.caminho_arquivo = caminho_arquivo
        self.materias = materias
        self.carga_horaria = carga_horaria
        self.professores = professores
        self.carga_professor = carga_professores
        self.disponibilidade = disponibilidade
        self.turmas = turmas
        # = fl.ler_arquivo_entrada(caminho_arquivo)
        self.model = ScheduleModel(self.materias, self.carga_horaria, self.professores, self.carga_professor, self.disponibilidade, self.turmas)
        self.model.solve()
        self.salvar_grade_csv()

    # def gerar_grade(self):

    def mostrar_grade(self):
        imprimir_previa_horarios(self.turmas, self.model.dias_semana, self.model.horarios_por_dia, self.model.horarios, self.materias, self.professores, self.model.x)
        alocacao_professores = self.model.get_allocation()
        imprimir_horarios_professores(alocacao_professores)
        imprimir_total_aulas(self.turmas, self.materias, self.model.horarios, self.model.x)

    def salvar_grade_csv(self):
        salvar_tabela_csv(self.turmas, self.model.dias_semana, self.model.horarios_por_dia, self.model.horarios, self.materias, self.professores, self.model.x)