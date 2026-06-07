# Analisador Lexico, Sintatico e Semantico

Projeto da AV3 com JFlex, JCup e Java. A linguagem implementada e uma MiniLang inspirada em C, com variaveis, funcoes, `if/else`, `while`, `return`, chamadas de funcao, atribuicoes e expressoes.

## Estrutura

- `src/main/jflex/MiniLang.flex`: especificacao do scanner JFlex.
- `src/main/cup/MiniLang.cup`: gramatica JCup com acoes semanticas.
- `src/main/java/br/edu/compiladores`: programa de demonstracao integrada.
- `src/generated/java`: classes geradas por JFlex e JCup apos executar os scripts.
- `input.txt`: codigo-fonte de entrada valido.
- `examples/input_semantic_error.txt`: entrada extra para demonstrar erros semanticos.
- `scripts`: scripts de download, geracao, compilacao, execucao e teste.

## Requisitos

- Java Runtime (`java`) instalado.
- PowerShell.
- Internet na primeira execucao, pois os scripts baixam JFlex, Java CUP, Java CUP Runtime e ECJ para a pasta `lib`.

Observacao: este projeto usa o compilador ECJ via JAR, por isso funciona mesmo quando `javac` nao esta no PATH.

## Como gerar Scanner, Parser e Sym

```powershell
.\scripts\generate.ps1
```

Saidas principais:

- `src/generated/java/br/edu/compiladores/lexer/Scanner.java`
- `src/generated/java/br/edu/compiladores/parser/Parser.java`
- `src/generated/java/br/edu/compiladores/parser/sym.java`

## Como compilar

```powershell
.\scripts\build.ps1
```

As classes compiladas ficam em `build/classes`.

## Como executar a demonstracao integrada

```powershell
.\scripts\run.ps1
```

Tambem e possivel informar outro arquivo:

```powershell
.\scripts\run.ps1 .\examples\input_semantic_error.txt
```

A execucao imprime:

1. O arquivo de entrada usado.
2. A lista de tokens gerados pelo Scanner.
3. O resultado da analise sintatica.
4. O resultado da analise semantica.

## Como rodar os testes de demonstracao

```powershell
.\scripts\test.ps1
```

O primeiro teste usa `input.txt` e deve passar. O segundo usa `examples/input_semantic_error.txt` e deve falhar, mostrando erros como incompatibilidade de tipos, variavel nao declarada, quantidade incorreta de argumentos e retorno invalido em funcao `void`.

## Observacao sobre o nome da pasta no Windows

Se a pasta do projeto terminar com ponto final, algumas versoes do PowerShell podem ter dificuldade para resolver o caminho. Nesse caso, renomeie a pasta removendo o ponto final ou execute os scripts a partir de um caminho alternativo sem ponto, por exemplo um junction criado com `mklink /J`.

## Resumo da linguagem

Tipos:

```c
int
float
void
```

Comandos:

```c
if (condicao) comando else comando
while (condicao) comando
return;
return expressao;
print(expressao);
```

Exemplo:

```c
int soma(int a, int b) {
    int total = a + b;
    return total;
}

void main() {
    int resultado = soma(2, 3);
    print(resultado);
    return;
}
```
