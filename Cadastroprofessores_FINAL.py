import json
import os

ARQUIVO_PROFESSOR = "professores.json"


def carregar_dados():
    if not os.path.exists(ARQUIVO_PROFESSOR):
        return []

    try:
        with open(ARQUIVO_PROFESSOR, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        print("\nErro: o arquivo de dados está inválido. A lista será iniciada vazia.")
        return []
    except OSError as erro:
        print(f"\nNão foi possível abrir o arquivo: {erro}")
        return []


def salvar_dados(professores):
    try:
        with open(ARQUIVO_PROFESSOR, "w", encoding="utf-8") as arquivo:
            json.dump(professores, arquivo, indent=4, ensure_ascii=False)
    except OSError as erro:
        print(f"\nNão foi possível salvar os dados: {erro}")


# ---------------------------------------------------------------
# FUNÇÕES PARA OUTROS MÓDULOS (turma, atividade, etc.)
# Uso: from Cadastroprofessor import buscar_professor
# ---------------------------------------------------------------
def buscar_professor(id_professor, professores=None):
    """Devolve o dicionário do professor com esse ID, ou None."""
    if professores is None:
        professores = carregar_dados()

    for professor in professores:
        if professor["id"] == id_professor:
            return professor
    return None


# ---------------------------------------------------------------
# VALIDAÇÕES E ENTRADAS
# ---------------------------------------------------------------
def nome_valido(nome):
    # Aceita letras (com acento), espaços, hífen e apóstrofo. Não aceita números.
    return (
        any(letra.isalpha() for letra in nome)
        and all(letra.isalpha() or letra in " -'" for letra in nome)
    )


def formatar_serie(serie):
    if isinstance(serie, int):
        return f"{serie}º ano"
    return str(serie)


def ler_nome(atual=None):
    texto = f"Nome [{atual}]: " if atual else "Nome do professor: "
    while True:
        nome = input(texto).strip()
        if atual and not nome:
            return atual
        if nome_valido(nome):
            return nome
        print("Nome inválido. Digite apenas letras (sem números ou símbolos).")


def ler_serie(atual=None):
    if atual is not None:
        texto = f"Ano escolar [{formatar_serie(atual)}] (só o número): "
    else:
        texto = "Ano escolar (somente o número, ex.: 1): "
    while True:
        serie = input(texto).strip()
        if atual is not None and not serie:
            return atual
        if serie.isdigit() and int(serie) > 0:
            return int(serie)
        print("Ano inválido. Digite apenas o número (ex.: 1, 2, 3).")


def ler_id():
    try:
        return int(input("Digite o ID do professor: "))
    except ValueError:
        print("\nID inválido. Digite um número inteiro.")
        return None


# ---------------------------------------------------------------
# 1. CRIAR
# ---------------------------------------------------------------
def criar_professor(professores):
    print("\n--- CADASTRAR PROFESSOR ---")

    if professores:
        novo_id = max(professor["id"] for professor in professores) + 1
    else:
        novo_id = 1

    professor = {
        "id": novo_id,
        "nome": ler_nome(),
        "serie": ler_serie(),
    }

    professores.append(professor)
    salvar_dados(professores)
    print(f"\nProfessor cadastrado com sucesso! (ID {novo_id})")


# ---------------------------------------------------------------
# 2. LER
# ---------------------------------------------------------------
def listar_professores(professores):
    if not professores:
        print("\nNenhum professor cadastrado.")
        return

    print("\n--- CONSULTAR PROFESSORES ---")
    print("1. Visualizar todos")
    print("2. Buscar por ID")
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        print()
        for professor in professores:
            print(
                f"ID: {professor['id']} | Nome: {professor['nome']} | "
                f"Série: {formatar_serie(professor.get('serie', '-'))}"
            )
    elif opcao == "2":
        busca_id = ler_id()
        if busca_id is None:
            return

        professor = buscar_professor(busca_id, professores)
        if professor:
            print("\n--- DADOS DO PROFESSOR ---")
            print(f"ID: {professor['id']}")
            print(f"Nome: {professor['nome']}")
            print(f"Série: {formatar_serie(professor.get('serie', '-'))}")
        else:
            print(f"\nProfessor com ID {busca_id} não encontrado.")
    else:
        print("\nOpção inválida.")


# ---------------------------------------------------------------
# 3. ATUALIZAR
# ---------------------------------------------------------------
def atualizar_professor(professores):
    if not professores:
        print("\nNenhum professor disponível para atualização.")
        return

    print("\n--- ATUALIZAR PROFESSOR ---")

    busca_id = ler_id()
    if busca_id is None:
        return

    professor = buscar_professor(busca_id, professores)
    if professor is None:
        print(f"\nProfessor com ID {busca_id} não encontrado.")
        return

    print(f"\nEditando cadastro de: {professor['nome']}")
    print("Deixe o campo vazio para manter a informação atual.")

    professor["nome"] = ler_nome(professor["nome"])
    professor["serie"] = ler_serie(professor.get("serie"))

    salvar_dados(professores)
    print("\nCadastro atualizado com sucesso.")


# ---------------------------------------------------------------
# 4. DELETAR
# ---------------------------------------------------------------
def deletar_professor(professores):
    if not professores:
        print("\nNenhum professor disponível para exclusão.")
        return

    print("\n--- EXCLUIR PROFESSOR ---")

    busca_id = ler_id()
    if busca_id is None:
        return

    professor = buscar_professor(busca_id, professores)
    if professor is None:
        print(f"\nProfessor com ID {busca_id} não encontrado.")
        return

    confirmacao = input(
        f"Deseja excluir o cadastro de {professor['nome']}? (S/N): "
    ).strip().upper()

    if confirmacao == "S":
        professores.remove(professor)
        salvar_dados(professores)
        print("\nCadastro excluído com sucesso.")
    else:
        print("\nExclusão cancelada.")


# ---------------------------------------------------------------
# MENU
# ---------------------------------------------------------------
def menu_professores():
    professores = carregar_dados()

    while True:
        print("=" * 70)
        print("Apo.ia - Professores".center(70))
        print("=" * 70)
        print("1. Cadastrar professor")
        print("2. Consultar professores")
        print("3. Atualizar professor")
        print("4. Deletar professor")
        print("5. Voltar ao menu principal")
        print("=" * 70)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            criar_professor(professores)
        elif opcao == "2":
            listar_professores(professores)
        elif opcao == "3":
            atualizar_professor(professores)
        elif opcao == "4":
            deletar_professor(professores)
        elif opcao == "5":
            return
        else:
            print("\nOpção inválida. Escolha um número de 1 a 5.")


if __name__ == "__main__":
    menu_professores()