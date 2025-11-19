gramatica = [
    ("S", ["stmt_list"]),
    ("stmt_list", ["stmt_list", "stmt"]),
    ("stmt_list", ["stmt"]),
    ("stmt", ["assign"]),
    ("stmt", ["if_stmt"]),
    ("stmt", ["while_stmt"]),
    ("stmt", ["func_call"]),
    ("stmt", ["expr"]),
    ("assign", ["id", "=", "expr"]),
    ("if_stmt", ["if", "(", "expr", ")", "{", "stmt_list", "}"]),
    ("if_stmt", ["if", "(", "expr", ")", "{", "stmt_list", "}", "else", "{", "stmt_list", "}"]),
    ("while_stmt", ["while", "(", "expr", ")", "{", "stmt_list", "}"]),
    ("expr", ["expr", "or", "and_expr"]),
    ("expr", ["and_expr"]),
    ("and_expr", ["and_expr", "and", "not_expr"]),
    ("and_expr", ["not_expr"]),
    ("not_expr", ["not", "not_expr"]),
    ("not_expr", ["comp_expr"]),
    ("comp_expr", ["comp_expr", "==", "arith"]),
    ("comp_expr", ["comp_expr", "!=", "arith"]),
    ("comp_expr", ["comp_expr", "<", "arith"]),
    ("comp_expr", ["comp_expr", ">", "arith"]),
    ("comp_expr", ["comp_expr", "<=", "arith"]),
    ("comp_expr", ["comp_expr", ">=", "arith"]),
    ("comp_expr", ["arith"]),
    ("arith", ["arith", "+", "term"]),
    ("arith", ["arith", "-", "term"]),
    ("arith", ["term"]),
    ("term", ["term", "*", "factor"]),
    ("term", ["term", "/", "factor"]),
    ("term", ["factor"]),
    ("factor", ["num"]),
    ("factor", ["id"]),
    ("factor", ["func_call"]),
    ("factor", ["(", "expr", ")"]),
    ("factor", ["list"]),
    ("factor", ["tuple"]),
    ("factor", ["-", "factor"]),
    ("factor", ["+", "factor"]),
    ("func_call", ["id", "(", "arg_list", ")"]),
    ("arg_list", ["expr"]),
    ("arg_list", ["arg_list", ",", "expr"]),
    ("arg_list", ["ε"]),
    ("list", ["[", "list_items", "]"]),
    ("list_items", ["expr"]),
    ("list_items", ["list_items", ",", "expr"]),
    ("list_items", ["ε"]),
    ("tuple", ["(", "tuple_items", ")"]),
    ("tuple_items", ["expr"]),
    ("tuple_items", ["tuple_items", ",", "expr"]),
    ("tuple_items", ["ε"]),
]


class ASTNode:
    def __init__(self, tipo, hijos=None, valor=None, datatype=None):
        self.tipo = tipo
        self.hijos = hijos if hijos else []
        self.valor = valor
        self.datatype = datatype


class SymbolTable:
    def __init__(self):
        self.table = {}

    def detect_type(self, value):
        if value.isdigit():
            return "entero"
        if value.replace(".", "", 1).isdigit():
            return "real"
        if value.startswith("[") and value.endswith("]"):
            return "lista"
        if value.startswith("(") and value.endswith(")"):
            return "tupla"
        return "desconocido"

    def add(self, name, value):
        tipo = self.detect_type(value)
        self.table[name] = {"valor": value, "tipo": tipo}

    def __repr__(self):
        out = ""
        for k, v in self.table.items():
            out += f"{k:10}  valor={v['valor']:10}  tipo={v['tipo']}\n"
        return out.strip()


symbol_table = SymbolTable()
temp_count = 0
code3d = []


def nuevo_temp():
    global temp_count
    t = f"t{temp_count}"
    temp_count += 1
    return t


def imprimir_ast(nodo, indent="", ultimo=True):
    rama = "└── " if ultimo else "├── "
    print(indent + rama + f"{nodo.tipo}  valor={nodo.valor}  tipo={nodo.datatype}")
    indent += "    " if ultimo else "│   "
    for i, h in enumerate(nodo.hijos):
        imprimir_ast(h, indent, i == len(nodo.hijos) - 1)


# ========= PARSING SIMPLE (SIN CAMBIAR TU LÓGICA) =========

def evaluar_expresion(expr):
    try:
        return str(eval(expr))
    except:
        return expr  # si no se puede evaluar, se deja igual


def parse_asignacion(tokens):
    if len(tokens) >= 3 and tokens[1] == "=":
        var = tokens[0]
        expr = " ".join(tokens[2:])

        valor_eval = evaluar_expresion(expr)

        symbol_table.add(var, valor_eval)

        t = nuevo_temp()
        code3d.append(f"{t} = {expr}")
        code3d.append(f"{var} = {t}")

        nodo = ASTNode("assign", valor=f"{var}={expr}", datatype="asignación")
        nodo.hijos.append(ASTNode("id", valor=var, datatype=symbol_table.table[var]["tipo"]))
        nodo.hijos.append(ASTNode("expr", valor=expr, datatype=symbol_table.table[var]["tipo"]))
        return nodo
    return None


def parse_expresion(tokens):
    expr = " ".join(tokens)
    t = nuevo_temp()
    code3d.append(f"{t} = {expr}")
    return ASTNode("expr", valor=expr, datatype="desconocido")


def construir_AST(linea):
    tokens = linea.split()
    nodo = parse_asignacion(tokens)
    if nodo:
        return nodo
    return parse_expresion(tokens)


# ================== EJECUCIÓN ==================

print("Ingresa instrucciones (enter vacío para terminar):")

ast_list = []

while True:
    linea = input("> ").strip()
    if linea == "":
        break
    ast_list.append(construir_AST(linea))

print("\n========== ÁRBOL AST DECORADO ==========")
for n in ast_list:
    imprimir_ast(n)
    print()

print("========== TABLA DE SÍMBOLOS ==========")
print(symbol_table)

print("========== CÓDIGO 3 DIRECCIONES ==========")
for c in code3d:
    print(c)
