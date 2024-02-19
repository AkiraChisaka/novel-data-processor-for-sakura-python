REPLACEMENT_SYMBOLS = {
    # Settings to replace the symbol on the left with the symbol on the right
    "(": "（",
    ")": "）",
    "「": "\"",
    "」": "\"",
    "“": "\"",
    "”": "\"",
    "·": "・",
}
SURROUNDING_SPACES = [
    # Symbols that should be removed if they are at the start or end of a line
    " ",
    "　",
]
QUOTE_ANCHOR_SYMBOLS = [
    # Anchor symbols are are quotes so need to be treated differently
    ["「", "」"],
    ["『", "』"],
    ["【", "】"],
    ["＜", "＞"],
    ["（", "）"],
    # ["(", ")"],
    ["\"", "\""],
]
ANCHOR_SYMBOLS = [
    # Symbols that can be used to anchor lines
    "－",
    "—",
    # "-",
    "§",
    "＊",
    "*",
    "→",
    # "・",
    "①",
    "②",
    "③",
    "④",
    "⑤",
    # "\"",
]
ERROR_CORRECT_LINE_SYMBOL = ";"
INITIAL_CHAOS = 0
MAX_CHAOS_PERMITTED = 100
CHAOS_RISE_ON_SIMPLE_LINE_FIX = 10
CHAOS_RISE_ON_COMPLEX_LINE_FIX = 20
