# Tarot Card Reading Application

A comprehensive tarot card reading application with multiple interfaces and full 78-card deck support.

## 🔮 Features

- **Complete 78-card tarot deck** with Major and Minor Arcana
- **Multiple reading types**: Single Card, Three Card (Past/Present/Future), Celtic Cross (10 cards)
- **Multiple interfaces**: Desktop GUI (Tkinter), Web App (Streamlit), Console
- **Save/Load functionality** for readings (.rdg format)
- **Card reversal mechanics** for deeper interpretations
- **Professional card meanings** and detailed interpretations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

```bash
# Clone or download the project
cd path/to/tarot-card-reader

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

#### Console Version (Default)
```bash
python src/main.py
```

#### Desktop GUI (Tkinter)
```bash
python src/main.py --gui
```

#### Web Application (Streamlit)
```bash
python src/main.py --web
# or directly:
streamlit run src/tarot_streamlit.py
```

## 📁 Project Structure

```
├── src/
│   ├── tarot_core.py       # Core tarot card classes and logic
│   ├── tarot_tkinter.py    # Desktop GUI application
│   ├── tarot_streamlit.py  # Web application
│   ├── main.py             # Main entry point with CLI
│   └── __init__.py
├── tests/                  # Unit tests (42 comprehensive tests)
├── docs/                   # Documentation
├── data/                   # Data folder (currently empty - cards generated programmatically)
├── notebooks/              # Original Jupyter notebook
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 📊 Data Sources

This tarot application is completely self-contained and does not require external datasets. The complete 78-card tarot deck (Major and Minor Arcana) with descriptions and meanings is generated programmatically within the application.

**Note**: If you need to reference the original development environment's data folder, it was located at:
`/mnt/c/Desktop/work for claude/google_colab/data/`

## 🎴 Reading Types

### Single Card Reading
Perfect for daily guidance or quick insights into specific questions.

### Three Card Reading
Explores Past, Present, and Future aspects of your situation:
- **Past**: What has influenced your current situation
- **Present**: Current circumstances and immediate factors
- **Future**: Potential outcomes and what to expect

### Celtic Cross Reading
A comprehensive 10-card spread providing deep insights:
1. Present Situation
2. Challenge/Cross
3. Distant Past/Foundation
4. Recent Past
5. Possible Outcome
6. Near Future
7. Your Approach
8. External Influences
9. Hopes and Fears
10. Final Outcome

## 💻 Usage Examples

### Console Interface
```python
from src.tarot_core import TarotReading

# Create a reading session
tarot = TarotReading()

# Perform a single card reading
reading = tarot.single_card_reading()
print(reading['interpretation'])

# Save the reading
tarot.save_reading('my_reading.rdg', reading)
```

### GUI Integration
```python
from src.tarot_tkinter import TarotApp
import tkinter as tk

# Create and run the desktop application
root = tk.Tk()
app = TarotApp(root)
root.mainloop()
```

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
python -m pytest tests/
```

## 📊 Technical Details

### Core Classes

- **TarotCard**: Represents individual cards with names, descriptions, and reversed states
- **TarotDeck**: Manages the complete 78-card deck with shuffling and drawing
- **TarotReading**: Handles different reading types and interpretations

### Supported File Formats
- **.rdg**: Custom reading format (JSON-based)
- **.json**: Standard JSON format for readings

### Dependencies
- `tkinter`: Desktop GUI (usually included with Python)
- `streamlit`: Web interface
- `pillow`: Image processing (future card image support)
- `json`: Reading save/load functionality

## 🎯 Development

### Adding New Reading Types
1. Add the reading method to `TarotReading` class in `tarot_core.py`
2. Update the interfaces (`tarot_tkinter.py`, `tarot_streamlit.py`, `main.py`)
3. Add comprehensive tests

### Adding Card Images
1. Place card images in an `images/` directory
2. Update `TarotCard.image_file` paths during deck initialization
3. Modify the display methods in GUI applications

## 🔧 Troubleshooting

### Common Issues

**Tkinter not available**: 
- On Linux: `sudo apt-get install python3-tk`
- On macOS: Included with Python from python.org

**Streamlit not starting**:
- Ensure Streamlit is installed: `pip install streamlit`
- Check firewall settings for port 8501

**Reading files not loading**:
- Ensure files are in valid JSON format
- Check file permissions

## 📜 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For questions, issues, or suggestions, please create an issue in the project repository.

---

*"The cards are a doorway to your intuition. Trust what resonates with you and use these readings as guidance for your personal journey."*