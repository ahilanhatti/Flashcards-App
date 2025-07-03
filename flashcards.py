# flashcards.py

import json
import os

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
    print("3. Quit")

def add_flashcard(flashcards):
    question = input("Enter the question: ").strip()
    answer = input("Enter the answer: ").strip()
    if not question or not answer:
        print("Both question and answer are required.")
        return

    # Optional: Prevent duplicates
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
            print("Saving and exiting. Goodbye!")
            save_flashcards(flashcards)
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
