grammar achurch;
root : termes            // l'etiqueta ja és root
     ;

termes : terme*;


terme : '(' terme ')'   #parentesis
      | terme terme     #aplicacio
      | SIMBOL LLETRA+ '.' terme #abstraccio
      | LLETRA  #lletra
      ;


LLETRA : [a-z];
SIMBOL : ('\\' | 'λ');
WS  : [ \t\n\r]+ -> skip ;
