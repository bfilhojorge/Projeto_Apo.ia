import os

from Cadastroaluno import menu_alunos
from Cadastroprofessores_FINAL import menu_professores
from Cadastroturma_FINAL import menu_turmas
from atividade2 import executar_programa
from login import tela_login

os.system("")


LETRAS = {
    "A": [" ### ",
          "#   #",
          "#####",
          "#   #",
          "#   #"],
    "P": ["#### ",
          "#   #",
          "#### ",
          "#    ",
          "#    "],
    "O": [" ### ",
          "#   #",
          "#   #",
          "#   #",
          " ### "],
    ".": [" ",
          " ",
          " ",
          " ",
          "#"],
    "I": ["###",
          " # ",
          " # ",
          " # ",
          "###"],
}


def exibir_logo():

    branco = "\033[107m"
    reset = "\033[0m"
    texto = "APO.IA"

    print()
    for linha in range(5):
        saida = "  "
        for letra in texto:
            for pixel in LETRAS[letra][linha]:
                if pixel == "#":
                    saida += branco + "  " + reset
                else:
                    saida += "  "
            saida += "  "  # espaço entre as letras
        print(saida)


def exibir_cabecalho():
    print("\n" + "=" * 70)
    exibir_logo()
    print("\n" + "=" * 70)
    print("Bem vindo ao Apo.IA".center(70))
    print("=" * 70)


def exibir_menu():
    exibir_cabecalho()
    print("Selecione uma opção do menu principal:".center(70))
    print("=" * 70)
    print("  1 - Professor")
    print("  2 - Turma")
    print("  3 - Aluno")
    print("  4 - Atividade")
    print("  0 - Sair")
    print("=" * 70)


def main():
    usuario = tela_login(exibir_cabecalho)
    if usuario is None:
        print("Até logo! Apo.ia encerrado.")
        return

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_professores()
        elif opcao == "2":
            menu_turmas()
        elif opcao == "3":
            menu_alunos()
        elif opcao == "4":
            executar_programa()
        elif opcao == "0":
            print("=" * 70)
            print("Até logo! Apo.ia encerrado.".center(70))
            print("=" * 70)
            break
        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    main()
