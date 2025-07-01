# flashcards.py

def show_menu():
    print("\nFlashcard Quiz App")
    print("1. Add a flashcard")
    print("2. Review flashcards")
    print("3. Quit")

def add_flashcard(flashcards):
    question = input("Enter the question: ")
    answer = input("Enter the answer: ")
    flashcards.append({"question": question, "answer": answer})
    print("Flashcard added!")

def review_flashcards(flashcards):
    if not flashcards:
        print("No flashcards to review.")
        return

    for i, card in enumerate(flashcards, 1):
        input(f"\nCard {i}: {card['question']} (press Enter to show answer)")
        print(f"Answer: {card['answer']}")

def main():
    flashcards = []

    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            add_flashcard(flashcards)
        elif choice == "2":
            review_flashcards(flashcards)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
