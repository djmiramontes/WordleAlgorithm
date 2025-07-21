import json
import math

def sigmoid(x, midpoint=0.5, k=10):
    return 1 / (1 + math.exp(-k * (midpoint - x)))

def rank_based_sigmoid(freq_file='freq_map.json', output_file='sigmoid_ranked.json', center_rank=6000, k=10):
    with open(freq_file, 'r') as f:
        freq_map = json.load(f)

    # Sort words by frequency descending
    sorted_words = sorted(freq_map.items(), key=lambda x: -x[1])
    total_words = len(sorted_words)

    sigmoid_scores = {}

    for i, (word, freq) in enumerate(sorted_words):
        # Normalize rank between 0 and 1
        norm_rank = i / (total_words - 1)
        score = round(sigmoid(norm_rank, midpoint=center_rank/(total_words-1), k=k), 5)
        sigmoid_scores[word] = score

    # Save sorted by sigmoid descending
    sorted_sigmoid = sorted(sigmoid_scores.items(), key=lambda x: -x[1])

    with open(output_file, 'w') as f:
        json.dump(dict(sorted_sigmoid), f, indent=2)

    print(f"Sigmoid saved to {output_file}")
    print("Top 10 words by sigmoid score:")
    for word, score in sorted_sigmoid[:10]:
        print(f"{word:10} → {score}")

# Run with a smooth k, e.g. 10
rank_based_sigmoid(center_rank=4000, k=10)
