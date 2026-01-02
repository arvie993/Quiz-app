# Quizzler - Quiz Application

A modern, interactive True/False quiz application built with Python and Tkinter. Test your knowledge with questions fetched from the Open Trivia Database API or use the built-in question dataset.

## Features

✨ **Interactive GUI** - Clean and modern interface built with Tkinter
🎯 **True/False Questions** - Simple and engaging question format
📊 **Score Tracking** - Real-time score display and progress tracking
🌐 **API Integration** - Fetches questions from Open Trivia Database (opentdb.com)
🎨 **Modern Design** - Color-coded feedback with visual styling
📈 **Progress Indicator** - Shows current question number and total questions

## Project Structure

```
quizzler-app-start/
├── main.py                  # Entry point - fetches questions and initializes the quiz
├── quiz_brain.py           # Core quiz logic and score management
├── question_model.py       # Question data model
├── ui.py                   # GUI implementation using Tkinter
├── data.py                 # Local question dataset (fallback)
├── images/                 # Button images (true.png, false.png)
└── README.md               # This file
```

## Requirements

- Python 3.7+
- `tkinter` (usually comes with Python)
- `Pillow` (PIL) for image handling
- `requests` for API calls

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Quiz-app.git
cd Quiz-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install pillow requests
```

3. Ensure you have the `images/` folder with:
   - `true.png` - Image for the True button
   - `false.png` - Image for the False button

## Usage

Run the application:
```bash
python main.py
```

### How to Play

1. Launch the application
2. Read the question displayed on the card
3. Click **True** or **False** button to answer
4. Your score updates in real-time
5. Progress indicator shows your current position
6. After all questions, the final score is displayed

## Code Components

### `main.py`
- Fetches 10 random True/False questions from the Open Trivia Database API
- Decodes HTML entities in questions
- Creates a `QuizBrain` instance and initializes the GUI

### `question_model.py`
- `Question` class: Stores question text and correct answer

### `quiz_brain.py`
- `QuizBrain` class: Manages quiz logic
  - `still_has_questions()` - Checks if more questions remain
  - `next_question()` - Displays the next question
  - `check_answer()` - Validates user's answer and updates score

### `ui.py`
- `QuizInterface` class: Creates and manages the Tkinter GUI
  - Displays questions on a canvas
  - Handles True/False button clicks
  - Updates score and progress labels
  - Provides visual feedback for correct/incorrect answers

### `data.py`
- Local fallback dataset with 12 sample True/False questions
- Used when API is unavailable

## Features in Detail

### Score Tracking
- Real-time score display in the format "Score: X/Y"
- Tracks correct answers throughout the quiz

### Progress Indicator
- Shows "Question X of 10" at the top
- Helps users understand how far into the quiz they are

### Visual Feedback
- Card background changes color based on answer correctness
- Green flash for correct answers
- Red flash for incorrect answers
- Smooth transitions between questions

### Responsive Design
- Fixed window size (non-resizable)
- Proper padding and spacing
- Centered layout with grid management

## Future Enhancements

- [ ] Add difficulty level selection
- [ ] Implement different quiz categories
- [ ] Add timer for each question
- [ ] Save quiz history and statistics
- [ ] Add sound effects for correct/incorrect answers
- [ ] Support multiple languages
- [ ] Create a high scores leaderboard

## API Reference

This app uses the **Open Trivia Database API** (free):
- **Endpoint**: `https://opentdb.com/api.php`
- **Parameters**: 
  - `amount=10` - Number of questions
  - `type=boolean` - Question type (True/False)

Learn more: [https://opentdb.com/api_config.php](https://opentdb.com/api_config.php)

## Troubleshooting

### API Connection Issues
If you can't fetch questions from the API:
- Check your internet connection
- The app will fall back to the local dataset in `data.py`

### Missing Images
- Ensure `images/true.png` and `images/false.png` exist
- Images should be 100x97 pixels for best display

### Tkinter Not Found
On some Linux systems, you may need to install tkinter separately:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

## License

This project is open source. Feel free to fork, modify, and distribute.

## Author
Aravind + Claude

_Created as part of the 100 Days of Python challenge._

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

---

Enjoy testing your knowledge with Quizzler! 🎓
