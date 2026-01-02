from tkinter import Tk, Canvas, Label, Button, Frame
from PIL import Image, ImageTk
import requests
from html import unescape
from question_model import Question

THEME_COLOR = "#375362"
ACCENT_COLOR = "#4A90A4"
SUCCESS_COLOR = "#4CAF50"
ERROR_COLOR = "#E74C3C"
CARD_COLOR = "#FFFFFF"


class QuizInterface:
    
    def __init__(self, quiz_brain):
        self.quiz = quiz_brain
        self.total_questions = len(quiz_brain.question_list)
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(bg=THEME_COLOR, padx=40, pady=40)
        self.window.resizable(False, False)
        
        # Configure grid weights for centering
        self.window.columnconfigure(0, weight=1)
        
        # Title label
        self.title_label = Label(
            text="QUIZZLER",
            fg="white",
            bg=THEME_COLOR,
            font=("Arial", 28, "bold"),
            pady=5
        )
        self.title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Score frame for better layout
        self.score_frame = Frame(self.window, bg=THEME_COLOR)
        self.score_frame.grid(row=1, column=0, pady=(0, 15), sticky="ew")
        self.score_frame.columnconfigure(0, weight=1)
        self.score_frame.columnconfigure(1, weight=1)
        
        # Progress label
        self.progress_label = Label(
            self.score_frame,
            text="Question 1 of 10",
            fg="#B0C4DE",
            bg=THEME_COLOR,
            font=("Arial", 12)
        )
        self.progress_label.grid(row=0, column=0, sticky="w")
        
        # Score label with modern styling
        self.score_label = Label(
            self.score_frame,
            text="Score: 0/0",
            fg="white",
            bg=THEME_COLOR,
            font=("Arial", 16, "bold")
        )
        self.score_label.grid(row=0, column=1, sticky="e")
        
        # Canvas container frame for shadow effect
        self.canvas_frame = Frame(self.window, bg="#2C3E50", padx=3, pady=3)
        self.canvas_frame.grid(row=2, column=0, pady=(0, 25))
        
        # Canvas for the question with modern design
        self.canvas = Canvas(
            self.canvas_frame,
            width=420,
            height=280,
            bg=CARD_COLOR,
            highlightthickness=0
        )
        self.canvas.pack()
        self.question_text = self.canvas.create_text(
            210,
            140,
            width=380,
            text="",
            fill=THEME_COLOR,
            font=("Georgia", 18, "italic"),
            justify="center"
        )
        
        # Load and prepare images
        self.true_img = ImageTk.PhotoImage(Image.open("images/true.png").resize((100, 97), Image.Resampling.LANCZOS))
        self.false_img = ImageTk.PhotoImage(Image.open("images/false.png").resize((100, 97), Image.Resampling.LANCZOS))
        
        # Button frame for even spacing
        self.button_frame = Frame(self.window, bg=THEME_COLOR)
        self.button_frame.grid(row=3, column=0)
        
        # True button with image
        self.true_button = Button(
            self.button_frame,
            image=self.true_img,
            bg=THEME_COLOR,
            bd=0,
            highlightthickness=0,
            activebackground=THEME_COLOR,
            command=self.on_true_click,
            cursor="hand2"
        )
        self.true_button.grid(row=0, column=0, padx=50)
        
        # False button with image
        self.false_button = Button(
            self.button_frame,
            image=self.false_img,
            bg=THEME_COLOR,
            bd=0,
            highlightthickness=0,
            activebackground=THEME_COLOR,
            command=self.on_false_click,
            cursor="hand2"
        )
        self.false_button.grid(row=0, column=1, padx=50)
        
        # Try Again button (hidden initially)
        self.try_again_button = Button(
            self.window,
            text="🔄  Play Again",
            font=("Arial", 16, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            padx=30,
            pady=12,
            bd=0,
            cursor="hand2",
            activebackground="#3A7A94",
            activeforeground="white",
            command=self.restart_quiz
        )
        
        self.get_next_question()
        
        self.window.mainloop()
    
    def get_next_question(self):
        self.canvas.config(bg=CARD_COLOR)
        self.score_label.config(text=f"Score: {self.quiz.score}/{self.quiz.question_number}")
        
        if self.quiz.still_has_questions():
            self.quiz.next_question()
            self.progress_label.config(text=f"Question {self.quiz.question_number} of {self.total_questions}")
            q_text = self.quiz.current_question.text
            self.canvas.itemconfig(self.question_text, text=q_text, font=("Georgia", 18, "italic"), fill=THEME_COLOR)
        else:
            # Calculate percentage
            percentage = int((self.quiz.score / self.quiz.question_number) * 100)
            if percentage >= 80:
                message = "🏆 Excellent!"
                msg_color = SUCCESS_COLOR
            elif percentage >= 60:
                message = "👍 Good Job!"
                msg_color = ACCENT_COLOR
            else:
                message = "📚 Keep Learning!"
                msg_color = ERROR_COLOR
            
            self.progress_label.config(text="Quiz Complete!")
            self.canvas.itemconfig(
                self.question_text,
                text=f"{message}\n\nYou scored\n{self.quiz.score} out of {self.quiz.question_number}\n\n{percentage}%",
                font=("Arial", 24, "bold"),
                fill=msg_color
            )
            self.button_frame.grid_forget()
            self.try_again_button.grid(row=3, column=0, pady=10)
    
    def on_true_click(self):
        self.give_feedback(self.quiz.check_answer("True"))
    
    def on_false_click(self):
        self.give_feedback(self.quiz.check_answer("False"))
    
    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg=SUCCESS_COLOR)
        else:
            self.canvas.config(bg=ERROR_COLOR)
        
        self.score_label.config(text=f"Score: {self.quiz.score}/{self.quiz.question_number}")
        self.window.after(1000, self.get_next_question)
    
    def fetch_new_questions(self):
        """Fetch a new set of questions from the API"""
        url = "https://opentdb.com/api.php?amount=10&type=boolean"
        response = requests.get(url)
        response.raise_for_status()
        question_data = response.json()["results"]
        
        question_bank = []
        for question in question_data:
            question_text = unescape(question["question"])
            question_answer = question["correct_answer"]
            new_question = Question(question_text, question_answer)
            question_bank.append(new_question)
        
        return question_bank
    
    def restart_quiz(self):
        # Show loading state
        self.canvas.itemconfig(self.question_text, text="Loading new questions...", font=("Arial", 18, "italic"), fill=THEME_COLOR)
        self.try_again_button.grid_forget()
        self.window.update()
        
        # Fetch new questions
        new_questions = self.fetch_new_questions()
        self.quiz.question_list = new_questions
        self.total_questions = len(new_questions)
        
        # Reset quiz state
        self.quiz.question_number = 0
        self.quiz.score = 0
        self.quiz.current_question = None
        
        # Show quiz buttons
        self.button_frame.grid(row=3, column=0)
        
        # Reset labels and start quiz
        self.score_label.config(text="Score: 0/0")
        self.progress_label.config(text=f"Question 1 of {self.total_questions}")
        self.get_next_question()
