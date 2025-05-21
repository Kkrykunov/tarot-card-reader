"""
Unit tests for the main entry point and CLI functionality.

Tests the command-line interface and argument parsing.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import main


class TestMainCLI(unittest.TestCase):
    """Test cases for the main CLI functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.original_argv = sys.argv.copy()
    
    def tearDown(self):
        """Clean up after tests."""
        sys.argv = self.original_argv
    
    @patch('sys.argv', ['main.py', '--help'])
    def test_help_argument(self):
        """Test that help is displayed correctly."""
        with self.assertRaises(SystemExit):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                main.main()
            output = mock_stdout.getvalue()
            self.assertIn('Tarot Card Reading Application', output)
            self.assertIn('--gui', output)
            self.assertIn('--web', output)
    
    @patch('main.run_tkinter')
    @patch('sys.argv', ['main.py', '--gui'])
    def test_gui_argument(self, mock_run_tkinter):
        """Test that GUI mode is triggered correctly."""
        main.main()
        mock_run_tkinter.assert_called_once()
    
    @patch('main.run_streamlit')
    @patch('sys.argv', ['main.py', '--web'])
    def test_web_argument(self, mock_run_streamlit):
        """Test that web mode is triggered correctly."""
        main.main()
        mock_run_streamlit.assert_called_once()
    
    @patch('main.console_reading')
    @patch('sys.argv', ['main.py'])
    def test_default_console_mode(self, mock_console_reading):
        """Test that console mode is the default."""
        main.main()
        mock_console_reading.assert_called_once()
    
    @patch('main.console_reading')
    @patch('sys.argv', ['main.py', '--console'])
    def test_explicit_console_argument(self, mock_console_reading):
        """Test explicit console argument."""
        main.main()
        mock_console_reading.assert_called_once()


class TestRunFunctions(unittest.TestCase):
    """Test cases for the run functions."""
    
    @patch('subprocess.run')
    @patch('sys.executable', '/usr/bin/python')
    def test_run_streamlit(self, mock_subprocess_run):
        """Test running Streamlit application."""
        main.run_streamlit()
        mock_subprocess_run.assert_called_once_with([
            '/usr/bin/python', '-m', 'streamlit', 'run', 'tarot_streamlit.py'
        ])
    
    @patch('builtins.print')
    @patch('subprocess.run', side_effect=ImportError("Streamlit not found"))
    def test_run_streamlit_import_error(self, mock_subprocess_run, mock_print):
        """Test Streamlit run with import error."""
        with patch('importlib.import_module', side_effect=ImportError()):
            main.run_streamlit()
        mock_print.assert_called()
        # Should print error message about Streamlit not being installed
        args, kwargs = mock_print.call_args
        self.assertIn('Streamlit', args[0])
    
    @patch('builtins.print')
    def test_run_tkinter_success(self, mock_print):
        """Test successful Tkinter run."""
        # Mock the import and function call
        mock_module = MagicMock()
        mock_module.main = MagicMock()
        
        with patch.dict('sys.modules', {'tarot_tkinter': mock_module}):
            main.run_tkinter()
        
        # Should print starting message and call the main function
        mock_print.assert_any_call("Starting Tkinter Desktop Application...")
        mock_module.main.assert_called_once()
    
    @patch('builtins.print')
    def test_run_tkinter_import_error(self, mock_print):
        """Test Tkinter run with import error."""
        with patch('importlib.import_module', side_effect=ImportError("No module named tkinter")):
            main.run_tkinter()
        # Should print error message
        mock_print.assert_called()


class TestConsoleReading(unittest.TestCase):
    """Test cases for console reading functionality."""
    
    @patch('builtins.input', side_effect=['4'])  # Exit immediately
    @patch('builtins.print')
    def test_console_reading_exit(self, mock_print, mock_input):
        """Test console reading exits cleanly."""
        main.console_reading()
        # Should print welcome message and exit message
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        welcome_printed = any('Welcome to the Tarot Card Reader' in call for call in print_calls)
        exit_printed = any('Thank you for using' in call for call in print_calls)
        self.assertTrue(welcome_printed)
        self.assertTrue(exit_printed)
    
    @patch('builtins.input', side_effect=['1', 'n', '4'])  # Single card, don't save, exit
    @patch('builtins.print')
    def test_console_reading_single_card(self, mock_print, mock_input):
        """Test console reading performs single card reading."""
        main.console_reading()
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Should show reading result
        reading_shown = any('Single Card Reading' in call for call in print_calls)
        self.assertTrue(reading_shown)
    
    @patch('builtins.input', side_effect=['5', '1', 'n', '4'])  # Invalid choice, then valid
    @patch('builtins.print')
    def test_console_reading_invalid_choice(self, mock_print, mock_input):
        """Test console reading handles invalid choices."""
        main.console_reading()
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Should show error message for invalid choice
        error_shown = any('Invalid choice' in call for call in print_calls)
        self.assertTrue(error_shown)
    
    @patch('builtins.input', side_effect=KeyboardInterrupt())
    @patch('builtins.print')
    def test_console_reading_keyboard_interrupt(self, mock_print, mock_input):
        """Test console reading handles keyboard interrupt."""
        main.console_reading()
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Should handle KeyboardInterrupt gracefully
        exit_printed = any('Thank you for using' in call for call in print_calls)
        self.assertTrue(exit_printed)
    
    @patch('builtins.input', side_effect=['2', 'y', 'test_reading', '4'])
    @patch('builtins.print')
    @patch('main.TarotReading')
    def test_console_reading_save_file(self, mock_tarot_reading, mock_print, mock_input):
        """Test console reading saves file."""
        # Mock the TarotReading instance
        mock_instance = MagicMock()
        mock_tarot_reading.return_value = mock_instance
        mock_instance.three_card_reading.return_value = {
            'type': 'Three Card',
            'interpretation': 'Test interpretation'
        }
        mock_instance.save_reading.return_value = True
        
        main.console_reading()
        
        # Should call save_reading with correct filename
        mock_instance.save_reading.assert_called_with('test_reading.rdg', mock_instance.three_card_reading.return_value)


if __name__ == '__main__':
    unittest.main()