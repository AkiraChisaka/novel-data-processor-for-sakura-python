# settings.py
ANCHOR_SYMBOLS = [
    # Symbols that can be used to anchor lines
    "－",
    "§",
    "＊",
    "*",
    "→",
    "①",
    "②",
    "③",
    "④",
    "⑤",
]
QUOTE_ANCHOR_SYMBOLS = [
    # Anchor symbols are are quotes so need to be treated differently
    ["「", "」"],
    ["『", "』"],
    ["【", "】"],
    ["＜", "＞"],
    ["（", "）"],
    ["(", ")"],
    ["\"", "\""],
]
REPLACEMENT_SYMBOLS = {
    # Settings to replace the symbol on the left with the symbol on the right
    "，": ",",
}
ERROR_CORRECT_LINE_SYMBOL = ";"
INITIAL_CHAOS = 0
MAX_CHAOS_PERMITTED = 100
CHAOS_RISE_ON_SIMPLE_LINE_FIX = 10
CHAOS_RISE_ON_COMPLEX_LINE_FIX = 20
