from __future__ import annotations
from antlr4 import *
from achurchLexer import achurchLexer
from achurchParser import achurchParser
from achurchVisitor import achurchVisitor
from dataclasses import dataclass
import string

import pydot
# importa l'API de Telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


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
# llista de "print" que es faran a la funció Main un cop s'acabi l'execució d'una instrucció
# s'han eliminat els prints a les funcions, i es fa només un append del que s'hauria d'imprimir,
# per tal de no haver de passar context i update a cada funció
pasos = []


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
                # substitut substitueix en term1 les aparicions de term1.var per el term2
                subs = substitut(term1, term1.var, term2)
                # afegim un pas a la llista
                pasos.append(getArbol(a) + '-> β ->' + getArbol(subs))
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
                    # generem una nova variable, que no estigui usada
                    new_var = novaVar(used_variables)
                    used_variables.add(new_var)
                    # utilitzem la mateixa funció que en la Beta reducció per substituir les anteriors variables per les noves
                    alfa = Abstraccion(Variable(new_var), substitut(
                        term, var, Variable(new_var)))
                    # afegim un pas a la llista
                    pasos.append(getArbol(a) + '-> α ->' + getArbol(alfa))
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
class TreeVisitor(achurchVisitor):

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


# funció que donat un arbre crea una imatge en el directori de l'arbre
def crea_imatge(a: Arbre):
    # digraph per obtenir fletxes, en comptes de edges normals
    graph = pydot.Dot('arbre', graph_type='digraph', gbcolor='white')

    # funció creadora de nodes i edges
    # retorna un str que servirà per identificar al fill i que el pare pugui crerar l'aresta amb ell
    def visit(arb: Arbre, id: str) -> str:
        match arb:
            case Abstraccion(var, term):
                # l'id del node és l'id del pare 'id' més el valor de la variable de l'abstracció
                id2 = id + str(getArbol(var))
                # en una abstracció el pare és λ+variable, i el fill el node del terme
                graph.add_node(pydot.Node(id2, label='λ' +
                               str(getArbol(var)), shape='none'))
                # creem una aresta amb el fill
                graph.add_edge(pydot.Edge(id2, visit(term, id2)))
                # retornem el id del node
                return id2

            case Applicacion(esq, dre):
                # l'id del node és l'id del pare 'id' més '@'
                id2 = id + '@'
                # en una aplicació el pare és '@' i els seus dos fills són els termes esq i dre
                graph.add_node(pydot.Node(id2, label='@', shape='none'))

                # afegim les arestes amb els fills
                # aresta Esquerra
                graph.add_edge(pydot.Edge(id2, visit(esq, id2+'E')))
                # aresta Dreta
                graph.add_edge(pydot.Edge(id2, visit(dre, id2+'D')))
                # retornem el id del node
                return id2

            case Variable(var):
                # l'id del node és l'id del pare més '*', '*' podria ser cualsevol altre caràcter
                # ja que és el final del 'path', mentres no sigui una lletra minúscula, ara veurem el motiu*
                id2 = id + '*'
                graph.add_node(pydot.Node(id2, label=var, shape='none'))

                # per saber si var és una variable lligada hem de recòrrer el path i veure si està en el path
                # *: com que només les variables d'una abstracció afegeixen una lletra al path, si var està al path podrem 'linkar' el nostre node amb el pare corresponent
                if var in id2:
                    # l'id del pare serà tot el path fins l'última aparició de la variable
                    # per això anem recorrent el path i quan trobem la variable guardem el path actual a pare_id
                    # després del 'for' el que quedarà a pare_id serà el path de l'última variable, que correspondrà al path, i l'id, del pare
                    path = ''
                    pare_id = ''
                    for i in id2:
                        path += i
                        if i == str(var):
                            pare_id = path
                    # amb l'id del pare podem crear l'aresta, que la diferenciem de la resta amb un estil i color diferents
                    graph.add_edge(pydot.Edge(
                        id2, pare_id, color="purple", style='dotted'))
                return id2

    visit(a, 'ROOT')
    graph.write_png('arbre.png')


