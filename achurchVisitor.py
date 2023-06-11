# Generated from achurch.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .achurchParser import achurchParser
else:
    from achurchParser import achurchParser

# This class defines a complete generic visitor for a parse tree produced by achurchParser.

class achurchVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by achurchParser#root.
    def visitRoot(self, ctx:achurchParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by achurchParser#inst.
    def visitInst(self, ctx:achurchParser.InstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by achurchParser#assignacio.
    def visitAssignacio(self, ctx:achurchParser.AssignacioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by achurchParser#calcul.
    def visitCalcul(self, ctx:achurchParser.CalculContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by achurchParser#parentesis.
    def visitParentesis(self, ctx:achurchParser.ParentesisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by achurchParser#macro.
    def visitMacro(self, ctx:achurchParser.MacroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by achurchParser#lletra.
    def visitLletra(self, ctx:achurchParser.LletraContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by achurchParser#abstraccio.
    def visitAbstraccio(self, ctx:achurchParser.AbstraccioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by achurchParser#aplicacio.
    def visitAplicacio(self, ctx:achurchParser.AplicacioContext):
        return self.visitChildren(ctx)



del achurchParser