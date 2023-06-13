from __future__ import annotations
from antlr4 import *
from lcLexer import lcLexer
from lcParser import lcParser
from lcVisitor import lcVisitor
from dataclasses import dataclass
import string

# conjunt de lletres de l'abecedari per saber quines no estan utilitzades a l'hora de fer la alfa conversió
lista_letras = list(string.ascii_lowercase)
# llista de macros
llista_macros = dict()


@dataclass
class Variable:
    valor: str


@dataclass
class Abstraccion:
    var: Variable
    term: Arbre


@dataclass
class Applicacion:
    left: Arbre
    right: Arbre


Arbre = Variable | Abstraccion | Applicacion


# funció que retorna un string donada una expressió de lambda càlcul en format Arbre
def getArbol(a: Arbre) -> str:
    arbol = ''
    match a:
        case Variable(val):
            arbol += str(val)
        case Abstraccion(var, term):
            arbol += '(λ' + getArbol(var) + '.' + getArbol(term) + ')'
        case Applicacion(term1, term2):
            arbol += '(' + getArbol(term1) + getArbol(term2) + ')'
    return arbol


# funció encarregada de fer Beta Conversions
def evalBetaArbre(a: Arbre) -> Arbre:
    match a:
        case Variable(_):
            return a

        case Abstraccion(var, term):
            return Abstraccion(var, evalBetaArbre(term))

        case Applicacion(term1, term2):
            # cas en el que es pot fer una Beta reducció
            if isinstance(term1, Abstraccion):
                print('β-reducció:')
                print(getArbol(a) + ' -> ', end="")
                # substitut substitueix en term1 les aparicions de term1.var per el term2
                subs = substitut(term1, term1.var, term2)
                print(getArbol(subs))
                return subs
            else:
                return Applicacion(evalBetaArbre(term1), evalBetaArbre(term2))


# funció que retorna True si es pot fer una Beta reducció
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


# funció encarregada de substiuir els elements en la Beta reducció
def substitut(a: Arbre, antic: Variable, nou: Arbre) -> Arbre:
    match a:
        case Variable(val):
            # si la variable actual és igual a la que tenim guardada l'hem de substituir
            if str(val) == str(antic.valor):
                return nou
            else:
                return Variable(val)

        case Abstraccion(var, term):
            # si la variable de l'abstracció és igual a la guardada, l'eliminem
            if var == antic:
                return substitut(term, antic, nou)
            else:
                return Abstraccion(var, substitut(term, antic, nou))

        case Applicacion(term1, term2):
            return Applicacion(substitut(term1, antic, nou), substitut(term2, antic, nou))


# funció que donat un arbre retorna un amb una alfa conversió
def alfaConver(a: Arbre) -> Arbre:
    # llista de les variables usades en l'arbre, utilitzat per detectar col.lisions entre variables
    used_variables = set()
    used_variables.add("no_empty")

    def convert(a: Arbre) -> Arbre:
        nonlocal used_variables

        match a:
            case Variable(_):
                return a

            case Abstraccion(var, term):
                # si la variable de l'abstracció ja estava al diccionari cal canviar-la
                if str(var.valor) in used_variables:
                    print('α-conversió: ', end="")
                    print(str(var.valor) + ' -> ', end="")
                    # generem una nova variable, que no estigui usada
                    new_var = novaVar(used_variables)
                    used_variables.add(new_var)
                    print(new_var)
                    print(getArbol(a) + ' -> ', end="")
                    # utilitzem la mateixa funció que en la Beta reducció per substituir les anteriors variables per les noves
                    alfa = Abstraccion(Variable(new_var), substitut(
                        term, var, Variable(new_var)))
                    print(getArbol(alfa))
                    return alfa
                else:
                    # si la variable no estava utilitzada, l'afegim al conjunt
                    used_variables.add(str(var.valor))
                    return Abstraccion(var, convert(term))

            case Applicacion(term1, term2):
                # si el terme 2 és una variable també l'afegim al conjunt de variables utilitzades
                if isinstance(term1, Abstraccion) and isinstance(term2, Variable):
                    used_variables.add(str(term2.valor))

                return Applicacion(convert(term1), convert(term2))

    return convert(a)


# funció destinada a crear una variable que no estigui utilitzada
def novaVar(used_variables: set[str]) -> str:
    n = len(lista_letras)
    ll = lista_letras
    while True:
        i = 0
        while i < n:
            # iterem per totes les lletres del diccionari fins a trobar una que no estigui utilitzada
            new_var = ll[i]
            if new_var not in used_variables:
                return new_var
            i += 1
        # no hem trobat cap lletra empty, provem amb una llista amb les lletres i un '
        ii = 0
        ll2 = []
        while ii < n:
            ll2.append(ll[ii]+'\'')
            ii += 1
        ll = ll2


