package br.edu.compiladores;

import br.edu.compiladores.lexer.Scanner;
import br.edu.compiladores.parser.sym;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java_cup.runtime.Symbol;

public final class TokenPrinter {
  private TokenPrinter() {
  }

  public static void print(Path input) throws Exception {
    try (Reader reader = Files.newBufferedReader(input, StandardCharsets.UTF_8)) {
      Scanner scanner = new Scanner(reader);
      Symbol token;
      while ((token = scanner.next_token()).sym != sym.EOF) {
        String value = token.value == null ? "" : " valor=" + token.value;
        System.out.printf("%-15s linha=%-3d coluna=%-3d%s%n",
            TokenNames.name(token.sym), token.left, token.right, value);
      }
    }
  }
}
