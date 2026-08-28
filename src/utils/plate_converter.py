import re


LETTER_MAP = {
    "A": "الف",
    "B": "ب",
    "D": "د",
#    "t": "ت",
    "H": "ه",
    "J": "ج",
    "L": "ل",
    "M": "م",
    "N": "ن",
    "P": "پ",
    "S": "س",
    "T": "ط",
    "V": "و",
    "Y": "ی",
}


REVERSE_LETTER_MAP = {
    v: k
    for k, v in LETTER_MAP.items()
}


PERSIAN_DIGITS = {
    "0": "۰",
    "1": "۱",
    "2": "۲",
    "3": "۳",
    "4": "۴",
    "5": "۵",
    "6": "۶",
    "7": "۷",
    "8": "۸",
    "9": "۹",
}


ENGLISH_DIGITS = {
    "۰": "0",
    "۱": "1",
    "۲": "2",
    "۳": "3",
    "۴": "4",
    "۵": "5",
    "۶": "6",
    "۷": "7",
    "۸": "8",
    "۹": "9",
}


def to_persian_number(text: str) -> str:

    for en, fa in PERSIAN_DIGITS.items():
        text = text.replace(en, fa)

    return text


def to_english_number(text: str) -> str:

    for fa, en in ENGLISH_DIGITS.items():
        text = text.replace(fa, en)

    return text


def to_persian_plate(
    plate_number: str
) -> str:

    """
    44B123-88
    =>
    ۴۴ ب ۱۲۳ ۸۸
    """

    pattern = r"(\d{2})([A-Z])(\d{3})-(\d{2})"

    match = re.match(
        pattern,
        plate_number
    )

    if not match:
        return plate_number

    left, letter, middle, right = match.groups()

    persian_letter = (
        LETTER_MAP.get(
            letter,
            letter
        )
    )

    return (
        f"{to_persian_number(left)} "
        f"{persian_letter} "
        f"{to_persian_number(middle)} "
        f"{to_persian_number(right)}"
    )


def to_database_plate(
    persian_plate: str
) -> str:

    """
    ۴۴ ب ۱۲۳ ۸۸
    =>
    44B123-88
    """

    persian_plate = (
        persian_plate
        .strip()
    )

    parts = persian_plate.split()

    if len(parts) != 4:
        raise ValueError(
            "فرمت پلاک صحیح نیست"
        )

    left = to_english_number(
        parts[0]
    )

    letter = (
        REVERSE_LETTER_MAP
        .get(parts[1])
    )

    if not letter:
        raise ValueError(
            "حرف پلاک نامعتبر است"
        )

    middle = to_english_number(
        parts[2]
    )

    right = to_english_number(
        parts[3]
    )

    return (
        f"{left}"
        f"{letter}"
        f"{middle}"
        f"-"
        f"{right}"
    )