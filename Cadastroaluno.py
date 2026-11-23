import json
import os

ARQUIVO_DADOS = "alunos.json"
NIVEIS_SUPORTE = ("1", "2", "3")


def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return []

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        print("\nErro: o arquivo de dados está inválido. A lista será iniciada vazia.")
        return []
    except OSError as erro:
        print(f"\nNão foi possível abrir o arquivo: {erro}")
        return []


def salvar_dados(alunos):
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(alunos, arquivo, indent=4, ensure_ascii=False)
    except OSError as erro:
        print(f"\nNão foi possível salvar os dados: {erro}")


def nome_valido(nome):
    # Aceita letras (com acento), espaços, hífen e apóstrofo. Não aceita números.
    return (
        any(letra.isalpha() for letra in nome)
        and all(letra.isalpha() or letra in " -'" for letra in nome)
    )


def criar_aluno(alunos):
    print("\n--- CADASTRAR ALUNO ---")

    if alunos:
        novo_id = max(aluno["id"] for aluno in alunos) + 1
    else:
        novo_id = 1

    nome = input("Nome do aluno: ").strip()
    while not nome_valido(nome):
        print("Nome inválido. Digite apenas letras (sem números ou símbolos).")
        nome = input("Nome do aluno: ").strip()

    while True:
        try:
            idade = int(input("Idade: "))
            if idade <= 0:
                print("A idade deve ser maior que zero.")
            else:
                break
        except ValueError:
            print("Digite uma idade usando números inteiros.")

    serie = input("Ano escolar (somente o número, ex.: 1): ").strip()
    while not (serie.isdigit() and int(serie) > 0):
        print("Ano inválido. Digite apenas o número (ex.: 1, 2, 3).")
        serie = input("Ano escolar (somente o número, ex.: 1): ").strip()
    serie = int(serie)

    print("Níveis de suporte disponíveis: 1, 2 ou 3.")
    nivel_suporte = input("Nível de suporte: ").strip()
    while nivel_suporte not in NIVEIS_SUPORTE:
        print("Opção inválida. Escolha 1, 2 ou 3.")
        nivel_suporte = input("Nível de suporte: ").strip()

    interesses = input("Interesses: ").strip()
    necessidades = input("Necessidades específicas de aprendizagem: ").strip()

    novo_aluno = {
        "id": novo_id,
        "nome": nome,
        "idade": idade,
        "serie": f"{serie} ano",
        "nivel_suporte": f"Nível {nivel_suporte}",
        "interesses": interesses if interesses else "Não informado",
        "necessidades": necessidades if necessidades else "Não informado"
    }

    alunos.append(novo_aluno)
    salvar_dados(alunos)
    print(f"\nAluno(a) {nome} cadastrado(a) com sucesso. ID: {novo_id}")


def listar_alunos(alunos):
    if not alunos:
        print("\nNenhum aluno cadastrado.")
        return

    print("\n--- CONSULTAR ALUNOS ---")
    print("1. Visualizar todos")
    print("2. Buscar por ID")
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        for aluno in alunos:
            print(
                f"ID: {aluno['id']} | Nome: {aluno['nome']} | "
                f"Série: {aluno['serie']} | Suporte: {aluno['nivel_suporte']}"
            )
    elif opcao == "2":
        try:
            busca_id = int(input("Digite o ID do aluno: "))
            aluno_encontrado = None

            for aluno in alunos:
                if aluno["id"] == busca_id:
                    aluno_encontrado = aluno
                    break

            if aluno_encontrado:
                print("\n--- DADOS DO ALUNO ---")
                for campo, valor in aluno_encontrado.items():
                    print(f"{campo.capitalize()}: {valor}")
            else:
                print(f"\nAluno com ID {busca_id} não encontrado.")
        except ValueError:
            print("\nID inválido. Digite um número inteiro.")
    else:
        print("\nOpção inválida.")


