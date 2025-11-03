"""Enkel ASCII-banderollgenerator i C64-stil med sinus-scroll.

Programmet ber användaren om ett ord och visar sedan en färgad
skrollande banderoll som följer en sinuskurva, inspirerad av
klassiska C64-demos.
"""

from __future__ import annotations

import math
import shutil
import sys
import time

LETTER_HEIGHT = 5
SPACING_COLUMNS = 3
PIXEL_ON_CHAR = "#"
PIXEL_SHADOW_CHAR = "."
FRAME_DELAY = 0.05
WAVE_LENGTH = 8.0

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


def build_text_columns(word: str) -> tuple[list[list[bool]], list[float]]:
    """Förvandla ordet till kolumner av boolar och vågfas per bokstav."""
    columns: list[list[bool]] = []
    phases: list[float] = []
    for char in word.upper():
        pattern = LETTER_PATTERNS.get(char, LETTER_PATTERNS["?"])
        width = len(pattern[0])
        start_index = len(columns)
        letter_center = start_index + width / 2
        for col_idx in range(width):
            column = [pattern[row][col_idx] != " " for row in range(LETTER_HEIGHT)]
            columns.append(column)
            phases.append(letter_center)
        for _ in range(SPACING_COLUMNS):
            columns.append([False] * LETTER_HEIGHT)
            phases.append(letter_center)
    if not columns:
        return [[False] * LETTER_HEIGHT], [0.0]
    return columns, phases


def compose_frame(
    columns: list[list[bool]],
    phases: list[float],
    frame_index: int,
    width: int,
    height: int,
    amplitude: int,
    baseline: int,
) -> list[list[str]]:
    """Skapa en enkel framebuffer med skuggade tecken."""
    buffer = [[" "] * width for _ in range(height)]
    column_count = len(columns)
    for screen_col in range(width):
        source_idx = frame_index + screen_col
        if source_idx < 0 or source_idx >= column_count:
            continue
        column_bits = columns[source_idx]
        phase_value = (frame_index + phases[source_idx]) / WAVE_LENGTH
        vertical_offset = int(
            round(math.sin(phase_value) * amplitude)
        )
        top_row = baseline + vertical_offset
        for bit_row, is_on in enumerate(column_bits):
            if not is_on:
                continue
            target_row = top_row + bit_row
            if 0 <= target_row < height:
                buffer[target_row][screen_col] = PIXEL_ON_CHAR
                shadow_row = target_row + 1
                shadow_col = screen_col + 1
                if (
                    0 <= shadow_row < height
                    and 0 <= shadow_col < width
                    and buffer[shadow_row][shadow_col] == " "
                ):
                    buffer[shadow_row][shadow_col] = PIXEL_SHADOW_CHAR
    return buffer


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


def format_line(chars: list[str], color_code: str) -> str:
    """Färglägg sammanhängande tecken med vald färg."""
    if not color_code:
        return "".join(chars)
    result: list[str] = []
    in_color = False
    for ch in chars:
        if ch == PIXEL_ON_CHAR and not in_color:
            result.append(color_code)
            in_color = True
        elif ch != PIXEL_ON_CHAR and in_color:
            result.append(RESET_COLOR)
            in_color = False
        result.append(ch)
    if in_color:
        result.append(RESET_COLOR)
    return "".join(result)


def animate_scroll(word: str, color_code: str) -> None:
    """Visa banderollen och låt texten skrolla över skärmen."""
    columns, phases = build_text_columns(word)
    term_size = shutil.get_terminal_size(fallback=(80, 24))
    width = max(40, term_size.columns)
    height = max(LETTER_HEIGHT + 6, min(term_size.lines or 24, 40))
    amplitude = max(1, min((height - LETTER_HEIGHT) // 2, 6))
    baseline = height // 2 - LETTER_HEIGHT // 2

    print("Tryck Ctrl+C för att avsluta demon.")
    time.sleep(1)

    hide_cursor = "\033[?25l"
    show_cursor = "\033[?25h"
    total_frames = len(columns) + width

    sys.stdout.write(hide_cursor)
    sys.stdout.flush()
    try:
        while True:
            frame_index = -width
            while frame_index <= total_frames:
                buffer = compose_frame(
                    columns,
                    phases,
                    frame_index,
                    width,
                    height,
                    amplitude,
                    baseline,
                )
                sys.stdout.write("\033[H\033[2J")
                for line_chars in buffer:
                    sys.stdout.write(format_line(line_chars, color_code) + "\n")
                sys.stdout.flush()
                frame_index += 1
                time.sleep(FRAME_DELAY)
            time.sleep(0.3)
    except KeyboardInterrupt:
        sys.stdout.write("\nDemon avslutad.\n")
        sys.stdout.flush()
    finally:
        sys.stdout.write(show_cursor)
        sys.stdout.flush()


def main() -> None:
    word = input("Skriv ett ord och tryck enter: ").strip()
    if not word:
        print("Inget ord angavs. Programmet avslutas.")
        return
    color_choice = prompt_for_color()
    animate_scroll(word, color_choice)


if __name__ == "__main__":
    main()
