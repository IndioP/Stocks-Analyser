import random
import string

structure = {
    "Tipo da peça":         [],
    "Dificuldade":          [],
    "Quantidade":           [],
    "Custo de produção":    [],
    "Peças para costurar":  [],
    "Preço":                []
}

CLICKED = True
SHOW_ADD_PRODUCTS_SESSION = False
random_id = lambda N: ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

