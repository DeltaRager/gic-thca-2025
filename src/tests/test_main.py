import io
import tempfile
from pathlib import Path
from unittest.mock import patch

from main import show_format_help


class TestMainFormatHelp:
    def test_show_format_help(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            show_format_help()
            output = mock_stdout.getvalue()
            assert "ERROR: Invalid input format!" in output
            assert "Correct format:" in output
            assert "10 10" in output
            assert "Directions: N (North)" in output
            assert "Commands: F (Forward)" in output


class TestMainInputValidation:
    def test_valid_input_parsing(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("5 5\n\nA\n1 2 N\nFFR\n\nB\n3 3 S\n")
            temp_path = f.name

        with patch("sys.argv", ["main.py", temp_path]):
            with patch("settings.settings.log_level", "critical"):
                try:
                    from main import main

                    main()
                    success = True
                except SystemExit as e:
                    success = e.code == 0

        Path(temp_path).unlink()
        assert success

    def test_car_without_commands(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("5 5\nA\n1 2 N\n\nB\n3 3 S\nF")
            temp_path = f.name

        with patch("sys.argv", ["main.py", temp_path]):
            with patch("settings.settings.log_level", "critical"):
                try:
                    from main import main

                    main()
                    success = True
                except SystemExit as e:
                    success = e.code == 0

        Path(temp_path).unlink()
        assert success

    def test_empty_commands(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("3 3\nA\n1 1 N\n")
            temp_path = f.name

        with patch("sys.argv", ["main.py", temp_path]):
            with patch("settings.settings.log_level", "critical"):
                try:
                    from main import main

                    main()
                    success = True
                except SystemExit as e:
                    success = e.code == 0

        Path(temp_path).unlink()
        assert success