def atualizar_aluno(alunos):
    if not alunos:
        print("\nNenhum aluno disponível para atualização.")
        return

    print("\n--- ATUALIZAR ALUNO ---")

    try:
        busca_id = int(input("Digite o ID do aluno: "))
    except ValueError:
        print("\nID inválido. Digite um número inteiro.")
        return

    aluno = None
    for cadastro in alunos:
        if cadastro["id"] == busca_id:
            aluno = cadastro
            break

    if aluno is None:
        print(f"\nAluno com ID {busca_id} não encontrado.")
        return

    print(f"\nEditando cadastro de: {aluno['nome']}")
    print("Deixe o campo vazio para manter a informação atual.")

    novo_nome = input(f"Nome [{aluno['nome']}]: ").strip()
    while novo_nome and not nome_valido(novo_nome):
        print("Nome inválido. Digite apenas letras (sem números ou símbolos).")
        novo_nome = input(f"Nome [{aluno['nome']}]: ").strip()
    if novo_nome:
        aluno["nome"] = novo_nome

    while True:
        nova_idade = input(f"Idade [{aluno['idade']}]: ").strip()
        if not nova_idade:
            break
        try:
            idade = int(nova_idade)
            if idade <= 0:
                print("A idade deve ser maior que zero.")
            else:
                aluno["idade"] = idade
                break
        except ValueError:
            print("Digite uma idade usando números inteiros.")

    nova_serie = input(f"Ano escolar [{aluno['serie']}] (só o número): ").strip()
    while nova_serie and not (nova_serie.isdigit() and int(nova_serie) > 0):
        print("Ano inválido. Digite apenas o número (ex.: 1, 2, 3).")
        nova_serie = input(f"Ano escolar [{aluno['serie']}] (só o número): ").strip()
    if nova_serie:
        aluno["serie"] = f"{int(nova_serie)} ano"

    print("Níveis de suporte disponíveis: 1, 2 ou 3.")
    novo_nivel = input(
        f"Nível de suporte [{aluno['nivel_suporte']}]: "
    ).strip()

    if novo_nivel:
        while novo_nivel and novo_nivel not in NIVEIS_SUPORTE:
            print("Opção inválida. Escolha 1, 2 ou 3, ou deixe em branco.")
            novo_nivel = input("Novo nível de suporte: ").strip()
        if novo_nivel:
            aluno["nivel_suporte"] = f"Nível {novo_nivel}"

    novos_interesses = input(
        f"Interesses [{aluno['interesses']}]: "
    ).strip()
    if novos_interesses:
        aluno["interesses"] = novos_interesses

    novas_necessidades = input(
        f"Necessidades [{aluno['necessidades']}]: "
    ).strip()
    if novas_necessidades:
        aluno["necessidades"] = novas_necessidades

    salvar_dados(alunos)
    print("\nCadastro atualizado com sucesso.")


def deletar_aluno(alunos):
    if not alunos:
        print("\nNenhum aluno disponível para exclusão.")
        return

    print("\n--- EXCLUIR ALUNO ---")

    try:
        busca_id = int(input("Digite o ID do aluno: "))
    except ValueError:
        print("\nID inválido. Digite um número inteiro.")
        return

    aluno = None
    for cadastro in alunos:
        if cadastro["id"] == busca_id:
            aluno = cadastro
            break

    if aluno is None:
        print(f"\nAluno com ID {busca_id} não encontrado.")
        return

    confirmacao = input(
        f"Deseja excluir o cadastro de {aluno['nome']}? (S/N): "
    ).strip().upper()

    if confirmacao == "S":
        alunos.remove(aluno)
        salvar_dados(alunos)
        print("\nCadastro excluído com sucesso.")
    else:
        print("\nExclusão cancelada.")


def menu_alunos():
    alunos = carregar_dados()

    while True:
        print("=" * 70)
        print("Apo.ia - Alunos".center(70))
        print("=" * 70)
        print("1. Cadastrar alunos")
        print("2. Consultar alunos")
        print("3. Atualizar aluno")
        print("4. Deletar aluno")
        print("5. Voltar ao menu principal")
        print("=" * 70)

        opcao = input("Escolha uma opção (1-5): ").strip()
        print("=" * 70)
        if opcao == "1":
            criar_aluno(alunos)
        elif opcao == "2":
            listar_alunos(alunos)
        elif opcao == "3":
            atualizar_aluno(alunos)
        elif opcao == "4":
            deletar_aluno(alunos)
        elif opcao == "5":
            return
        else:
            print("\nOpção inválida. Escolha um número de 1 a 5.")
            print("=" * 70)

if __name__ == "__main__":
    menu_alunos()