grammar lc;
root : inst        //root és un conjunt d'instruccions    
     ;

inst: instruccio*;

instruccio: 
      VAR ('≡' | '=') terme     #assignacio
      | terme          #calcul
      ;



terme : '(' terme ')'   #parentesis
      | terme terme     #aplicacio
      | SIMBOL LLETRA+ '.' terme #abstraccio
      | LLETRA  #lletra
      | VAR       #macro
      ;

VAR: ( [A-Z] ([A-Z] | [0-9])*) | ( [\u0021-\u0027] | [\u002A-\u002D] | [\u002F] | [\u003A-\u003C] | [\u003E-\u0040] | [\u005B] | [\u005D-\u0060] | [\u007B-\u007E] | [\u00A0-\u00AC] | [\u00AE-\u00EF] | [\u00F7] ); //agafem com a possibilitats tots els caracters exceptuant els alfanumèrics, parèntesis, etc.
LLETRA : [a-z];
SIMBOL : ('\u005C' | 'λ'); //pot ser una λ o un '\'
WS  : [ \t\n\r]+ -> skip ;