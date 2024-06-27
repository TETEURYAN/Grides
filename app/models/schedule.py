import pulp

class ScheduleModel:
    def __init__(self, materias, carga_horaria, professores, carga_professor, disponibilidade, turmas):
        self.materias = materias
        self.carga_horaria = carga_horaria
        self.professores = professores
        self.carga_professor = carga_professor
        self.disponibilidade = disponibilidade
        self.turmas = turmas
        self.dias_semana = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta']
        self.horarios_por_dia = 6
        self.total_horarios = len(self.dias_semana) * self.horarios_por_dia
        self.horarios = range(self.total_horarios)
        self.prob = pulp.LpProblem("GradeHoraria", pulp.LpMaximize)
        self.x = pulp.LpVariable.dicts("x", (self.turmas, self.materias, self.horarios), cat='Binary')

    def define_objective_function(self):
        self.prob += pulp.lpSum(self.x[t][m][h] for t in self.turmas for m in self.materias for h in self.horarios)

    def add_constraints(self):
        for t in self.turmas:
            for m in self.materias:
                self.prob += pulp.lpSum(self.x[t][m][h] for h in self.horarios) == self.carga_horaria[m]
        for p in self.professores.values():
            for h in self.horarios:
                if self.disponibilidade[p][h] == 0:
                    for t in self.turmas:
                        for m in self.materias:
                            if self.professores[m] == p:
                                self.prob += self.x[t][m][h] == 0
        for p in self.professores.values():
            for t in self.turmas:
                for h in self.horarios:
                    self.prob += pulp.lpSum(self.x[t][m][h] for m in self.materias if self.professores[m] == p) <= self.carga_professor[p]
        for h in self.horarios:
            for p in self.professores.values():
                self.prob += pulp.lpSum(self.x[t][m][h] for t in self.turmas for m in self.materias if self.professores[m] == p) <= 1
        for t in self.turmas:
            for h in self.horarios:
                self.prob += pulp.lpSum(self.x[t][m][h] for m in self.materias) <= 1
        for m in self.materias:
            self.prob += pulp.lpSum(self.x[t][m][h] for t in self.turmas for h in self.horarios) <= self.carga_horaria[m] * len(self.turmas)

    def solve(self):
        self.define_objective_function()
        self.add_constraints()
        self.prob.solve()

    def get_schedule(self):
        schedule = {}
        for t in self.turmas:
            schedule[t] = {h: None for h in self.horarios}
            for h in self.horarios:
                for m in self.materias:
                    if pulp.value(self.x[t][m][h]) == 1:
                        schedule[t][h] = m
        return schedule

    def get_allocation(self):
        allocation = {p: [] for p in self.professores.values()}
        for t in self.turmas:
            for h in self.horarios:
                for m in self.materias:
                    if pulp.value(self.x[t][m][h]) == 1:
                        professor = self.professores[m]
                        dia_semana = self.dias_semana[h // self.horarios_por_dia]
                        horario = (h % self.horarios_por_dia) + 1
                        allocation[professor].append(f"{dia_semana} Horário {horario} - {t}")
        return allocation
