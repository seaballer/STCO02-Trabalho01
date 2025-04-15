
class BSTNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def insert(self, key, value):
        if key < self.key:
            if self.left: self.left.insert(key, value)
            else: self.left = BSTNode(key, value)
        elif key > self.key:
            if self.right: self.right.insert(key, value)
            else: self.right = BSTNode(key, value)
        else:
            self.value = value  # update if already exists

    def find(self, key):
        if key == self.key:
            return self.value
        elif key < self.key and self.left:
            return self.left.find(key)
        elif key > self.key and self.right:
            return self.right.find(key)
        return None

    def preorder(self):
        left = self.left.preorder() if self.left else "None"
        right = self.right.preorder() if self.right else "None"
        return f"({self.key}, {left}, {right})"

class HashTable:
    def __init__(self):
        self.size = 29
        self.table = [None] * self.size

    def hash(self, s):
        mult = 1
        hash_value = 0
        for c in s:
            hash_value += mult * ord(c)
            mult += 1
        return hash_value % self.size

    def insert(self, key, value):
        idx = self.hash(key)
        if self.table[idx] is None:
            self.table[idx] = BSTNode(key, value)
        else:
            self.table[idx].insert(key, value)

    def find(self, key):
        idx = self.hash(key)
        if self.table[idx] is None:
            return None
        return self.table[idx].find(key)

    def print_table(self):
        for node in self.table:
            print(node.preorder() if node else "None")

receitas_table = HashTable()
itens_table = HashTable()

with open("craft.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

i = 0
while i < len(lines):
    receita = lines[i]
    i += 1
    ingredientes = []
    while i < len(lines) and not lines[i][0].isalpha():
        item, qtde = lines[i].rsplit(" ", 1)
        ingredientes.append((item, int(qtde)))
        i += 1

    receitas_table.insert(receita, ingredientes)

    for item, _ in ingredientes:
        lst = itens_table.find(item)
        if lst is None:
            itens_table.insert(item, [receita])
        else:
            if receita not in lst:
                lst.append(receita)

while True:
    try:
        cmd = input()
        if cmd == 'q':
            break
        elif cmd.startswith("r "):
            nome = cmd[2:]
            resultado = receitas_table.find(nome)
            print(nome)
            if resultado:
                for item, qtde in resultado:
                    print(f"{item} {qtde}")
            else:
                print("Não encontrado.")
        elif cmd.startswith("i "):
            nome = cmd[2:]
            resultado = itens_table.find(nome)
            print(nome)
            if resultado:
                for receita in resultado:
                    print(receita)
            else:
                print("Não encontrado.")
        elif cmd == "p r":
            receitas_table.print_table()
        elif cmd == "p i":
            itens_table.print_table()
    except EOFError:
        break
