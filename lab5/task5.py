from num2words import num2words


def converts_amount_into_written_amount(amount: float) -> str:
    if not isinstance(amount, (int, float)):
        raise TypeError("The number must be an integer or a decimal")
    if not (0 <= amount <= 999999.99):
        raise ValueError("The number must be between 0 and 999999.99")

    hryvnias = int(amount)
    kopiyka = int(round((amount - hryvnias) * 100))

    hryvnias_words = num2words(hryvnias, lang='uk')
    if hryvnias % 10 == 1 and hryvnias % 100 != 11:
        hryvnias_words = hryvnias_words.replace("один", "одна").replace("Один", "Одна")

    hryvnia_word = get_hryvnia_form(hryvnias)
    form_kopiyka = get_kopeck_form(kopiyka)

    return f"{hryvnias_words.capitalize()} {hryvnia_word} {kopiyka} {form_kopiyka}"


def get_hryvnia_form(number: int) -> str:
    if 10 <= number % 100 <= 19:
        return "гривень"
    elif number % 10 == 1:
        return "гривня"
    elif 2 <= number % 10 <= 4:
        return "гривні"
    else:
        return "гривень"


def get_kopeck_form(number: int) -> str:
    if 10 <= number % 100 <= 19:
        return "копійок"
    elif number % 10 == 1:
        return "копійка"
    elif 2 <= number % 10 <= 4:
        return "копійки"
    else:
        return "копійок"