# retorna true si l'arbre requereix d'una alfa conversió, similar en estructura a la funció alfaConver
def needAlfa(a: Arbre) -> Arbre:
    used_variables = set()
    used_variables.add("no_empty")

    def convert(a: Arbre) -> Arbre:
        nonlocal used_variables

        match a:
            case Variable(_):
                return False

            case Abstraccion(var, term):

                if str(var.valor) in used_variables:
                    return True
                else:
                    used_variables.add(str(var.valor))
                    return convert(term)

            case Applicacion(term1, term2):
                if isinstance(term1, Abstraccion) and isinstance(term2, Variable):
                    used_variables.add(str(term2.valor))

                return convert(term1) or convert(term2)

    return convert(a)


# visitador de l'arbre
class TreeVisitor(lcVisitor):

    def visitRoot(self, ctx):
        a = self.visitChildren(ctx)
        return a

    def visitAbstraccio(self, ctx):
        parametres = list(ctx.getChildren())
        n_parametres = len(parametres)
        term = parametres[n_parametres-1]
        variables = parametres[1:n_parametres-2]
        b = len(variables)-1
        # com podem tenir λxyz... hem de crear una abstracció recursiva (λx.(λy.(λz.TERME)))
        # la primera abstracció, la més interna, serà l'ultima variable amb el terme (λz.TERME)
        x = Abstraccion(Variable(variables[b]), self.visit(term))
        # per la resta d'abstraccions fem un recorregut invers de la llista de variables
        # creem una abstracció de la variable amb l'abstracció anterior
        for i in range(b-1, -1, -1):
            x = Abstraccion(Variable(variables[i]), x)
        return x

    def visitAplicacio(self, ctx):
        [term1, term2] = list(ctx.getChildren())
        strin = str(ctx.getChild(1).getChild(0))
        # si el fill 2 és un símbol no alfanumèric cal invertir l'ordre dels termes, notació infixa
        # les condicions per tal que això passi són:
        # length de terme2 = 1, no alfanumeric, no parèntesis (podria detectar l'inici de una expressió com a símbol infix), no '\' i no λ
        if (len(strin) == 1 and not strin.isalpha() and strin != '(' and strin != '\u005C' and strin != 'λ'):
            return Applicacion(self.visit(term2), self.visit(term1))
        else:
            return Applicacion(self.visit(term1), self.visit(term2))

    def visitParentesis(self, ctx):
        [_, exp, _] = list(ctx.getChildren())
        return self.visit(exp)

    def visitLletra(self, ctx):
        [ll] = list(ctx.getChildren())
        x = Variable(ll.getText())
        return x

    def visitAssignacio(self, ctx):
        [nom, _, arbre] = list(ctx.getChildren())
        # guardem l'arbre a la lllista de macros
        llista_macros[str(nom)] = self.visit(arbre)
        # retornem un booleà per diferenciar una assignació d'una lambda expressió normal en el Main
        return True

    def visitMacro(self, ctx):
        var = str(ctx.getChild(0))
        return llista_macros[var]

    def visitCalcul(self, ctx):
        return self.visitChildren(ctx)


# "Main"
while True:
    input_stream = InputStream(input('? '))
    lexer = lcLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = lcParser(token_stream)
    tree = parser.root()

    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = TreeVisitor()
        a = visitor.visit(tree)

        match a:
            # cas d'una assignació de macro
            case True:
                # imprimim la llista de macros
                for i in llista_macros:
                    print(i + " ≡ " + getArbol(llista_macros[i]))

            # cas d'analisi d'una expressió
            case _:
                print('Arbre:')
                print(getArbol(a))

                # alfa, mentres requereixi d'una alfa conversió, la fem
                while needAlfa(a):
                    a = alfaConver(a)

                # beta, si pot fer una beta reducció, la fem
                # no es posa directament el while ja que podem tenir el cas d'una beta reducció infinita
                if potFerBeta(a):
                    b = evalBetaArbre(a)
                    exited = 0  # paràmetre que ens servirà per veure si estem en un bucle infinit
                    while (potFerBeta(b)):
                        ast = getArbol(a)
                        bst = getArbol(b)
                        # comparem els tamanys de l'arbre per valorar si la possibilitat del bucle infinit de reduccions
                        if len(ast) == len(bst):
                            exited = 1
                            break
                        else:
                            # no tenim bucle, continuem
                            a = b
                            b = evalBetaArbre(b)

                    # si hem trobat un bucle infinit
                    if exited:
                        print('...')
                        print('Resultat:')
                        print('Nothing')
                    # si no podem aplicar més beta reduccions
                    else:
                        print('Resultat:')
                        print(getArbol(b))

    else:
        print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
        print(tree.toStringTree(recog=parser))
