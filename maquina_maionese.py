class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    # Função para que node_to_string seja chamado sempre que utilizar um print(node)
    def __str__(self):
        return node_to_string(self)

# Função para imprimir os elementos da tree, em pré-ordem (raiz, esquerda, direita)
def node_to_string(node):
    if not node:
        return "None"
    left_str = node_to_string(node.left)
    right_str = node_to_string(node.right)
    return f"({node.key}, {left_str}, {right_str})"

class Tree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            return Node(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    # Função utilizado para chamar node_to_string sempre que fizer um print(tree)
    def __str__(self):
        return node_to_string(self.root)

class HashTable:
    def __init__(self, size=29):
        self.size = size
        self.slots = [Tree() for _ in range(size)]
        
    def hash(self, s):
        mult = 1
        hash_value = 0
        for c in s:
            hash_value += mult * ord(c)
            mult += 1
        return hash_value
        
    def put(self, key, value):
        hv = self.hash(key) % self.size
        self.slots[hv].insert(key, value)
    
    def get_recipe(self, key):
        hv = self.hash(key) % self.size
        node = self.slots[hv].search(key)

        print(key)
        if node is None:
            print("Não encontrado")
        else:
            for ingr, qty in node.value:
                print(f"{ingr} {qty}")

    def get_item(self, key):
        print(key)
        hv = self.hash(key) % self.size
        node = self.slots[hv].search(key)
        if node is None:
            print("Não encontrado")
        else:
            for recipe in node.value:
                print(recipe)


    def print_all(self):
        for tree in self.slots:
            if tree.root is not None:
                print(tree)
            else:
                print('None')

def load_recipes_from_file(filename, recipes_ht, items_ht):

    # Lê um arquivo de receitas formatado em blocos:
    #   - Nome da receita em uma linha
    #   - N linhas de "ingrediente quantidade"
    #   - Linha em branco separando receitas

    # Atualiza duas tabelas hash:
    #   - recipes_ht: chave: receita -> valor: lista de (ingrediente, quantidade)
    #   - items_ht: chave: ingrediente (item) -> valor: lista de receitas

    with open(filename, 'r', encoding='utf-8') as f:
        # lê todo o arquivo linha por linha e remove quebras de linha
        lines = f.read().splitlines()

    i = 0
    while i < len(lines):
        # pula linhas em branco
        if not lines[i].strip():
            i += 1
            continue
         
        # utiliza .strip() para tirar espaços indesejados 
        recipe_name = lines[i].strip()
        # Avança o contador para ler os ingredientes 
        i += 1 

        ingredients = []
        # Repete até chegar no final do arquivo ou encontrar uma linha vazia
        while i < len(lines) and lines[i].strip(): 
            parts = lines[i].rsplit(' ', 1) # Separa a linha em ingrediente e quantidade
            ingr_name = parts[0].strip() 
            ingr_qty = int(parts[1]) 
            ingredients.append([ingr_name, ingr_qty]) 
            i += 1

        recipes_ht.put(recipe_name, ingredients) 

        for ingredient, _ in ingredients:
            hv = items_ht.hash(ingredient) % items_ht.size
            node = items_ht.slots[hv].search(ingredient)
            if node is None:
                items_ht.put(ingredient, [recipe_name]) 
            else:
                node.value.append(recipe_name)  
        # Pula a linha em branco que separa cada "bloco" de receitas
        i += 1

def main():
    recipes = HashTable()
    items = HashTable()

    load_recipes_from_file("./craft.txt", recipes, items)

    # Loop principal para ler os comandos do usuário 
    while True:
        command = input().strip()
        if not command:
            continue

        # Divide o input do usuário em 2 partes 
        # para que o programa possa verificar os comandos digitados através da sequência de if/elif/else
        parts = command.split(' ', 1)
        cmd = parts[0].lower()

        if cmd == 'q':
            break

        elif cmd == 'p':
            if len(parts) < 2: 
                print("Comando inválido. Use 'p r' para imprimir as receitas, ou 'p i' para imprimir os itens.")
                continue

            subcmd = parts[1].lower()
            if subcmd == 'r':
                recipes.print_all()
            elif subcmd == 'i':
                items.print_all()
            else:
                print("Comando inválido. Use 'p r' para receitas ou 'p i' para itens.")

        elif cmd == 'r':
            if len(parts) < 2:
                print("Receita não especificada. Use: r <nome_da_receita>") 
                continue
            recipe_name = parts[1]
            recipes.get_recipe(recipe_name)

        elif cmd == 'i':
            if len(parts) < 2:
                print("Item não especificado. Use: i <nome_do_item>")
                continue
            item_name = parts[1]
            items.get_item(item_name)

        else:
            print("Comando inválido. Use:")
            print("  p r -> imprime todas as receitas")
            print("  p i -> imprime todos os itens")
            print("  r <nome> -> imprime receita específica")
            print("  i <item> -> imprime receitas que usam o item")
            print("  q -> sair")

if __name__ == "__main__":
    main()