# funció Main, s'execute per defecte si no s'executa cap comanda definida
def Main(update, context):
    input_stream = InputStream(update.message.text)
    lexer = achurchLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = achurchParser(token_stream)
    tree = parser.root()

    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = TreeVisitor()
        a = visitor.visit(tree)
        # creem l'imatge de l'arbre original
        crea_imatge(a)
        match a:
            # cas d'una assignació de macro
            case True:
                # ara no hem d'imprimir la llista de macros, només en el cas de '/macros'
                return

            # cas d'analisi d'una expressió
            case _:
                # imprimim l'arbre i l'imatge originals
                context.bot.send_message(
                    chat_id=update.message.chat_id, text=getArbol(a))
                update.message.reply_photo(photo=open('arbre.png', 'rb'))

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

                    # imprimim tota la llista de passos que hem fet per analitzar l'expressió
                    for p in pasos:
                        context.bot.send_message(
                            chat_id=update.message.chat_id, text=p)
                    # netejem la llista per tenir-la preparada per una propera instrucció
                    pasos.clear()

                    # si hem trobat un bucle infinit
                    if exited:
                        context.bot.send_message(
                            chat_id=update.message.chat_id, text="...")
                        context.bot.send_message(
                            chat_id=update.message.chat_id, text="Nothing")
                    # si no podem aplicar més beta reduccions
                    else:
                        # imprimim l'arbre resultant, creem la imatge resultat i l'imprimim
                        context.bot.send_message(
                            chat_id=update.message.chat_id, text=getArbol(b))
                        crea_imatge(b)
                        update.message.reply_photo(
                            photo=open('arbre.png', 'rb'))
    else:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=parser.getNumberOfSyntaxErrors() + 'errors de sintaxi.')
        context.bot.send_message(
            chat_id=update.message.chat_id, text=tree.toStringTree(recog=parser))


# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(update, context):
    botname = context.bot.username
    fullname = update.effective_chat.first_name
    missatge = "Benvingut %s, jo sóc el bot %s\nUtilitza la comanda /help per veure les diferents opcions" % (
        fullname, botname)
    context.bot.send_message(chat_id=update.effective_chat.id, text=missatge)


# defineix una funció que mostra informació de l'autor i que s'executarà quan el bot rebi el missatge /author
def author(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Bot creat per Òscar Ramos Núñez\nPràctica LP (FIB-UPC)\nCurs: 2022-2023 Q2")


# defineix una funció que mostra la llista de comandes i que s'executarà quan el bot rebi el missatge /help
def help2(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="/start - missatge introductori\n/author - veure autor\n/help - llista de comandes\n/macros - taula de macros definides\n/clear - esborrar macros\nλ-Expression Analisis")


# defineix una funció que llista les macros definides i que s'executarà quan el bot rebi el missatge /macros
def macros(update, context):
    if len(llista_macros) == 0:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Oops! Sembla que no hi ha cap macro definida de moment")
    else:
        for i in llista_macros:
            context.bot.send_message(
                chat_id=update.message.chat_id, text=i + '≡' + getArbol(llista_macros[i]))


# defineix una funció que neteja la llista de macros definides i que s'executarà quan el bot rebi el missatge /clear
def clear(update, context):
    llista_macros.clear()


# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()
# crea objecte per treballar amb Telegram
updater = Updater(token=TOKEN, use_context=True)

# definim les funcions del bot
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('author', author))
updater.dispatcher.add_handler(CommandHandler('help', help2))
updater.dispatcher.add_handler(CommandHandler('macros', macros))
updater.dispatcher.add_handler(CommandHandler('clear', clear))
# per defecte, en el cas que no s'utilitzi cap comanda, executarem la funció Main
updater.dispatcher.add_handler(MessageHandler(Filters.text, Main))

# engega el bot
updater.start_polling()