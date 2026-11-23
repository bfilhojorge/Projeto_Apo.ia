#CADASTRO DE TURMAS - APOIA - ANA CAROLINA

import json
from Cadastroprofessores_FINAL import carregar_dados as carregar_professores
from Cadastroprofessores_FINAL import buscar_professor

turmas = []


def salvar_turmas():
    try:
        with open("turmas.json", "w", encoding="utf-8") as arquivo:
            json.dump(turmas, arquivo, ensure_ascii=False, indent=4)
        print("Dados salvos com sucesso!")
        return True
    except (OSError, TypeError, ValueError):
        print("Erro ao salvar as turmas.")
        return False


def carregar_turmas():
    try:
        with open("turmas.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        if not isinstance(dados, list):
            print("O arquivo não contém uma lista de turmas.")
            return False
        for turma in dados:
            if not isinstance(turma, dict):
                print("O arquivo contém uma turma inválida.")
                return False
            if "id" not in turma or "ano_serie" not in turma or "professor" not in turma or "estudantes" not in turma:
                print("Faltam informações em uma turma do arquivo.")
                return False
            if type(turma["id"]) is not int or turma["id"] <= 0:
                print("O arquivo contém um ID de turma inválido.")
                return False
            if not isinstance(turma["ano_serie"], str) or not isinstance(turma["professor"], str):
                print("O arquivo contém campos de texto inválidos.")
                return False
            if turma["ano_serie"].strip() == "" or turma["professor"].strip() == "":
                print("O arquivo contém campos vazios.")
                return False
            if "id_professor" in turma and type(turma["id_professor"]) is not int:
                print("O arquivo contém um ID de professor inválido.")
                return False
            if not isinstance(turma["estudantes"], list):
                print("O arquivo contém uma lista de estudantes inválida.")
                return False
            for id_estudante in turma["estudantes"]:
                if type(id_estudante) is not int or id_estudante <= 0:
                    print("O arquivo contém um ID de estudante inválido.")
                    return False
        turmas.clear()
        turmas.extend(dados)
        print("Turmas carregadas com sucesso!")
        return True
    except FileNotFoundError:
        print("Nenhum arquivo encontrado. Iniciando com lista vazia.")
        return True
    except (OSError, UnicodeError, json.JSONDecodeError):
        print("Erro ao ler o arquivo de turmas. O menu não será aberto para proteger os dados.")
        return False


# ---------------------------------------------------------------
# PROFESSORES (lidos do professores.json)
# ---------------------------------------------------------------
def selecionar_professor():
    """Mostra os professores cadastrados e devolve o escolhido (ou None)."""
    professores = carregar_professores()
    if not professores:
        print("Nenhum professor cadastrado. Cadastre um professor antes.")
        return None

    print("\nProfessores cadastrados:")
    for professor in professores:
        print(f"  ID {professor['id']} - {professor['nome']}")
    print()

    while True:
        entrada = input("Digite o ID do professor responsável (0 para cancelar): ").strip()
        try:
            id_professor = int(entrada)
        except ValueError:
            print("Digite um número inteiro válido.")
            continue
        if id_professor == 0:
            return None
        professor = buscar_professor(id_professor, professores)
        if professor is None:
            print("Professor não encontrado. Escolha um ID da lista.")
        else:
            return professor


def nome_professor(turma):
    """Nome atual do professor (se ele foi renomeado, aparece o nome novo)."""
    if "id_professor" in turma:
        professor = buscar_professor(turma["id_professor"])
        if professor:
            return professor["nome"]
    return turma["professor"]


# ---------------------------------------------------------------
# TURMAS
# ---------------------------------------------------------------
def cadastrar_turma():
    while True:
        try:
            id_turma = int(input("Digite um número para identificar a nova turma:  "))
            if id_turma <= 0:
                print("ID inválido! Digite um número inteiro maior que zero.")
                continue
            id_existe = False
            for turma in turmas:
                if turma["id"] == id_turma:
                    id_existe = True
                    break
            if id_existe:
                print("Esse ID já está cadastrado.")
            else:
                break
        except ValueError:
            print("Digite um número inteiro válido.")
    ano_serie = input("Digite o ano/série: ").strip()
    if ano_serie == "":
        print("Ano/série não pode ficar vazio.")
        return

    professor = selecionar_professor()
    if professor is None:
        print("Cadastro da turma cancelado.")
        return

    turma = {
        "id": id_turma,
        "ano_serie": ano_serie,
        "professor": professor["nome"],
        "id_professor": professor["id"],
        "estudantes": [],
    }
    turmas.append(turma)
    print(f"Turma cadastrada com o professor {professor['nome']}!")
    salvar_turmas()


def listar_turmas():
    if len(turmas) == 0:
        print("Nenhuma turma cadastrada.")
        return
    for turma in turmas:
        print("ID:", turma["id"])
        print("Ano/Série:", turma["ano_serie"])
        print("Professor:", nome_professor(turma))
        print("--------------------")


def consultar_turma():
    try:
        id_busca = int(input("Digite o ID da turma: "))
        for turma in turmas:
            if turma["id"] == id_busca:
                print("ID:", turma["id"])
                print("Ano/Série:", turma["ano_serie"])
                print("Professor:", nome_professor(turma))
                print("IDs dos estudantes:", turma["estudantes"])
                return
        print("Turma não encontrada.")
    except ValueError:
        print("Digite um número inteiro válido.")


# ---------------------------------------------------------------
# ALUNOS (lidos do alunos.json)
# ---------------------------------------------------------------
def carregar_alunos():
    try:
        with open("alunos.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def buscar_aluno(id_estudante):
    for aluno in carregar_alunos():
        if aluno["id"] == id_estudante:
            return aluno
    return None


def listar_alunos_cadastrados():
    alunos = carregar_alunos()
    if not alunos:
        print("Nenhum aluno cadastrado ainda.")
        return
    print("\nAlunos cadastrados:")
    for aluno in alunos:
        print(f"  ID {aluno['id']} - {aluno['nome']}")
    print()


def adicionar_estudante():
    try:
        listar_alunos_cadastrados()   # ajuda a lembrar o ID
        id_turma = int(input("Digite o ID da turma: "))
        id_estudante = int(input("Digite o ID do estudante: "))
        if id_turma <= 0 or id_estudante <= 0:
            print("Os IDs devem ser positivos.")
            return

        aluno = buscar_aluno(id_estudante)   # lê do alunos.json
        if aluno is None:
            print("Aluno não cadastrado.")
            return

        for turma in turmas:
            if turma["id"] == id_turma:
                if id_estudante in turma["estudantes"]:
                    print("Aluno já vinculado a esta turma.")
                else:
                    turma["estudantes"].append(id_estudante)
                    salvar_turmas()
                    print(f"{aluno['nome']} vinculado à turma!")
                return
        print("Turma não encontrada.")
    except ValueError:
        print("Digite números inteiros válidos.")


def consultar_estudantes_turma():
    try:
        id_turma = int(input("Digite o ID da turma: "))
        for turma in turmas:
            if turma["id"] == id_turma:
                if len(turma["estudantes"]) == 0:
                    print("Esta turma não possui estudantes.")
                    return
                for id_estudante in turma["estudantes"]:
                    estudante = buscar_aluno(id_estudante)   # lê do alunos.json
                    if estudante is None:
                        print("Estudante ID", id_estudante, "não encontrado no cadastro atual.")
                        continue
                    print("Nome:", estudante["nome"])
                    if estudante.get("perfil_cadastrado"):
                        print("Perfil pedagógico: Cadastrado")
                    else:
                        print("Perfil pedagógico: Pendente")
                    print("--------------------")
                return
        print("Turma não encontrada.")
    except ValueError:
        print("Digite um número inteiro válido.")


def editar_turma():
    try:
        id_busca = int(input("Digite o ID da turma: "))
        for turma in turmas:
            if turma["id"] == id_busca:
                print("1 - Alterar ano/série")
                print("2 - Alterar professor")
                print("3 - Remover aluno da turma")
                print("0 - Cancelar")
                opcao = input("Escolha uma opção: ")
                if opcao == "1":
                    novo_ano = input("Novo ano/série: ").strip()
                    if novo_ano == "":
                        print("Ano/série não pode ficar vazio.")
                        return
                    turma["ano_serie"] = novo_ano
                elif opcao == "2":
                    novo_professor = selecionar_professor()
                    if novo_professor is None:
                        print("Alteração cancelada.")
                        return
                    turma["professor"] = novo_professor["nome"]
                    turma["id_professor"] = novo_professor["id"]
                elif opcao == "3":
                    if len(turma["estudantes"]) == 0:
                        print("Esta turma não possui estudantes.")
                        return
                    print("IDs dos estudantes na turma:", turma["estudantes"])
                    try:
                        id_remover = int(input("Digite o ID do estudante a remover: "))
                    except ValueError:
                        print("Digite um número inteiro válido.")
                        return
                    if id_remover in turma["estudantes"]:
                        turma["estudantes"].remove(id_remover)
                        print(f"Estudante ID {id_remover} removido da turma.")
                    else:
                        print("Estudante não encontrado nesta turma.")
                elif opcao == "0":
                    print("Alteração cancelada.")
                    return
                else:
                    print("Opção inválida.")
                    return
                print("Turma atualizada!")
                salvar_turmas()
                return
        print("Turma não encontrada.")
    except ValueError:
        print("Digite um número inteiro válido.")


def excluir_turma():
    try:
        id_busca = int(input("Digite o ID da turma: "))
        for turma in turmas:
            if turma["id"] == id_busca:
                print("Turma:", turma["ano_serie"], "-", nome_professor(turma))
                confirmacao = input("Confirma a exclusão? (S/N): ")
                if confirmacao.upper() == "S":
                    turmas.remove(turma)
                    print("Turma excluída!")
                    salvar_turmas()
                else:
                    print("Exclusão cancelada.")
                return
        print("Turma não encontrada.")
    except ValueError:
        print("Digite um número inteiro válido.")


def menu_turmas():
    while True:
        print("=" * 70)
        print("Apo.ia - Turmas".center(70))
        print("=" * 70)
        print("1 - Cadastrar turma")
        print("2 - Listar turmas")
        print("3 - Consultar turma")
        print("4 - Adicionar estudante")
        print("5 - Consultar estudantes e perfis")
        print("6 - Editar turma")
        print("7 - Excluir turma")
        print("0 - Sair")
        print("=" * 70)
        opcao = input("Escolha uma opção: ")
        print("=" * 70)
        if opcao == "1":
            cadastrar_turma()
        elif opcao == "2":
            listar_turmas()
        elif opcao == "3":
            consultar_turma()
        elif opcao == "4":
            adicionar_estudante()
        elif opcao == "5":
            consultar_estudantes_turma()
        elif opcao == "6":
            editar_turma()
        elif opcao == "7":
            excluir_turma()
        elif opcao == "0":
            print("=" * 70)
            print("Saindo do cadastro de turmas.".center(70))
            print("=" * 70)
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    if carregar_turmas():
        menu_turmas()

        #FIM DO CADASTRO DE TURMAS - APOIA - ANA CAROLINA