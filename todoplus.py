import redis
import json

db = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

def adicionar_tarefa(descricao: str):
    tarefa_id = db.incr("next_id")

    tarefa = {
        "id": tarefa_id,
        "descricao": descricao,
        "concluida": False
    }

    db.hset("tarefas_plus", tarefa_id, json.dumps(tarefa))
    print(f"Tarefa adicionada (ID: {tarefa_id})")


def listar_tarefas():
    tarefas = db.hgetall("tarefas_plus")

    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    print("\n------- Todas as Tarefas --------")
    for id, dados in tarefas.items():
        tarefa = json.loads(dados)
        status = "Concluída" if tarefa["concluida"] else "Pendente"
        print(f"{tarefa['id']} : {tarefa['descricao']} - {status}")


def concluir_tarefa(tarefa_id):
    dados = db.hget("tarefas_plus", tarefa_id)

    if not dados:
        print("Tarefa não encontrada.")
        return

    tarefa = json.loads(dados)
    tarefa["concluida"] = True

    db.hset("tarefas_plus", tarefa_id, json.dumps(tarefa))
    print(f"Tarefa {tarefa_id} marcada como concluída.")


def remover_tarefa(tarefa_id):
    if db.hdel("tarefas_plus", tarefa_id):
        print(f"Tarefa {tarefa_id} removida.")
    else:
        print("Tarefa não encontrada.")


def listar_pendentes():
    tarefas = db.hgetall("tarefas_plus")

    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    print("\n------- Tarefas Pendentes --------")
    encontrou = False

    for id, dados in tarefas.items():
        tarefa = json.loads(dados)
        if not tarefa["concluida"]:
            encontrou = True
            print(f"{tarefa['id']} : {tarefa['descricao']} - Pendente")

    if not encontrou:
        print("Nenhuma tarefa pendente.")


def listar_concluidas():
    tarefas = db.hgetall("tarefas_plus")

    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    print("\n------- Tarefas Concluídas --------")
    encontrou = False

    for id, dados in tarefas.items():
        tarefa = json.loads(dados)
        if tarefa["concluida"]:
            encontrou = True
            print(f"{tarefa['id']} : {tarefa['descricao']} - Concluída")

    if not encontrou:
        print("Nenhuma tarefa concluída.")


def menu():
    while True:
        print("\n1 - Adicionar Tarefa")
        print("2 - Listar Todas")
        print("3 - Concluir Tarefa")
        print("4 - Remover Tarefa")
        print("5 - Listar Pendentes")
        print("6 - Listar Concluídas")
        print("0 - Sair")

        opcao = input("Escolha uma opção (0-6): ")

        match opcao:
            case "1":
                tarefa = input("Digite uma tarefa: ")
                adicionar_tarefa(tarefa)

            case "2":
                listar_tarefas()

            case "3":
                listar_tarefas()
                tarefa_id = input("ID da tarefa: ")
                concluir_tarefa(tarefa_id)

            case "4":
                listar_tarefas()
                tarefa_id = input("ID da tarefa: ")
                remover_tarefa(tarefa_id)

            case "5":
                listar_pendentes()

            case "6":
                listar_concluidas()

            case "0":
                print("Saindo...")
                break

            case _:
                print("Opção inválida.")


menu()
