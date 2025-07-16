# Full implementation of Flashcard Quiz App - Phase 6
# Includes performance tracking (reviewed count, correct count, accuracy-based sorting)

import json
import os
import random

FLASHCARD_FILE = "flashcards.json"

def load_flashcards():
    if os.path.exists(FLASHCARD_FILE):
        try:
            with open(FLASHCARD_FILE, "r") as f:
                flashcards = json.load(f)
                for card in flashcards:
                    card.setdefault("reviewed", 0)
                    card.setdefault("correct", 0)
                return flashcards
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
    print("4. Show categories")
    print("5. Manage flashcards")
    print("6. Quit")

def get_categories(flashcards):
    return sorted(set(card["category"] for card in flashcards))

def choose_category(flashcards):
    categories = get_categories(flashcards)
    if not categories:
        print("No categories available.")
        return None

    print("\nAvailable categories:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    print(f"{len(categories)+1}. All categories")

    while True:
        choice = input("Choose a category (number): ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            elif choice == len(categories) + 1:
                return None
        print("Invalid selection. Try again.")

def add_flashcard(flashcards):
    question = input("Enter the question: ").strip()
    answer = input("Enter the answer: ").strip()
    category = input("Enter a category (e.g., math, history): ").strip()

    if not question or not answer or not category:
        print("All fields are required.")
        return

    for card in flashcards:
        if card["question"].lower() == question.lower():
            print("This question already exists. Skipping.")
            return

    flashcards.append({
        "question": question,
        "answer": answer,
        "category": category,
        "reviewed": 0,
        "correct": 0
    })
    save_flashcards(flashcards)
    print("Flashcard added and saved!")

def review_flashcards(flashcards):
    if not flashcards:
        print("No flashcards to review.")
        return

    category = choose_category(flashcards)
    cards = [card for card in flashcards if category is None or card["category"] == category]

    if not cards:
        print("No flashcards found in this category.")
        return

    for i, card in enumerate(cards, 1):
        input(f"\nCard {i}: {card['question']} (press Enter to show answer)")
        print(f"Answer: {card['answer']}")

def take_quiz(flashcards):
    if not flashcards:
        print("No flashcards available to quiz.")
        return

    category = choose_category(flashcards)
    cards = [card for card in flashcards if category is None or card["category"] == category]

    if not cards:
        print("No flashcards found in this category.")
        return

    print("\nStarting quiz! Type your answers and press Enter.\n")
    score = 0
    missed_cards = []

    cards.sort(key=lambda c: (c["correct"] / c["reviewed"]) if c["reviewed"] else 0)
    # this lambda function is equivalent to:
    # def proportion_correct( c ):    # c is a dictionary representing one flashcard
    #     if c["reviewed"] != 0:
    #         return c["correct"] / c["reviewed"]
    #     else:
    #         return 0
    # then you would call:
    # cards.sort(key=proportion_correct)

    for i, card in enumerate(cards, 1):
        print(f"Question {i}: {card['question']}")
        user_answer = input("Your answer: ").strip().lower()
        correct_answer = card["answer"].strip().lower()

        card["reviewed"] += 1

        if user_answer == correct_answer:
            print("✅ Correct!\n")
            score += 1
            card["correct"] += 1
        else:
            print(f"❌ Incorrect. The correct answer was: {card['answer']}\n")
            missed_cards.append(card)

    print(f"Quiz complete! You scored {score}/{len(cards)} ({(score/len(cards)) * 100:.1f}%).")
    save_flashcards(flashcards)

    if missed_cards:
        retry = input("Retry missed questions? (y/n): ").strip().lower()
        if retry == "y":
            take_quiz(missed_cards)

def manage_flashcards(flashcards):
    if not flashcards:
        print("No flashcards to manage.")
        return

    print("\nFlashcards:")
    for i, card in enumerate(flashcards, 1):
        if card["reviewed"]:
            accuracy = f"{(card['correct'] / card['reviewed']) * 100:.0f}%"
        else:
            accuracy = "N/A"
        print(f"{i}. [{card['category']}] {card['question']} (Accuracy: {accuracy})")

    try:
        choice = int(input("Select a flashcard to manage (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(flashcards):
            manage_single_card(flashcards, choice - 1)
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")

def manage_single_card(flashcards, index):
    card = flashcards[index]
    print(f"\nSelected Flashcard:")
    print(f"Q: {card['question']}")
    print(f"A: {card['answer']}")
    print(f"Category: {card['category']}")
    print(f"Reviewed: {card['reviewed']}, Correct: {card['correct']}")
    print("1. Edit")
    print("2. Delete")
    print("3. Cancel")

    choice = input("Choose an option: ").strip()
    if choice == "1":
        edit_flashcard(card)
        save_flashcards(flashcards)
        print("Flashcard updated.")
    elif choice == "2":
        confirm = input("Are you sure you want to delete this flashcard? (y/n): ").strip().lower()
        if confirm == "y":
            del flashcards[index]
            save_flashcards(flashcards)
            print("Flashcard deleted.")
    else:
        print("Canceled.")

def edit_flashcard(card):
    print("Leave a field blank to keep current value.")
    new_question = input("New question: ").strip()
    new_answer = input("New answer: ").strip()
    new_category = input("New category: ").strip()

    if new_question:
        card["question"] = new_question
    if new_answer:
        card["answer"] = new_answer
    if new_category:
        card["category"] = new_category

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
            categories = get_categories(flashcards)
            if categories:
                print("\nAvailable categories:")
                for cat in categories:
                    print(f"- {cat}")
            else:
                print("No categories defined yet.")
        elif choice == "5":
            manage_flashcards(flashcards)
        elif choice == "6":
            print("Saving and exiting. Goodbye!")
            save_flashcards(flashcards)
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
