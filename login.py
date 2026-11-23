ADMIN_EMAIL = "instituição@apo.ia"
ADMIN_SENHA = "123"
MAX_TENTATIVAS = 3


def fazer_login():
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        print("=" * 70)
        email = input("\nE-mail: ").strip().lower()
        senha = input("Senha: ")
        print("=" * 70)

        if email == ADMIN_EMAIL.lower() and senha == ADMIN_SENHA:
            return "Administrador"

        else:
            print("E-mail ou senha incorretos.")
    return None


def tela_login(cabecalho=None):
    while True:
        if cabecalho:
            cabecalho()

        print("=" * 70)
        print("\n  1 - Entrar")
        print("  0 - Sair")
        print("=" * 70)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            usuario = fazer_login()
            if usuario:
                print(f"\nLogin realizado com sucesso! Olá, {usuario}!")
                return usuario
        elif opcao == "0":
            return None
        else:
            print("Opção inválida, tente novamente.")