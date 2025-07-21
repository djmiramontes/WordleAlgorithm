import json
import os
from collections import Counter

def is_word_consistent(word, guess, feedback, debug=False):
    word_letters = list(word)
    guess_letters = list(guess)

    if debug:
        print(f"\nChecking word: {word} against guess: {guess} with feedback: {feedback}")

    used_in_word = [False] * 5
    used_in_guess = [False] * 5

    # Step 1: Handle greens
    for i in range(5):
        if feedback[i] == 'g':
            if word[i] != guess[i]:
                if debug: print(f"Green mismatch at {i}: {word[i]} != {guess[i]}")
                return False
            used_in_word[i] = True
            used_in_guess[i] = True

    # Step 2: Handle yellows
    for i in range(5):
        if feedback[i] == 'y':
            matched = False
            for j in range(5):
                if not used_in_word[j] and guess[i] == word[j] and i != j:
                    matched = True
                    used_in_word[j] = True
                    used_in_guess[i] = True
                    break
            if not matched:
                if debug: print(f"Yellow letter {guess[i]} not found in other position")
                return False

    # Step 3: Handle blacks
    for i in range(5):
        if feedback[i] == 'b':
            if not used_in_guess[i]:
                for j in range(5):
                    if not used_in_word[j] and guess[i] == word[j]:
                        if debug: print(f"Black letter {guess[i]} improperly appears at {j}")
                        return False

    if debug: print(f"Word {word} PASSES")
    return True



def filter_possible_words(possible_words, guess, feedback):
    return [w for w in possible_words if is_word_consistent(w, guess, feedback)]

def is_word_consistent_all_feedback(word, history):
    return all(is_word_consistent(word, guess, feedback) for guess, feedback in history)

def filter_allowed_words_by_history(allowed_words, history):
    return [w for w in allowed_words if is_word_consistent_all_feedback(w, history)]

def calculate_expected_scores(possible_words, allowed_words, sigmoid_data, entropy_data, score):
    expected_scores = {}
    for word in allowed_words:
        prob = sigmoid_data.get(word, 0)
        uncertainty = entropy_data.get(word, 0)
        expected = prob * score + (1 - prob) * (score + uncertainty)
        expected_scores[word] = expected
    return sorted(expected_scores.items(), key=lambda x: x[1], reverse=True)

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    with open('possible_words.txt') as f:
        possible_words = [w.strip() for w in f]

    with open('allowed_words.txt') as f:
        allowed_words = [w.strip() for w in f]

    sigmoid_data = load_json('sigmoid_ranked.json')
    entropy_data = load_json('ranked_entropy.json')

    current_possible = possible_words.copy()
    history = []
    score = 1

    print("\n--- Wordle Solver ---")
    print("Feedback codes: g=green, y=yellow, b=black/gray\n")

    # First guess: highest entropy
    first_guess = max(entropy_data.items(), key=lambda x: x[1])[0]
    print(f"Guess #{score}: {first_guess}")

    os.makedirs('solver_data', exist_ok=True)

    # Save initial data
    save_json(current_possible, f'solver_data/possible_words_step{score}.json')
    save_json({first_guess: entropy_data[first_guess]}, f'solver_data/guess_step{score}.json')
    expected_scores = calculate_expected_scores(current_possible, allowed_words, sigmoid_data, entropy_data, score)
    save_json(dict(expected_scores), f'solver_data/expected_scores_step{score}.json')

    current_guess = first_guess

    while True:
        feedback = input("Enter feedback (e.g. gybby): ").strip().lower()
        if len(feedback) != 5 or any(c not in 'gyb' for c in feedback):
            print("Invalid feedback. Use 5 chars from [g,y,b]. Try again.")
            continue

        if feedback == "ggggg":
            print(f"Solved in {score} guesses! 🎉")
            break

        # Add to feedback history
        history.append((current_guess, feedback))

        # Filter possible words strictly by latest feedback
        current_possible = filter_possible_words(current_possible, current_guess, feedback)

        if not current_possible:
            print("No possible words remaining. Check inputs or data.")
            break

        # Filter allowed words by *all* feedback history to ensure guesses are valid
        filtered_allowed = filter_allowed_words_by_history(allowed_words, history)

        if not filtered_allowed:
            print("No allowed words remaining after filtering by history.")
            break

        score += 1

        # Calculate expected scores with current score
        expected_scores = calculate_expected_scores(current_possible, filtered_allowed, sigmoid_data, entropy_data, score)

        next_guess = expected_scores[0][0]
        print(f"Guess #{score}: {next_guess}")

        # Save step data
        save_json(current_possible, f'solver_data/possible_words_step{score}.json')
        save_json({next_guess: expected_scores[0][1]}, f'solver_data/guess_step{score}.json')
        save_json(dict(expected_scores), f'solver_data/expected_scores_step{score}.json')

        current_guess = next_guess

if __name__ == "__main__":
    main()
