"""Moduł do zarządzania listą zadań (TODO)."""

import json
import os
import sys

DATA_FILE = "zadania.json"


def load_tasks():
    """Wczytuje listę zadań z pliku JSON.

    Returns:
        list: Lista słowników reprezentujących zadania.
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    """Zapisuje listę zadań do pliku JSON.

    Args:
        tasks (list): Lista zadań do zapisania.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)


def add_task(title):
    """Dodaje nowe zadanie i wypisuje jego numer.

    Args:
        title (str): Treść zadania.
    """
    tasks = load_tasks()
    new_task = {
        "title": title,
        "done": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    task_number = len(tasks)
    print(f"Dodano zadanie {task_number}: {title}")


def list_tasks():
    """Wypisuje wszystkie zadania w formacie: numer, [ ]/[x], treść."""
    tasks = load_tasks()
    if not tasks:
        print("Brak zadań.")
        return

    for index, task in enumerate(tasks, start=1):
        status = "[x]" if task.get("done") else "[ ]"
        print(f"{index}. {status} {task.get('title')}")


def mark_done(task_number_str):
    """Oznacza zadanie o podanym numerze jako wykonane.

    Args:
        task_number_str (str): Numer zadania jako ciąg znaków.
    """
    try:
        task_number = int(task_number_str)
    except ValueError:
        print(f"Błąd: '{task_number_str}' nie jest poprawnym numerem zadania.")
        return

    tasks = load_tasks()
    if task_number < 1 or task_number > len(tasks):
        print(f"Błąd: Zadanie o numerze {task_number} nie istnieje.")
        return

    tasks[task_number - 1]["done"] = True
    save_tasks(tasks)
    print(f"Zadanie {task_number} oznaczono jako wykonane.")


def delete_task(task_number_str):
    """Usuwa zadanie o podanym numerze.

    Args:
        task_number_str (str): Numer zadania jako ciąg znaków.
    """
    try:
        task_number = int(task_number_str)
    except ValueError:
        print(f"Błąd: '{task_number_str}' nie jest poprawnym numerem zadania.")
        return

    tasks = load_tasks()
    if task_number < 1 or task_number > len(tasks):
        print(f"Błąd: Zadanie o numerze {task_number} nie istnieje.")
        return

    removed_task = tasks.pop(task_number - 1)
    save_tasks(tasks)
    print(f"Usunięto zadanie {task_number}: {removed_task.get('title')}")


def main():
    """Główna funkcja przetwarzająca argumenty wiersza poleceń."""
    if len(sys.argv) < 2:
        print("Użycie: python todo.py [dodaj|lista|zrobione|usun] [argumenty]")
        return

    command = sys.argv[1].lower()

    if command == "dodaj":
        if len(sys.argv) < 3:
            print("Błąd: Podaj treść zadania. Użycie: python todo.py dodaj \"Treść zadania\"")
            return
        title = " ".join(sys.argv[2:])
        add_task(title)
    elif command == "lista":
        list_tasks()
    elif command == "zrobione":
        if len(sys.argv) < 3:
            print("Błąd: Podaj numer zadania. Użycie: python todo.py zrobione <numer>")
            return
        mark_done(sys.argv[2])
    elif command == "usun":
        if len(sys.argv) < 3:
            print("Błąd: Podaj numer zadania. Użycie: python todo.py usun <numer>")
            return
        delete_task(sys.argv[2])
    else:
        print(f"Błąd: Nieznana komenda '{command}'. Dostępne komendy: dodaj, lista, zrobione, usun.")


if __name__ == "__main__":
    main()

