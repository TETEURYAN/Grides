from manager.controll import ScheduleController
import os

def main():
    # Caminho para o arquivo de entrada
    caminho_arquivo = os.path.join('..', 'tests', 'ex01.in')  # Ajuste este caminho conforme necessário

    # Cria uma instância do controlador
    controller = ScheduleController(caminho_arquivo)
    
    # Gera a grade horária
    controller.gerar_grade()
    
    # Mostra a grade horária
    controller.mostrar_grade()
    
    # Salva a grade horária em um arquivo CSV
    controller.salvar_grade_csv()

if __name__ == "__main__":
    main()
