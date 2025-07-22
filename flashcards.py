# Rewriting the Phase 7 tkinter GUI app after kernel reset

import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import random
import csv
import requests
import html  # To decode HTML entities from the API

FLASHCARD_FILE = "flashcards.csv"

def load_flashcards():
    flashcards = []
    if os.path.exists(FLASHCARD_FILE):
        try:
            with open(FLASHCARD_FILE, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    flashcards.append({
                        "question": row.get("question", ""),
                        "answer": row.get("answer", ""),
                        "category": row.get("category", ""),
                        "reviewed": int(row.get("reviewed", 0)),
                        "correct": int(row.get("correct", 0))
                    })
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load flashcards: {e}")
    return flashcards

def save_flashcards():
    with open(FLASHCARD_FILE, "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ["question", "answer", "category", "reviewed", "correct"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for card in flashcards:
            writer.writerow(card)

def add_flashcard():
    question = simpledialog.askstring("Add Flashcard", "Enter the question:")
    if not question:
        return
    answer = simpledialog.askstring("Add Flashcard", "Enter the answer:")
    if not answer:
        return
    category = simpledialog.askstring("Add Flashcard", "Enter the category:")
    if not category:
        return

    flashcards.append({
        "question": question,
        "answer": answer,
        "category": category,
        "reviewed": 0,
        "correct": 0
    })
    save_flashcards()
    messagebox.showinfo("Saved", "Flashcard added!")

def load_trivia_questions():
    try:
        amount = simpledialog.askinteger("Load Trivia", "How many trivia questions (1–50)?", minvalue=1, maxvalue=50)
        if not amount:
            return
        response = requests.get(f"https://opentdb.com/api.php?amount={amount}&type=multiple")
        data = response.json()
        if data["response_code"] != 0:
            raise Exception("Failed to fetch trivia questions.")

        added = 0
        for item in data["results"]:
            question = html.unescape(item["question"])
            answer = html.unescape(item["correct_answer"])
            category = html.unescape(item["category"])
            flashcards.append({
                "question": question,
                "answer": answer,
                "category": category,
                "reviewed": 0,
                "correct": 0
            })
            added += 1
        save_flashcards()
        messagebox.showinfo("Success", f"{added} trivia flashcards added.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load trivia: {e}")

def start_quiz():
    global quiz_cards, quiz_index, quiz_score
    category = simpledialog.askstring("Quiz Category", "Enter a category (or leave blank for all):")
    quiz_cards = [c for c in flashcards if category.lower() in c["category"].lower()] if category else flashcards[:]
    if not quiz_cards:
        messagebox.showinfo("Info", "No flashcards found.")
        return
    quiz_cards.sort(key=lambda c: (c["correct"] / c["reviewed"]) if c["reviewed"] else 0)
    quiz_index = 0
    quiz_score = 0
    show_quiz_card()

def show_quiz_card():
    global quiz_index
    if quiz_index < len(quiz_cards):
        card = quiz_cards[quiz_index]
        question_label.config(text=f"Q: {card['question']}")
        answer_entry.delete(0, tk.END)
        submit_button.config(state=tk.NORMAL)
    else:
        question_label.config(text=f"Quiz complete! Score: {quiz_score}/{len(quiz_cards)}")
        submit_button.config(state=tk.DISABLED)
        save_flashcards()

def submit_answer():
    global quiz_index, quiz_score
    card = quiz_cards[quiz_index]
    user_ans = answer_entry.get().strip().lower()
    correct_ans = card["answer"].strip().lower()
    card["reviewed"] += 1
    if user_ans == correct_ans:
        card["correct"] += 1
        quiz_score += 1
        messagebox.showinfo("Correct", "✅ Correct!")
    else:
        messagebox.showinfo("Incorrect", f"❌ Incorrect.\nCorrect answer: {card['answer']}")
    quiz_index += 1
    show_quiz_card()

def manage_flashcards():
    if not flashcards:
        messagebox.showinfo("Info", "No flashcards to manage.")
        return
    msg = ""
    for i, c in enumerate(flashcards, 1):
        acc = f"{(c['correct']/c['reviewed']*100):.1f}%" if c['reviewed'] else "N/A"
        msg += f"{i}. [{c['category']}] {c['question']} (Accuracy: {acc})\n"
    messagebox.showinfo("Flashcards", msg)

flashcards = load_flashcards()
quiz_cards = []
quiz_index = 0
quiz_score = 0

# GUI Setup
root = tk.Tk()
root.title("Flashcard Quiz App")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Button(frame, text="Add Flashcard", command=add_flashcard, width=20).pack(pady=5)
tk.Button(frame, text="Start Quiz", command=start_quiz, width=20).pack(pady=5)
tk.Button(frame, text="Manage Flashcards", command=manage_flashcards, width=20).pack(pady=5)
tk.Button(frame, text="Load Trivia Questions", command=load_trivia_questions, width=20).pack(pady=5)

question_label = tk.Label(frame, text="Welcome to the Flashcard Quiz!", wraplength=400, justify="center")
question_label.pack(pady=10)

answer_entry = tk.Entry(frame, width=50)
answer_entry.pack(pady=5)

submit_button = tk.Button(frame, text="Submit Answer", command=submit_answer, state=tk.DISABLED)
submit_button.pack(pady=5)

root.mainloop()
