package br.edu.compiladores.lexer;

import java_cup.runtime.Symbol;
import br.edu.compiladores.parser.sym;

%%

%public
%class Scanner
%unicode
%cup
%line
%column
%state COMMENT

%{
  private Symbol symbol(int type) {
    return new Symbol(type, yyline + 1, yycolumn + 1);
  }

  private Symbol symbol(int type, Object value) {
    return new Symbol(type, yyline + 1, yycolumn + 1, value);
  }
%}

LineTerminator = \r|\n|\r\n
WhiteSpace = {LineTerminator} | [ \t\f]
Identifier = [:jletter:][:jletterdigit:]*
Integer = 0|[1-9][0-9]*
Float = ({Integer}\.[0-9]+)([eE][+-]?[0-9]+)?|({Integer}[eE][+-]?[0-9]+)

%%

<YYINITIAL> {
  "//".*                         { }
  "/*"                           { yybegin(COMMENT); }

  "if"                           { return symbol(sym.IF); }
  "else"                         { return symbol(sym.ELSE); }
  "while"                        { return symbol(sym.WHILE); }
  "return"                       { return symbol(sym.RETURN); }
  "int"                          { return symbol(sym.INT); }
  "float"                        { return symbol(sym.FLOAT); }
  "void"                         { return symbol(sym.VOID); }
  "print"                        { return symbol(sym.PRINT); }

  "=="                           { return symbol(sym.EQ); }
  "!="                           { return symbol(sym.NE); }
  "<="                           { return symbol(sym.LE); }
  ">="                           { return symbol(sym.GE); }
  "&&"                           { return symbol(sym.AND); }
  "||"                           { return symbol(sym.OR); }

  "="                            { return symbol(sym.ASSIGN); }
  "<"                            { return symbol(sym.LT); }
  ">"                            { return symbol(sym.GT); }
  "!"                            { return symbol(sym.NOT); }
  "+"                            { return symbol(sym.PLUS); }
  "-"                            { return symbol(sym.MINUS); }
  "*"                            { return symbol(sym.TIMES); }
  "/"                            { return symbol(sym.DIVIDE); }

  ";"                            { return symbol(sym.SEMI); }
  ","                            { return symbol(sym.COMMA); }
  "("                            { return symbol(sym.LPAREN); }
  ")"                            { return symbol(sym.RPAREN); }
  "{"                            { return symbol(sym.LBRACE); }
  "}"                            { return symbol(sym.RBRACE); }

  {Float}                        { return symbol(sym.FLOAT_LITERAL, Double.valueOf(yytext())); }
  {Integer}                      { return symbol(sym.INT_LITERAL, Integer.valueOf(yytext())); }
  {Identifier}                   { return symbol(sym.ID, yytext()); }
  {WhiteSpace}                   { }
}

<COMMENT> {
  "*/"                           { yybegin(YYINITIAL); }
  [^*\r\n]+                      { }
  "*"                            { }
  {LineTerminator}               { }
  <<EOF>>                        { throw new RuntimeException("Comentario de bloco nao encerrado na linha " + (yyline + 1)); }
}

[^]                              { throw new RuntimeException("Caractere ilegal '" + yytext() + "' na linha " + (yyline + 1) + ", coluna " + (yycolumn + 1)); }
