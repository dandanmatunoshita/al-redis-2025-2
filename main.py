import redis

db = redis.Redis(
    host = "localhost",
    port = 6379,
    db = 0,
    decode_responses = True
)

db.set("professor","Marco")

valor = db.get("professor")

print("Valor armazenado: ", valor)