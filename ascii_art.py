"""Enkel ASCII-banderollgenerator.

Detta program ber användaren om ett ord och skriver sedan ut
en dekorativ ASCII-grafik med stiliserade blockbokstäver.
"""

from __future__ import annotations

LETTER_HEIGHT = 5
SPACING = "  "

LETTER_PATTERNS = {
    "A": [
        "  A  ",
        " A A ",
        "AAAAA",
        "A   A",
        "A   A",
    ],
    "B": [
        "BBBB ",
        "B   B",
        "BBBB ",
        "B   B",
        "BBBB ",
    ],
    "C": [
        " CCCC",
        "C    ",
        "C    ",
        "C    ",
        " CCCC",
    ],
    "D": [
        "DDDD ",
        "D   D",
        "D   D",
        "D   D",
        "DDDD ",
    ],
    "E": [
        "EEEEE",
        "E    ",
        "EEE  ",
        "E    ",
        "EEEEE",
    ],
    "F": [
        "FFFFF",
        "F    ",
        "FFF  ",
        "F    ",
        "F    ",
    ],
    "G": [
        " GGGG",
        "G    ",
        "G  GG",
        "G   G",
        " GGG ",
    ],
    "H": [
        "H   H",
        "H   H",
        "HHHHH",
        "H   H",
        "H   H",
    ],
    "I": [
        "IIIII",
        "  I  ",
        "  I  ",
        "  I  ",
        "IIIII",
    ],
    "J": [
        "JJJJJ",
        "    J",
        "    J",
        "J   J",
        " JJJ ",
    ],
    "K": [
        "K   K",
        "K  K ",
        "K K  ",
        "K  K ",
        "K   K",
    ],
    "L": [
        "L    ",
        "L    ",
        "L    ",
        "L    ",
        "LLLLL",
    ],
    "M": [
        "M   M",
        "MM MM",
        "M M M",
        "M   M",
        "M   M",
    ],
    "N": [
        "N   N",
        "NN  N",
        "N N N",
        "N  NN",
        "N   N",
    ],
    "O": [
        " OOO ",
        "O   O",
        "O   O",
        "O   O",
        " OOO ",
    ],
    "P": [
        "PPPP ",
        "P   P",
        "PPPP ",
        "P    ",
        "P    ",
    ],
    "Q": [
        " QQQ ",
        "Q   Q",
        "Q   Q",
        "Q  Q ",
        " QQ Q",
    ],
    "R": [
        "RRRR ",
        "R   R",
        "RRRR ",
        "R  R ",
        "R   R",
    ],
    "S": [
        " SSS ",
        "S    ",
        " SSS ",
        "    S",
        " SSS ",
    ],
    "T": [
        "TTTTT",
        "  T  ",
        "  T  ",
        "  T  ",
        "  T  ",
    ],
    "U": [
        "U   U",
        "U   U",
        "U   U",
        "U   U",
        " UUU ",
    ],
    "V": [
        "V   V",
        "V   V",
        "V   V",
        " V V ",
        "  V  ",
    ],
    "W": [
        "W   W",
        "W   W",
        "W W W",
        "WW WW",
        "W   W",
    ],
    "X": [
        "X   X",
        " X X ",
        "  X  ",
        " X X ",
        "X   X",
    ],
    "Y": [
        "Y   Y",
        " Y Y ",
        "  Y  ",
        "  Y  ",
        "  Y  ",
    ],
    "Z": [
        "ZZZZZ",
        "   Z ",
        "  Z  ",
        " Z   ",
        "ZZZZZ",
    ],
    " ": [
        "     ",
        "     ",
        "     ",
        "     ",
        "     ",
    ],
    "?": [
        "?????",
        "   ? ",
        "  ?  ",
        "     ",
        "  ?  ",
    ],
}

COLOR_CODES = {
    "röd": "\033[31m",
    "grön": "\033[32m",
    "gul": "\033[33m",
    "blå": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "vit": "\033[37m",
}
RESET_COLOR = "\033[0m"


def render_word(word: str) -> list[str]:
    """Returnera rader med ASCII-grafik för det angivna ordet."""
    rows = ["" for _ in range(LETTER_HEIGHT)]
    for index, char in enumerate(word.upper()):
        pattern = LETTER_PATTERNS.get(char, LETTER_PATTERNS["?"])
        for row_index in range(LETTER_HEIGHT):
            if rows[row_index]:
                rows[row_index] += SPACING
            rows[row_index] += pattern[row_index]
    return rows


def frame_lines(lines: list[str]) -> list[str]:
    """Lägg till en dekorativ ram runt raderna."""
    if not lines:
        return []
    content_width = max(len(line) for line in lines)
    top_bottom = "*" * (content_width + 4)
    framed = [top_bottom]
    for line in lines:
        padded = line.ljust(content_width)
        framed.append(f"* {padded} *")
    framed.append(top_bottom)
    return framed


def prompt_for_color() -> str:
    """Be användaren välja en färgkod för bokstäverna."""
    print("Tillgängliga färger:")
    for name in COLOR_CODES:
        print(f"- {name.title()}")
    while True:
        choice = input("Välj en färg (eller tryck enter för standardfärg): ").strip().lower()
        if not choice:
            return ""
        if choice in COLOR_CODES:
            return COLOR_CODES[choice]
        print("Ogiltigt val. Försök igen.")


def main() -> None:
    word = input("Skriv ett ord och tryck enter: ").strip()
    if not word:
        print("Inget ord angavs. Programmet avslutas.")
        return
    color_choice = prompt_for_color()
    art_lines = render_word(word)
    framed_art = frame_lines(art_lines)
    print()
    for line in framed_art:
        if color_choice and line.startswith("* ") and line.endswith(" *"):
            content = line[2:-2]
            colored_content = f"{color_choice}{content}{RESET_COLOR}"
            print(f"* {colored_content} *")
        else:
            print(line)


if __name__ == "__main__":
    main()
