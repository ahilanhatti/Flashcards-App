# flashcards.py

import json
import os
import random

FLASHCARD_FILE = "flashcards.json"

def load_flashcards():
    if os.path.exists(FLASHCARD_FILE):
        try:
            with open(FLASHCARD_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: flashcards.json is corrupted. Starting with empty set.")
    return []

def save_flashcards(flashcards):
    with open(FLASHCARD_FILE, "w") as f:
        json.dump(flashcards, f, indent=2)

def show_menu():
    print("\nFlashcard Quiz App")
    print("1. Add a flashcard")
    print("2. Review flashcards")
    print("3. Take a quiz")
    print("4. Quit")

def add_flashcard(flashcards):
    question = input("Enter the question: ").strip()
    answer = input("Enter the answer: ").strip()
    if not question or not answer:
        print("Both question and answer are required.")
        return

    for card in flashcards:
        if card["question"].lower() == question.lower():
            print("This question already exists. Skipping.")
            return

    flashcards.append({"question": question, "answer": answer})
    save_flashcards(flashcards)
    print("Flashcard added and saved!")

def review_flashcards(flashcards):
    if not flashcards:
        print("No flashcards to review.")
        return

    for i, card in enumerate(flashcards, 1):
        input(f"\nCard {i}: {card['question']} (press Enter to show answer)")
        print(f"Answer: {card['answer']}")

def take_quiz(flashcards):
    if not flashcards:
        print("No flashcards available to quiz.")
        return

    print("\nStarting quiz! Type your answers and press Enter.\n")
    score = 0
    missed_cards = []

    cards = flashcards.copy()
    random.shuffle(cards)

    for i, card in enumerate(cards, 1):
        print(f"Question {i}: {card['question']}")
        user_answer = input("Your answer: ").strip().lower()
        correct_answer = card["answer"].strip().lower()

        if user_answer == correct_answer:
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Incorrect. The correct answer was: {card['answer']}\n")
            missed_cards.append(card)

    print(f"Quiz complete! You scored {score}/{len(cards)} ({(score/len(cards)) * 100:.1f}%).")

    if missed_cards:
        retry = input("Would you like to retry the missed questions? (y/n): ").strip().lower()
        if retry == "y":
            take_quiz(missed_cards)

def main():
    flashcards = load_flashcards()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_flashcard(flashcards)
        elif choice == "2":
            review_flashcards(flashcards)
        elif choice == "3":
            take_quiz(flashcards)
        elif choice == "4":
            print("Saving and exiting. Goodbye!")
            save_flashcards(flashcards)
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
