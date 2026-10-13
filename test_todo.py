"""Testy jednostkowe dla modułu todo.py."""

import json
import os
import unittest
from io import StringIO
from unittest.mock import patch

import todo


class TestTodoApp(unittest.TestCase):
    """Przypadki testowe dla aplikacji TODO."""

    def setUp(self):
        """Przygotowanie środowiska przed każdym testem."""
        self.test_file = "test_zadania.json"
        todo.DATA_FILE = self.test_file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Czyszczenie plików po każdym teście."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_task(self):
        """Testuje dodawanie zadania do bazy."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            todo.add_task("Kup mleko")
            output = mock_out.getvalue()

        self.assertIn("Dodano zadanie 1: Kup mleko", output)
        tasks = todo.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Kup mleko")
        self.assertFalse(tasks[0]["done"])

    def test_list_tasks(self):
        """Testuje wyświetlanie listy zadań."""
        todo.save_tasks([
            {"title": "Zadanie 1", "done": False},
            {"title": "Zadanie 2", "done": True}
        ])

        with patch("sys.stdout", new=StringIO()) as mock_out:
            todo.list_tasks()
            output = mock_out.getvalue()

        self.assertIn("1. [ ] Zadanie 1", output)
        self.assertIn("2. [x] Zadanie 2", output)

    def test_mark_done(self):
        """Testuje oznaczanie zadania jako wykonane."""
        todo.save_tasks([{"title": "Kup chleb", "done": False}])

        with patch("sys.stdout", new=StringIO()) as mock_out:
            todo.mark_done("1")
            output = mock_out.getvalue()

        self.assertIn("Zadanie 1 oznaczono jako wykonane.", output)
        tasks = todo.load_tasks()
        self.assertTrue(tasks[0]["done"])

    def test_mark_done_invalid_number(self):
        """Testuje reakcję na nieistniejący numer zadania."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            todo.mark_done("99")
            output = mock_out.getvalue()

        self.assertIn("Błąd: Zadanie o numerze 99 nie istnieje.", output)

    def test_delete_task(self):
        """Testuje usuwanie zadania."""
        todo.save_tasks([{"title": "Kup masło", "done": False}])

        with patch("sys.stdout", new=StringIO()) as mock_out:
            todo.delete_task("1")
            output = mock_out.getvalue()

        self.assertIn("Usunięto zadanie 1", output)
        tasks = todo.load_tasks()
        self.assertEqual(len(tasks), 0)

    def test_delete_task_invalid_number(self):
        """Testuje reakcję na nieistniejący numer przy usuwaniu."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            todo.delete_task("5")
            output = mock_out.getvalue()

        self.assertIn("Błąd: Zadanie o numerze 5 nie istnieje.", output)

    def test_load_tasks_missing_file(self):
        """Testuje wczytywanie zadań, gdy plik danych nie istnieje."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        tasks = todo.load_tasks()
        self.assertEqual(tasks, [])

    def test_load_tasks_corrupted_json(self):
        """Testuje wczytywanie zadań z uszkodzonego pliku JSON."""
        # Utworzenie uszkodzonego pliku JSON
        with open(self.test_file, "w", encoding="utf-8") as file:
            file.write("niepoprawny json")
        tasks = todo.load_tasks()
        self.assertEqual(tasks, [])

    def test_list_tasks_empty(self):
        """Testuje wyświetlanie pustej listy zadań."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            todo.list_tasks()
            output = mock_out.getvalue()

        self.assertIn("Brak zadań.", output)

    def test_mark_done_non_integer(self):
        """Testuje oznaczanie zadania, gdy podano niepoprawny format numeru."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            todo.mark_done("abc")
            output = mock_out.getvalue()

        self.assertIn("Błąd: 'abc' nie jest poprawnym numerem zadania.", output)

    def test_mark_done_zero_or_negative(self):
        """Testuje oznaczanie zadania dla numeru zerowego lub ujemnego."""
        todo.save_tasks([{"title": "Zadanie 1", "done": False}])
        with patch("sys.stdout", new=StringIO()) as mock_out:
            todo.mark_done("0")
            output = mock_out.getvalue()

        self.assertIn("Błąd: Zadanie o numerze 0 nie istnieje.", output)

    def test_delete_task_non_integer(self):
        """Testuje usuwanie zadania, gdy podano niepoprawny format numeru."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            todo.delete_task("xyz")
            output = mock_out.getvalue()

        self.assertIn("Błąd: 'xyz' nie jest poprawnym numerem zadania.", output)

    def test_delete_task_zero_or_negative(self):
        """Testuje usuwanie zadania dla numeru zerowego lub ujemnego."""
        todo.save_tasks([{"title": "Zadanie 1", "done": False}])
        with patch("sys.stdout", new=StringIO()) as mock_out:
            todo.delete_task("-1")
            output = mock_out.getvalue()

        self.assertIn("Błąd: Zadanie o numerze -1 nie istnieje.", output)

    def test_main_no_arguments(self):
        """Testuje wywołanie funkcji main bez argumentów."""
        with patch("sys.argv", ["todo.py"]):
            with patch("sys.stdout", new=StringIO()) as mock_out:
                todo.main()
                output = mock_out.getvalue()

        self.assertIn("Użycie: python todo.py [dodaj|lista|zrobione|usun] [argumenty]", output)

    def test_main_unknown_command(self):
        """Testuje wywołanie funkcji main z nieznaną komendą."""
        with patch("sys.argv", ["todo.py", "nieznana"]):
            with patch("sys.stdout", new=StringIO()) as mock_out:
                todo.main()
                output = mock_out.getvalue()

        self.assertIn("Błąd: Nieznana komenda 'nieznana'.", output)

    def test_main_add_task_without_title(self):
        """Testuje wywołanie komendy dodaj bez podania treści."""
        with patch("sys.argv", ["todo.py", "dodaj"]):
            with patch("sys.stdout", new=StringIO()) as mock_out:
                todo.main()
                output = mock_out.getvalue()

        self.assertIn("Błąd: Podaj treść zadania.", output)

    def test_main_add_task_success(self):
        """Testuje pomyślne dodanie zadania przez funkcję main."""
        with patch("sys.argv", ["todo.py", "dodaj", "Kup", "mleko"]):
            with patch("sys.stdout", new=StringIO()) as mock_out:
                todo.main()
                output = mock_out.getvalue()

        self.assertIn("Dodano zadanie 1: Kup mleko", output)
        tasks = todo.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Kup mleko")

    def test_main_list_tasks(self):
        """Testuje wyświetlanie zadań przez funkcję main."""
        todo.save_tasks([{"title": "Testowe zadanie", "done": False}])
        with patch("sys.argv", ["todo.py", "lista"]):
            with patch("sys.stdout", new=StringIO()) as mock_out:
                todo.main()
                output = mock_out.getvalue()

        self.assertIn("1. [ ] Testowe zadanie", output)

    def test_main_mark_done_without_number(self):
        """Testuje wywołanie komendy zrobione bez numeru zadania."""
        with patch("sys.argv", ["todo.py", "zrobione"]):
            with patch("sys.stdout", new=StringIO()) as mock_out:
                todo.main()
                output = mock_out.getvalue()

        self.assertIn("Błąd: Podaj numer zadania.", output)

    def test_main_mark_done_success(self):
        """Testuje pomyślne oznaczenie zadania przez funkcję main."""
        todo.save_tasks([{"title": "Zadanie", "done": False}])
        with patch("sys.argv", ["todo.py", "zrobione", "1"]):
            with patch("sys.stdout", new=StringIO()) as mock_out:
                todo.main()
                output = mock_out.getvalue()

        self.assertIn("Zadanie 1 oznaczono jako wykonane.", output)
        tasks = todo.load_tasks()
        self.assertTrue(tasks[0]["done"])

    def test_main_delete_without_number(self):
        """Testuje wywołanie komendy usun bez podania numeru."""
        with patch("sys.argv", ["todo.py", "usun"]):
            with patch("sys.stdout", new=StringIO()) as mock_out:
                todo.main()
                output = mock_out.getvalue()

        self.assertIn("Błąd: Podaj numer zadania.", output)

    def test_main_delete_success(self):
        """Testuje pomyślne usunięcie zadania przez funkcję main."""
        todo.save_tasks([{"title": "Do usunięcia", "done": False}])
        with patch("sys.argv", ["todo.py", "usun", "1"]):
            with patch("sys.stdout", new=StringIO()) as mock_out:
                todo.main()
                output = mock_out.getvalue()

        self.assertIn("Usunięto zadanie 1: Do usunięcia", output)
        tasks = todo.load_tasks()
        self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()


