"""Moduł kalkulatora pobierający znak operacji bezpośrednio od użytkownika."""


def add(first_number: float, second_number: float) -> float:
    """Dodaje dwie liczby i zwraca wynik."""
    return first_number + second_number


def subtract(first_number: float, second_number: float) -> float:
    """Odejmuje drugą liczbę od pierwszej i zwraca wynik."""
    return first_number - second_number


def multiply(first_number: float, second_number: float) -> float:
    """Mnoży dwie liczby i zwraca wynik."""
    return first_number * second_number


def divide(first_number: float, second_number: float) -> float:
    """Dzieli pierwszą liczbę przez drugą i zwraca wynik.

    Podnosi ValueError w przypadku dzielenia przez zero.
    """
    if second_number == 0:
        # Zgłoszenie błędu przy dzieleniu przez zero
        raise ValueError("Nie można dzielić przez zero.")
    return first_number / second_number


def main() -> None:
    """Główna funkcja pobierająca znak operacji oraz liczby od użytkownika."""
    allowed_operations = ("+", "-", "*", "/")
    operation = input("Wybierz operację (+, -, *, /): ").strip()

    if operation not in allowed_operations:
        print(f"Nieprawidłowy znak operacji: '{operation}'. Dozwolone: +, -, *, /")
        return

    try:
        first_number = float(input("Podaj pierwszą liczbę: "))
        second_number = float(input("Podaj drugą liczbę: "))
    except ValueError:
        print("Błąd: Wprowadzona wartość nie jest poprawną liczbą.")
        return

    try:
        if operation == "+":
            result = add(first_number, second_number)
        elif operation == "-":
            result = subtract(first_number, second_number)
        elif operation == "*":
            result = multiply(first_number, second_number)
        elif operation == "/":
            result = divide(first_number, second_number)

        print(f"Wynik: {first_number} {operation} {second_number} = {result}")
    except ValueError as error:
        print(f"Błąd: {error}")


if __name__ == "__main__":
    main()

