"""
Tarot Card Reading Application - Main Entry Point

Command-line interface for running different versions of the tarot application.
Supports Tkinter desktop GUI, Streamlit web app, and console-based readings.
"""

import sys
import argparse
from typing import Optional
from tarot_core import TarotReading


def console_reading():
    """Run a console-based tarot reading."""
    print("🔮 Welcome to the Tarot Card Reader (Console Mode)")
    print("=" * 50)
    
    tarot = TarotReading()
    
    while True:
        print("\nAvailable Reading Types:")
        print("1. Single Card Reading")
        print("2. Three Card Reading (Past, Present, Future)")
        print("3. Celtic Cross Reading (10 cards)")
        print("4. Exit")
        
        try:
            choice = input("\nSelect an option (1-4): ").strip()
            
            if choice == "1":
                reading = tarot.single_card_reading()
            elif choice == "2":
                reading = tarot.three_card_reading()
            elif choice == "3":
                reading = tarot.celtic_cross_reading()
            elif choice == "4":
                print("Thank you for using the Tarot Card Reader!")
                break
            else:
                print("Invalid choice. Please select 1-4.")
                continue
            
            if "error" in reading:
                print(f"Error: {reading['error']}")
                continue
            
            # Display the reading
            print(f"\n{reading['type']} Reading")
            print("=" * 50)
            print(reading['interpretation'])
            print("=" * 50)
            
            # Ask if user wants to save
            save_choice = input("\nSave this reading? (y/n): ").strip().lower()
            if save_choice == 'y':
                filename = input("Enter filename (without extension): ").strip()
                if filename:
                    filename += ".rdg"
                    if tarot.save_reading(filename, reading):
                        print(f"Reading saved to {filename}")
                    else:
                        print("Failed to save reading")
        
        except KeyboardInterrupt:
            print("\n\nThank you for using the Tarot Card Reader!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


def run_tkinter():
    """Run the Tkinter desktop application."""
    try:
        from tarot_tkinter import main as tkinter_main
        print("Starting Tkinter Desktop Application...")
        tkinter_main()
    except ImportError as e:
        print(f"Error importing Tkinter components: {e}")
        print("Make sure you have tkinter installed and available.")
    except Exception as e:
        print(f"Error running Tkinter application: {e}")


def run_streamlit():
    """Run the Streamlit web application."""
    try:
        import subprocess
        import sys
        print("Starting Streamlit Web Application...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "tarot_streamlit.py"])
    except ImportError:
        print("Streamlit is not installed. Please install it with: pip install streamlit")
    except Exception as e:
        print(f"Error running Streamlit application: {e}")


def main():
    """Main entry point with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Tarot Card Reading Application",
        epilog="Examples:\n"
               "  python main.py              # Run console version\n"
               "  python main.py --gui        # Run Tkinter GUI\n"
               "  python main.py --web        # Run Streamlit web app\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--gui", "-g",
        action="store_true",
        help="Run the Tkinter desktop GUI application"
    )
    group.add_argument(
        "--web", "-w",
        action="store_true",
        help="Run the Streamlit web application"
    )
    group.add_argument(
        "--console", "-c",
        action="store_true",
        help="Run the console-based application (default)"
    )
    
    args = parser.parse_args()
    
    if args.gui:
        run_tkinter()
    elif args.web:
        run_streamlit()
    else:
        console_reading()


if __name__ == "__main__":
    main()