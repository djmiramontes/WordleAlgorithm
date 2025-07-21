import json
import math

def calculate_entropy_from_uncertainty(input_file='uncertainty.json', output_file='ranked_entropy.json', top_n=25):
    with open(input_file, 'r') as f:
        uncertainty_data = json.load(f)

    entropy_data = {}

    for guess, feedback_counts in uncertainty_data.items():
        total = sum(feedback_counts.values())
        entropy = 0.0
        for count in feedback_counts.values():
            p = count / total
            if p > 0:
                entropy += p * math.log2(1 / p)  # log2(1/p) == -log2(p)
        entropy_data[guess] = round(entropy, 5)

    # Sort by entropy (descending)
    sorted_entropy = sorted(entropy_data.items(), key=lambda x: -x[1])

    # Save to JSON
    with open(output_file, 'w') as f:
        json.dump(dict(sorted_entropy), f, indent=2)

    # Print top N
    print(f"Top {top_n} guesses by entropy (bits):\n")
    for guess, ent in sorted_entropy[:top_n]:
        print(f"{guess:10} → {ent} bits")

# Run the function
calculate_entropy_from_uncertainty(top_n=25)
