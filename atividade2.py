from pathlib import Path

def carregar_atividade():
    banco = {}

    caminho = Path(__file__).parent / "atividade.txt"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(";", 2)

            if len(partes) == 3:
                atividade, resposta1, resposta2 = partes
                banco[atividade.lower()] = [resposta1, resposta2]

    return banco


def executar_programa():

    banco = carregar_atividade()

    while True:

        print("=" * 70)
        print("Apo.ia - ATIVIDADES".center(70))
        print("=" * 70)

        atividade = input(
            "\nDigite a atividade que você deseja realizar (ou 0 para voltar ao menu inicial): "
        ).strip().lower()

        if atividade == "0":
            break

        if atividade in banco:

            print("=" * 70)
            print("Primeira sugestão de atividade".center(70))
            print("=" * 70)

            print(banco[atividade][0].replace("\\n", "\n"))

            print("=" * 70)
            print("A atividade condiz com o que deseja aplicar?".center(70))
            print("1 - Sim")
            print("2 - Não")
            print("3 - Voltar ao menu inicial")
            print("=" * 70)

            opcao = input("Digite sua opção: ").strip()

            if opcao == "1":

                print("\nAtividade supriu sua necessidade!")

            elif opcao == "2":

                print("=" * 70)
                print("Segunda sujestão de atividade".center(70))
                print("=" * 70)

                print(banco[atividade][1].replace("\\n", "\n"))
                print("=" * 70)
                print("Atividade reformulada com sucesso!".center(70))
                print("=" * 70)

            elif opcao == "3":

                break

            else:

                print("\nOpção inválida!")

        else:
            print("=" * 70)
            print("Atividade não encontrada!".center(70))
            print("=" * 70)

if __name__ == "__main__":
    executar_programa()
