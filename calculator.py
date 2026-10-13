"""Moduł kalkulatora wykonujący podstawowe operacje arytmetyczne."""


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

    Podnosi ValueError w przypadku próby dzielenia przez zero.
    """
    if second_number == 0:
        # Zgłoszenie błędu przy dzieleniu przez zero
        raise ValueError("Nie można dzielić przez zero.")
    return first_number / second_number


def main() -> None:
    """Główna funkcja uruchamiająca prosty interfejs tekstowy kalkulatora."""
    print("Prosty kalkulator")
    print("1. Dodawanie")
    print("2. Odejmowanie")
    print("3. Mnożenie")
    print("4. Dzielenie")

    choice = input("Wybierz operację (1/2/3/4): ")
    if choice not in ("1", "2", "3", "4"):
        print("Nieprawidłowy wybór.")
        return

    try:
        first_input = float(input("Podaj pierwszą liczbę: "))
        second_input = float(input("Podaj drugą liczbę: "))
    except ValueError:
        print("Błąd: Wprowadzona wartość nie jest liczbą.")
        return

    try:
        if choice == "1":
            result = add(first_input, second_input)
        elif choice == "2":
            result = subtract(first_input, second_input)
        elif choice == "3":
            result = multiply(first_input, second_input)
        elif choice == "4":
            result = divide(first_input, second_input)
        print(f"Wynik: {result}")
    except ValueError as error:
        print(f"Błąd operacji: {error}")


if __name__ == "__main__":
    main()

