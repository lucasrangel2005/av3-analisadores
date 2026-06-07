package br.edu.compiladores;

import br.edu.compiladores.parser.sym;

public final class TokenNames {
  private TokenNames() {
  }

  public static String name(int tokenId) {
    if (tokenId >= 0 && tokenId < sym.terminalNames.length) {
      return sym.terminalNames[tokenId];
    }
    return "#" + tokenId;
  }
}
