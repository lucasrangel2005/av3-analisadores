# -*- coding: utf-8 -*-
from pathlib import Path
from textwrap import dedent

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "relatorio"
OUT_FILE = OUT_DIR / "relatorio-analisadores.pdf"


def code(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def make_table(rows, widths):
    table = Table(rows, colWidths=widths, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("LEADING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#b7c6d6")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f6fa")]),
            ]
        )
    )
    return table


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#5f6b75"))
    canvas.drawString(2 * cm, 1.15 * cm, "AV3 - Analisador Lexico, Sintatico e Semantico")
    canvas.drawRightString(A4[0] - 2 * cm, 1.15 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT_FILE),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Relatorio - Analisadores com JFlex e JCup",
        author="Equipe",
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleBlue",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#153d63"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Subtitle",
            parent=styles["Normal"],
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#2f3b45"),
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="HeadingBlue",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#1f4e79"),
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontSize=9.4,
            leading=13,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Small",
            parent=styles["BodyText"],
            fontSize=8.5,
            leading=11,
            spaceAfter=4,
        )
    )
    code_style = ParagraphStyle(
        "Code",
        fontName="Courier",
        fontSize=7.4,
        leading=9,
        leftIndent=4,
        rightIndent=4,
        spaceBefore=4,
        spaceAfter=8,
    )

    story = []
    story.append(Paragraph("Relatorio - Analisadores com JFlex e JCup", styles["TitleBlue"]))
    story.append(
        Paragraph(
            "Projeto integrado para construcao de um scanner, um parser e uma etapa de verificacao semantica para uma linguagem didatica chamada MiniLang.",
            styles["Subtitle"],
        )
    )
    story.append(Spacer(1, 0.25 * cm))
    story.append(
        make_table(
            [
                ["Item", "Descricao"],
                ["Ferramentas", "JFlex para analise lexica, JCup para analise sintatica e ECJ para compilacao Java."],
                ["Entrada principal", "input.txt, contendo variaveis globais, funcoes, while, if/else, chamadas e return."],
                ["Saida esperada", "Listagem de tokens, sucesso sintatico e relatorio semantico sem erros."],
                ["Pacote", "Especificacoes .flex/.cup, classes geradas, scripts, README e este relatorio PDF."],
            ],
            [3.2 * cm, 12.4 * cm],
        )
    )
    story.append(Spacer(1, 0.2 * cm))

    story.append(Paragraph("1. Objetivo", styles["HeadingBlue"]))
    story.append(
        Paragraph(
            "O objetivo do trabalho foi implementar uma cadeia simples de compilacao front-end: o scanner transforma o codigo-fonte em tokens, o parser valida a estrutura gramatical e as acoes semanticas verificam regras como declaracao previa, compatibilidade de tipos e chamadas de funcao.",
            styles["Body"],
        )
    )

    story.append(Paragraph("2. Linguagem MiniLang", styles["HeadingBlue"]))
    story.append(
        Paragraph(
            "A MiniLang usa uma sintaxe inspirada em linguagens convencionais. Ela possui tipos int, float e void; variaveis globais e locais; funcoes; estruturas if/else e while; atribuicoes; expressoes aritmeticas, relacionais e logicas; return; e print.",
            styles["Body"],
        )
    )
    story.append(
        make_table(
            [
                ["Construcao", "Exemplo aceito"],
                ["Declaracao", "int limite = 5;"],
                ["Funcao", "int soma(int a, int b) { return a + b; }"],
                ["Controle", "while (i < limite) { i = i + 1; }"],
                ["Chamada", "resultado = soma(resultado, i);"],
                ["Saida", "print(resultado);"],
            ],
            [4 * cm, 11.6 * cm],
        )
    )

    story.append(Paragraph("3. Analisador Lexico com JFlex", styles["HeadingBlue"]))
    story.append(
        Paragraph(
            "O arquivo src/main/jflex/MiniLang.flex define as expressoes regulares dos tokens. Comentarios de linha e de bloco sao ignorados, enquanto identificadores, literais numericos, operadores e delimitadores sao retornados como Symbol para o JCup.",
            styles["Body"],
        )
    )
    story.append(
        make_table(
            [
                ["Categoria", "Tokens"],
                ["Keywords", "if, else, while, return, int, float, void, print"],
                ["Identificadores", "Sequencias iniciadas por letra, usando classes [:jletter:] e [:jletterdigit:]"],
                ["Constantes", "INT_LITERAL e FLOAT_LITERAL"],
                ["Operadores", "+, -, *, /, =, ==, !=, <, <=, >, >=, &&, ||, !"],
                ["Delimitadores", ";, ,, (, ), {, }"],
                ["Comentarios", "// comentario e /* comentario de bloco */"],
            ],
            [4 * cm, 11.6 * cm],
        )
    )
    story.append(Preformatted(dedent("""\
        <YYINITIAL> {
          "if"     { return symbol(sym.IF); }
          "while"  { return symbol(sym.WHILE); }
          "=="     { return symbol(sym.EQ); }
          {Float}  { return symbol(sym.FLOAT_LITERAL, Double.valueOf(yytext())); }
          {Integer}{ return symbol(sym.INT_LITERAL, Integer.valueOf(yytext())); }
          {Identifier} { return symbol(sym.ID, yytext()); }
        }"""), code_style))

    story.append(Paragraph("4. Analisador Sintatico com JCup", styles["HeadingBlue"]))
    story.append(
        Paragraph(
            "O arquivo src/main/cup/MiniLang.cup descreve a gramatica LALR da linguagem. A estrutura principal e formada por uma lista de declaracoes, que podem ser declaracoes de variaveis ou definicoes de funcoes. Blocos possuem declaracoes locais e listas de comandos.",
            styles["Body"],
        )
    )
    story.append(
        make_table(
            [
                ["Nao terminal", "Papel na gramatica"],
                ["program", "Ponto de partida; exige uma lista de declaracoes."],
                ["variable_declaration", "Reconhece declaracoes com ou sem inicializacao."],
                ["function_declaration", "Reconhece cabecalho, parametros e bloco da funcao."],
                ["statement", "Agrupa comandos simples, bloco, if/else, while, return e print."],
                ["expression", "Trata atribuicao, operadores logicos, relacionais e aritmeticos."],
            ],
            [4.2 * cm, 11.4 * cm],
        )
    )
    story.append(Preformatted(dedent("""\
        function_declaration ::= function_header compound_statement_function;
        statement ::= expression_statement
                    | compound_statement
                    | selection_statement
                    | iteration_statement
                    | return_statement
                    | print_statement;
        expression ::= ID ASSIGN expression
                    | logical_or_expression;"""), code_style))

    story.append(Paragraph("5. Analise Semantica", styles["HeadingBlue"]))
    story.append(
        Paragraph(
            "As acoes semanticas foram implementadas diretamente no parser gerado pelo JCup. O parser mantem uma pilha de escopos, uma tabela de funcoes e uma lista de erros para continuar a verificacao apos encontrar problemas.",
            styles["Body"],
        )
    )
    story.append(
        make_table(
            [
                ["Regra", "Verificacao realizada"],
                ["Escopo", "Variaveis locais, parametros e globais sao separados por escopo."],
                ["Duplicidade", "Impede declarar o mesmo identificador duas vezes no mesmo escopo."],
                ["Uso previo", "Sinaliza variavel usada antes da declaracao."],
                ["Tipos", "Permite int em float, mas rejeita float em int."],
                ["Funcoes", "Confere existencia, quantidade de argumentos e tipos dos argumentos."],
                ["Return", "Valida return com valor em funcoes nao void e sem valor em funcoes void."],
                ["main", "Exige funcao main void e sem parametros."],
            ],
            [3.5 * cm, 12.1 * cm],
        )
    )

    story.append(Paragraph("6. Integracao", styles["HeadingBlue"]))
    story.append(
        Paragraph(
            "A classe br.edu.compiladores.Main executa a demonstracao completa. Primeiro instancia o Scanner para imprimir todos os tokens do input.txt. Depois cria outro Scanner para alimentar o Parser, pois o primeiro percurso consome o arquivo. O Parser recebe os tokens via interface java_cup.runtime.Scanner.",
            styles["Body"],
        )
    )
    story.append(Preformatted(dedent("""\
        Scanner scanner = new Scanner(reader);
        Parser parser = new Parser(scanner);
        parser.parse();
        parser.printSemanticReport();"""), code_style))

    story.append(Paragraph("7. Entrada e Saida Esperada", styles["HeadingBlue"]))
    story.append(
        Paragraph(
            "O arquivo input.txt contem variaveis globais, a funcao soma e a funcao main com while, if/else, chamada de funcao, declaracao local float e return. A execucao esperada imprime os tokens e termina com sucesso sintatico e semantico.",
            styles["Body"],
        )
    )
    story.append(Preformatted(dedent("""\
        [OK] Analise sintatica concluida.
        [OK] Analise semantica concluida.
             Funcoes reconhecidas: [soma, main]
        [OK] Solucao integrada executada com sucesso."""), code_style))

    story.append(Paragraph("8. Scripts e Execucao", styles["HeadingBlue"]))
    story.append(
        make_table(
            [
                ["Script", "Funcao"],
                ["scripts/download-tools.ps1", "Baixa JFlex, JCup, runtime do CUP e ECJ para lib."],
                ["scripts/generate.ps1", "Gera Scanner.java, Parser.java e sym.java."],
                ["scripts/build.ps1", "Gera os fontes e compila as classes Java."],
                ["scripts/run.ps1", "Executa a demonstracao integrada sobre input.txt ou outro arquivo informado."],
                ["scripts/test.ps1", "Executa um caso valido e um caso com erros semanticos esperados."],
            ],
            [5 * cm, 10.6 * cm],
        )
    )
    story.append(Preformatted(dedent("""\
        .\\scripts\\generate.ps1
        .\\scripts\\build.ps1
        .\\scripts\\run.ps1
        .\\scripts\\test.ps1"""), code_style))

    story.append(Paragraph("9. Arquivos Entregues", styles["HeadingBlue"]))
    story.append(
        make_table(
            [
                ["Arquivo/Pasta", "Conteudo"],
                ["src/main/jflex/MiniLang.flex", "Especificacao lexico-formal do scanner."],
                ["src/main/cup/MiniLang.cup", "Gramatica e regras semanticas."],
                ["src/generated/java/.../Scanner.java", "Scanner gerado pelo JFlex."],
                ["src/generated/java/.../Parser.java", "Parser gerado pelo JCup."],
                ["src/generated/java/.../sym.java", "Tabela de simbolos gerada pelo JCup."],
                ["input.txt", "Programa de entrada principal."],
                ["README.md", "Passo a passo de compilacao e execucao."],
                ["relatorio/relatorio-analisadores.pdf", "Relatorio para apresentacao."],
            ],
            [6 * cm, 9.6 * cm],
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("10. Conclusao", styles["HeadingBlue"]))
    story.append(
        Paragraph(
            "A solucao demonstra a integracao entre analise lexica, analise sintatica e analise semantica. O scanner reconhece os tokens definidos na linguagem, o parser valida a estrutura do programa e a etapa semantica identifica inconsistencias comuns antes de qualquer geracao de codigo. Assim, o projeto cobre o fluxo essencial de um front-end de compilador didatico.",
            styles["Body"],
        )
    )
    story.append(Paragraph("Referencias", styles["HeadingBlue"]))
    story.append(
        Paragraph(
            "JFlex: https://jflex.de/ ; Java CUP: https://www2.cs.tum.edu/projects/cup/ ; Maven Central usado pelos scripts para baixar as ferramentas.",
            styles["Small"],
        )
    )

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(OUT_FILE)


if __name__ == "__main__":
    build()
