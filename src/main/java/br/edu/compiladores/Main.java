package br.edu.compiladores;

import br.edu.compiladores.lexer.Scanner;
import br.edu.compiladores.parser.Parser;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public final class Main {
  private Main() {
  }

  public static void main(String[] args) throws Exception {
    Path input = args.length == 0 ? Paths.get("input.txt") : Paths.get(args[0]);

    System.out.println("=== Codigo-fonte de entrada ===");
    System.out.println(input.toAbsolutePath());
    System.out.println();

    System.out.println("=== Tokens gerados pelo Scanner ===");
    TokenPrinter.print(input);
    System.out.println();

    System.out.println("=== Analise Sintatica e Semantica ===");
    Parser parser;
    boolean parsed = false;
    try (Reader reader = Files.newBufferedReader(input, StandardCharsets.UTF_8)) {
      parser = new Parser(new Scanner(reader));
      try {
        parser.parse();
        parsed = true;
      } catch (Exception exception) {
        System.out.println("[ERRO] Parser interrompido: " + exception.getMessage());
      }
    }

    parser.printSemanticReport();
    if (!parsed || parser.hasErrors()) {
      System.exit(1);
    }

    System.out.println("[OK] Solucao integrada executada com sucesso.");
  }
}
