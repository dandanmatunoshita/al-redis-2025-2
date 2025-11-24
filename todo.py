import redis

db = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

def adicionar_tarefa(tarefa: str):
    db.lpush("todo", tarefa)
    print(f"Tarefa adicionada: {tarefa}")

def listar_tarefas():
    tarefas = db.lrange("todo", 0, -1)
    if not tarefas:
        print("Nenhuma tarefa encontrada")
        return
    else:
        print("\n------ Lista de Tarefas -------")
        for k, v in enumerate(tarefas, start=1):
            print(f"{k}: {v}")
        print("--------------------------------")

def remover_tarefa(numero: int):
    tarefas = db.lrange("todo", 0, -1)
    if numero < 1 or numero > len(tarefas):
        print("Número inválido")
        return
    else:
        tarefa = tarefas[numero - 1]
        db.lrem("todo", 0, tarefa)  # remove todas as ocorrências
        print(f"Tarefa removida: {tarefa}")

def menu():
    while True:
        print("\n1 - Adicionar Tarefa")
        print("2 - Listar Tarefas")
        print("3 - Remover Tarefa")
        print("0 - Sair")
        opcao = input("Escolha uma opção (0-3): ")

        match opcao:
            case "1":
                tarefa = input("Digite uma tarefa: ")
                adicionar_tarefa(tarefa)
            case "2":
                listar_tarefas()
            case "3":
                listar_tarefas()
                num = int(input("Número da tarefa para remover: "))
                remover_tarefa(num)
            case "0":
                print("Saindo...")
                break
            case _:
                print("Opção inválida")


menu()
