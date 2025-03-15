professores = []

def cadastrar_professor():
    nome = input("Digite o nome do professor: ")
    email = input("Digite o e-mail do professor: ")
    sala_de_atendimento = input("Digite a sala de atendimento do professor: ")
    professores.append({"nome": nome, "email": email, "sala_de_atendimento": sala_de_atendimento})
    print(f"Professor {nome} cadastrado com sucesso!")

def listar_professores():
    if not professores:
        print("Nenhum professor cadastrado.")
    else:
        for professor in professores:
            print(f"Nome: {professor['nome']}, E-mail: {professor['email']}, Sala: {professor['sala_de_atendimento']}")

def atualizar_professor():
    nome = input("Digite o nome do professor a ser atualizado: ")
    for professor in professores:
        if professor["nome"] == nome:
            professor["email"] = input("Digite o novo e-mail: ")
            professor["sala_de_atendimento"] = input("Digite a nova sala de atendimento: ")
            print("Professor atualizado com sucesso!")
            return
    print("Professor não encontrado.")

def remover_professor():
    nome = input("Digite o nome do professor a ser removido: ")
    for professor in professores:
        if professor["nome"] == nome:
            professores.remove(professor)
            print("Professor removido com sucesso!")
            return
    print("Professor não encontrado.")

def main():
    while True:
        print("\nMenu de Opções:")
        print("1. Cadastrar Professor")
        print("2. Listar Professores")
        print("3. Atualizar Professor")
        print("4. Remover Professor")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            cadastrar_professor()
        elif opcao == '2':
            listar_professores()
        elif opcao == '3':
            atualizar_professor()
        elif opcao == '4':
            remover_professor()
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()