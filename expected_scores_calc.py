import json

def calculate_expected_score(
    sigmoid_file='sigmoid_ranked.json',
    entropy_file='ranked_entropy.json',
    output_file='expected_scores.json',
    score=1
):
    # Load sigmoid probabilities
    with open(sigmoid_file, 'r') as f:
        sigmoid_data = json.load(f)

    # Load entropy values
    with open(entropy_file, 'r') as f:
        entropy_data = json.load(f)

    expected_scores = {}

    for word in sigmoid_data:
        prob = sigmoid_data[word]
        uncertainty = entropy_data.get(word, 0)

        # Expected score formula
        expected = prob * score + (1 - prob) * (score + uncertainty)
        expected_scores[word] = round(expected, 5)

    # Sort by highest expected score
    sorted_scores = dict(sorted(expected_scores.items(), key=lambda x: x[1], reverse=True))

    # Save results
    with open(output_file, 'w') as f:
        json.dump(sorted_scores, f, indent=2)

    print(f"Expected scores saved to {output_file}")
    print("Top 10 suggestions:")
    for word, value in list(sorted_scores.items())[:10]:
        print(f"{word:10} → {value}")

# Run the function
calculate_expected_score()
