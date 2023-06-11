from __future__ import annotations
from antlr4 import *
from achurchLexer import achurchLexer
from achurchParser import achurchParser
from achurchVisitor import achurchVisitor
from dataclasses import dataclass
import string

lista_letras = string.ascii_lowercase

@dataclass
class Variable:
    valor: str
    
@dataclass
class Abstraccion:
    var: Variable #string
    term: Arbre
    
@dataclass
class Applicacion:
    left: Arbre
    right: Arbre

Arbre = Variable | Abstraccion | Applicacion

def getArbol(a: Arbre) -> str:
    arbol = ''
    match a:
        case Variable(val):
            arbol +=str(val)    
        case Abstraccion(var, term):
            arbol+= '(λ' + getArbol(var) + '.' + getArbol(term) + ')'
        case Applicacion(term1, term2):
            arbol += '(' + getArbol(term1) + getArbol(term2) + ')'
    return arbol

def evalBetaArbre(a: Arbre) -> Arbre:
    match a:
        case Variable(_):

            return a
        
        case Abstraccion(var, term):

            return Abstraccion(var, evalBetaArbre(term))
        
        case Applicacion(term1, term2):
            if isinstance(term1, Abstraccion):

                return substitut(term1, term1.var, term2)
            else:

                return Applicacion(evalBetaArbre(term1), evalBetaArbre(term2))

def potFerBeta(a: Arbre) -> bool:
    match a:
        case Variable(_):
            return False       
        case Abstraccion(_, term):
            return potFerBeta(term)      
        case Applicacion(term1, term2):
            if isinstance(term1, Abstraccion):
                return True
            else:
                return potFerBeta(term1) or potFerBeta(term2)



def substitut(a: Arbre, antic: Variable, nou: Arbre) -> Arbre:
    match a:
        case Variable(val):
            
            if str(val) == str(antic.valor):
                return nou
            else: return Variable(val)
            
        case Abstraccion(var, term):
            if var == antic:
        
                return substitut(term,antic,nou)
            else:
                
                return Abstraccion(var, substitut(term,antic,nou))
        case Applicacion(term1, term2):

            return Applicacion(substitut(term1,antic,nou),substitut(term2,antic,nou))


#################################
#################################
#################################
#################################

def alphaConversionSelective(a: Arbre) -> Arbre:
    used_variables = set()  # Conjunto de variables ligadas utilizadas hasta el momento
    used_variables.update(termes_aillats(a))
    #print(used_variables)
    def convert(a: Arbre) -> Arbre:
        nonlocal used_variables
        #print(used_variables)
        match a:
            case Variable(val):
                return a

            case Abstraccion(var, term):
                #print(var.valor)
                if str(var.valor) in used_variables:
                    print(str(var.valor) + ' -> ', end="")
                    new_var = generateFreshVariable(used_variables)  # Generar una nueva variable fresca
                    used_variables.add(new_var)  # Agregar la nueva variable al conjunto de variables ligadas
                    print(new_var)
                    # Realizar la conversión alfa reemplazando la variable ligada por la nueva variable fresca
                    return Abstraccion(Variable(new_var),substitut(term, var, Variable(new_var)))
                else:
                    #print('pruebo')
                    #print(used_variables)
                    used_variables.add(str(var.valor))  # Agregar la variable ligada al conjunto de variables ligadas
                    #print(used_variables)
                    # Realizar la conversión alfa en el término recursivamente
                    return Abstraccion(var, convert(term))

            case Applicacion(term1, term2):
                return Applicacion(convert(term1), convert(term2))

    return convert(a)


def termes_aillats(a: Arbre) -> set[str]:
    """
    Obtiene las variables ligadas en un árbol de términos.
    """
    variables = set()

    match a:
        case Variable(_):
            pass

        case Abstraccion(var, term):
            #variables.add(var.valor)
            variables.update(termes_aillats(term))

        case Applicacion(term1, term2):
            if isinstance(term1, Abstraccion) and isinstance(term2, Variable):
                variables.add(term2.valor) #nomes afegim els termes que s'aplicaràn en beta conversions
                variables.update(termes_aillats(term1))
            else:
                variables.update(termes_aillats(term1))
                variables.update(termes_aillats(term2))

    return variables



def generateFreshVariable(used_variables: set[str]) -> str:
    """
    Genera una nueva variable fresca que no está en el conjunto de variables utilizadas.
    """
    i = 0
    while True:
        #print(i)
        i = i % 26
        new_var = lista_letras[i]
        if new_var not in used_variables:
            return new_var
        i += 1

def needAlfa(a: Arbre) -> bool:
    used_variables = set()  # Conjunto de variables ligadas utilizadas hasta el momento
    used_variables.update(termes_aillats(a))
    
    arbre_en_string = getArbol(a)
    i = 0
    for i in range (0, len(arbre_en_string)-1):
        if arbre_en_string[i] == 'λ' and arbre_en_string[i+1] in used_variables: return True
        else: used_variables.add(arbre_en_string[i+1])
    return False


#################################
#################################
#################################
#################################

class TreeVisitor(achurchVisitor):
        
        def visitRoot(self, ctx):
            a = self.visitChildren(ctx)
            #print('Arbre:') 
            #print(getArbol(a))
            return a
        
        def visitAbstraccio(self, ctx):
            parametres = list(ctx.getChildren())
            n_parametres = len(parametres)
            term = parametres[n_parametres-1]
            variables = parametres[1:n_parametres-2]
            b = len(variables)-1
            
            x = Abstraccion(Variable(variables[b]),self.visit(term))
            for i in range(b-1,-1,-1):
                x = Abstraccion(Variable(variables[i]),x)
            return x
             
        def visitAplicacio(self, ctx):
            [term1, term2] = list(ctx.getChildren())
            x = Applicacion(self.visit(term1),self.visit(term2))
            return x
        
        def visitParentesis(self, ctx):
            [_, exp, _] = list(ctx.getChildren())
            return self.visit(exp)
        
        def visitLletra(self, ctx):
            [ll] = list(ctx.getChildren())
            x = Variable(ll.getText())
            return x
    
    
while True:
    input_stream = InputStream(input('? '))
    lexer = achurchLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = achurchParser(token_stream)
    tree = parser.root()

    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = TreeVisitor()
        a = visitor.visit(tree)
        print('Arbre:') 
        print(getArbol(a))
        
        #alfa
        while needAlfa(a):
            print('α-conversió: ', end="")
            b = alphaConversionSelective(a)
            print(getArbol(a) + ' -> ' + getArbol(b))  
            a = b
            
        # beta
        b = evalBetaArbre(a)
        print('β-reducció:') 
        print(getArbol(a) + ' -> ' + getArbol(b))
        exited = 0
        while(potFerBeta(b)):
            ast = getArbol(a)
            bst = getArbol(b)
            if len(ast) == len(bst): 
                exited = 1
                break
            else:
                a = b
                b = evalBetaArbre(b)
                print('β-reducció:') 
                print(getArbol(a) + ' -> ' + getArbol(b))
        if exited:
            print('...')
            print('Resultat:')
            print('Nothing')
        else:
            print('Resultat:')
            print(getArbol(b))
            #parem quan la size de la expresio anterior sigui igual a la seguent
    else:
        print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
        print(tree.toStringTree(recog=parser))


