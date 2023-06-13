# Generated from lc.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,9,47,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,1,1,5,1,12,8,1,
        10,1,12,1,15,9,1,1,2,1,2,1,2,1,2,3,2,21,8,2,1,3,1,3,1,3,1,3,1,3,
        1,3,1,3,4,3,30,8,3,11,3,12,3,31,1,3,1,3,1,3,1,3,3,3,38,8,3,1,3,1,
        3,5,3,42,8,3,10,3,12,3,45,9,3,1,3,0,1,6,4,0,2,4,6,0,1,1,0,1,2,49,
        0,8,1,0,0,0,2,13,1,0,0,0,4,20,1,0,0,0,6,37,1,0,0,0,8,9,3,2,1,0,9,
        1,1,0,0,0,10,12,3,4,2,0,11,10,1,0,0,0,12,15,1,0,0,0,13,11,1,0,0,
        0,13,14,1,0,0,0,14,3,1,0,0,0,15,13,1,0,0,0,16,17,5,6,0,0,17,18,7,
        0,0,0,18,21,3,6,3,0,19,21,3,6,3,0,20,16,1,0,0,0,20,19,1,0,0,0,21,
        5,1,0,0,0,22,23,6,3,-1,0,23,24,5,3,0,0,24,25,3,6,3,0,25,26,5,4,0,
        0,26,38,1,0,0,0,27,29,5,8,0,0,28,30,5,7,0,0,29,28,1,0,0,0,30,31,
        1,0,0,0,31,29,1,0,0,0,31,32,1,0,0,0,32,33,1,0,0,0,33,34,5,5,0,0,
        34,38,3,6,3,3,35,38,5,7,0,0,36,38,5,6,0,0,37,22,1,0,0,0,37,27,1,
        0,0,0,37,35,1,0,0,0,37,36,1,0,0,0,38,43,1,0,0,0,39,40,10,4,0,0,40,
        42,3,6,3,5,41,39,1,0,0,0,42,45,1,0,0,0,43,41,1,0,0,0,43,44,1,0,0,
        0,44,7,1,0,0,0,45,43,1,0,0,0,5,13,20,31,37,43
    ]

class lcParser ( Parser ):

    grammarFileName = "lc.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'\\u2261'", "'='", "'('", "')'", "'.'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "VAR", "LLETRA", "SIMBOL", 
                      "WS" ]

    RULE_root = 0
    RULE_inst = 1
    RULE_instruccio = 2
    RULE_terme = 3

    ruleNames =  [ "root", "inst", "instruccio", "terme" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    VAR=6
    LLETRA=7
    SIMBOL=8
    WS=9

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def inst(self):
            return self.getTypedRuleContext(lcParser.InstContext,0)


        def getRuleIndex(self):
            return lcParser.RULE_root

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = lcParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 8
            self.inst()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InstContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def instruccio(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lcParser.InstruccioContext)
            else:
                return self.getTypedRuleContext(lcParser.InstruccioContext,i)


        def getRuleIndex(self):
            return lcParser.RULE_inst

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInst" ):
                return visitor.visitInst(self)
            else:
                return visitor.visitChildren(self)




    def inst(self):

        localctx = lcParser.InstContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_inst)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 456) != 0):
                self.state = 10
                self.instruccio()
                self.state = 15
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InstruccioContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return lcParser.RULE_instruccio

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class AssignacioContext(InstruccioContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a lcParser.InstruccioContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VAR(self):
            return self.getToken(lcParser.VAR, 0)
        def terme(self):
            return self.getTypedRuleContext(lcParser.TermeContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignacio" ):
                return visitor.visitAssignacio(self)
            else:
                return visitor.visitChildren(self)


    class CalculContext(InstruccioContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a lcParser.InstruccioContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def terme(self):
            return self.getTypedRuleContext(lcParser.TermeContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCalcul" ):
                return visitor.visitCalcul(self)
            else:
                return visitor.visitChildren(self)



    def instruccio(self):

        localctx = lcParser.InstruccioContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_instruccio)
        self._la = 0 # Token type
        try:
            self.state = 20
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = lcParser.AssignacioContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 16
                self.match(lcParser.VAR)
                self.state = 17
                _la = self._input.LA(1)
                if not(_la==1 or _la==2):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 18
                self.terme(0)
                pass

            elif la_ == 2:
                localctx = lcParser.CalculContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 19
                self.terme(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return lcParser.RULE_terme

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class ParentesisContext(TermeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a lcParser.TermeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def terme(self):
            return self.getTypedRuleContext(lcParser.TermeContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParentesis" ):
                return visitor.visitParentesis(self)
            else:
                return visitor.visitChildren(self)


    class MacroContext(TermeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a lcParser.TermeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VAR(self):
            return self.getToken(lcParser.VAR, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMacro" ):
                return visitor.visitMacro(self)
            else:
                return visitor.visitChildren(self)


    class LletraContext(TermeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a lcParser.TermeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LLETRA(self):
            return self.getToken(lcParser.LLETRA, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLletra" ):
                return visitor.visitLletra(self)
            else:
                return visitor.visitChildren(self)


    class AbstraccioContext(TermeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a lcParser.TermeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SIMBOL(self):
            return self.getToken(lcParser.SIMBOL, 0)
        def terme(self):
            return self.getTypedRuleContext(lcParser.TermeContext,0)

        def LLETRA(self, i:int=None):
            if i is None:
                return self.getTokens(lcParser.LLETRA)
            else:
                return self.getToken(lcParser.LLETRA, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbstraccio" ):
                return visitor.visitAbstraccio(self)
            else:
                return visitor.visitChildren(self)


    class AplicacioContext(TermeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a lcParser.TermeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def terme(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lcParser.TermeContext)
            else:
                return self.getTypedRuleContext(lcParser.TermeContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAplicacio" ):
                return visitor.visitAplicacio(self)
            else:
                return visitor.visitChildren(self)



    def terme(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = lcParser.TermeContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 6
        self.enterRecursionRule(localctx, 6, self.RULE_terme, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                localctx = lcParser.ParentesisContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 23
                self.match(lcParser.T__2)
                self.state = 24
                self.terme(0)
                self.state = 25
                self.match(lcParser.T__3)
                pass
            elif token in [8]:
                localctx = lcParser.AbstraccioContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 27
                self.match(lcParser.SIMBOL)
                self.state = 29 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 28
                    self.match(lcParser.LLETRA)
                    self.state = 31 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==7):
                        break

                self.state = 33
                self.match(lcParser.T__4)
                self.state = 34
                self.terme(3)
                pass
            elif token in [7]:
                localctx = lcParser.LletraContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 35
                self.match(lcParser.LLETRA)
                pass
            elif token in [6]:
                localctx = lcParser.MacroContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 36
                self.match(lcParser.VAR)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 43
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = lcParser.AplicacioContext(self, lcParser.TermeContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_terme)
                    self.state = 39
                    if not self.precpred(self._ctx, 4):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                    self.state = 40
                    self.terme(5) 
                self.state = 45
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[3] = self.terme_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def terme_sempred(self, localctx:TermeContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         




