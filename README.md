# Informe del Compilador Simple

## 1. Gramática  
La gramática define la estructura del lenguaje que el compilador puede reconocer. Controla la forma correcta de las instrucciones, expresiones, listas, tuplas y estructuras de control.

```python
S → stmt_list
stmt_list → stmt_list stmt | stmt
stmt → assign | if_stmt | while_stmt | func_call | expr
assign → id = expr
if_stmt → if ( expr ) { stmt_list }
if_stmt → if ( expr ) { stmt_list } else { stmt_list }
while_stmt → while ( expr ) { stmt_list }
expr → expr or and_expr | and_expr
and_expr → and_expr and not_expr | not_expr
not_expr → not not_expr | comp_expr
comp_expr → comp_expr == arith | comp_expr != arith | comp_expr < arith | comp_expr > arith | comp_expr <= arith | comp_expr >= arith | arith
arith → arith + term | arith - term | term
term → term * factor | term / factor | factor
factor → num | id | func_call | ( expr ) | list | tuple | -factor | +factor
func_call → id ( arg_list )
arg_list → expr | arg_list , expr | ε
list → [ list_items ]
list_items → expr | list_items , expr | ε
tuple → ( tuple_items )
tuple_items → expr | tuple_items , expr | ε
```

---

## 2. AST Decorado  
El compilador genera un Árbol de Sintaxis Abstracta (AST) en el que cada nodo contiene:  
- El tipo (assign, expr, id, etc.)  
- El valor asociado  
- El tipo de dato inferido  

Esto permite representar la lógica interna del programa de forma jerárquica.

```python
└── assign (x=3, tipo=asignación)
    ├── id (x, tipo=entero)
    └── expr (3, tipo=entero)
```

---

## 3. Tabla de Símbolos  
La tabla de símbolos guarda los identificadores que aparecen en el programa, junto con su valor y el tipo inferido por el compilador.

```python
x: valor=3  tipo=entero
y: valor=3*x+4  tipo=desconocido
```

Esto ayuda en análisis semántico y futuras validaciones de tipos.

---

## 4. Código Intermedio de Tres Direcciones  
El compilador transforma las expresiones en una secuencia de instrucciones simples usando temporales.  
Esto facilita optimización o traducción a código máquina.

```python
t0 = 3
x = t0
t1 = 3 * x + 4
y = t1
```

---

## 5. Conclusión  
Este compilador simple implementa las etapas fundamentales de análisis:  
- Usa una **gramática consistente** para validar la estructura del código.  
- Construye un **AST decorado** que refleja la semántica del programa.  
- Gestiona una **tabla de símbolos** con tipos inferidos.  
- Produce **código intermedio 3D**, listo para posteriores fases del compilador.  

En conjunto, constituye una base funcional y extensible para continuar desarrollando un compilador más completo.
