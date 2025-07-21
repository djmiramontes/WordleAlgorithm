import json
from collections import defaultdict
from tqdm import tqdm


def get_feedback(guess, solution):
    feedback = ['0'] * 5
    used = [False] * 5

    # Green pass
    for i in range(5):
        if guess[i] == solution[i]:
            feedback[i] = '2'
            used[i] = True

    # Yellow pass
    for i in range(5):
        if feedback[i] == '2':
            continue
        for j in range(5):
            if not used[j] and guess[i] == solution[j]:
                feedback[i] = '1'
                used[j] = True
                break

    return ''.join(feedback)

def generate_uncertainty_map(allowed_guesses, possible_words):
    uncertainty = {}

    for guess in tqdm(allowed_guesses, desc="Calculating Uncertainty"):
        pattern_counts = defaultdict(int)
        for solution in possible_words:
            pattern = get_feedback(guess, solution)
            pattern_counts[pattern] += 1
        uncertainty[guess] = dict(pattern_counts)
    
    return uncertainty

# Load your word lists (replace with actual file paths or lists)
with open('allowed_words.txt') as f:
    allowed_guesses = [line.strip() for line in f]

with open('possible_words.txt') as f:
    possible_words = [line.strip() for line in f]

# Generate map and save
uncertainty_data = generate_uncertainty_map(allowed_guesses, possible_words)

with open('uncertainty.json', 'w') as f:
    json.dump(uncertainty_data, f, indent=2)

print("Uncertainty data saved to uncertainty.json")
