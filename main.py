from fastapi import FastAPI

app = FastAPI()

vendas = {
    1: {"item": "garrafa 2l", "preco_unitário": 9, "quantidade": 3},
    2: {"item": "garrafa 1.5l", "preco_unitário": 8, "quantidade": 6},
    3: {"item": "lata 350ml", "preco_unitário": 3.9, "quantidade": 4},
    4: {"item": "garrafa 600ml", "preco_unitário": 5, "quantidade": 11},
}

@app.get("/")
def home():
    return {"Vendas": len(vendas)}