import json
import time
from core.retriever import IncidentRetriever
from core.reasoner import IncidentReasoner

retriever = IncidentRetriever()
reasoner = IncidentReasoner()

def evaluate():

    with open("evaluation/test_dataset.json", "r") as f:
        test_data = json.load(f)

    total = len(test_data)
    correct_severity = 0
    total_latency = 0
    total_similarity = 0
    confidence_correct_pairs = []

    for sample in test_data:

        start = time.time()

        similar = retriever.find_similar(sample["query"], top_k=3)
        result = reasoner.analyze(sample["query"], similar)

        latency = time.time() - start
        total_latency += latency

        # Severity prediction (majority vote from similar)
        if similar:
            predicted_severity = max(
                set([s["severity"] for s in similar]),
                key=[s["severity"] for s in similar].count
            )
        else:
            predicted_severity = "Unknown"

        if predicted_severity == sample["expected_severity"]:
            correct_severity += 1
            is_correct = 1
        else:
            is_correct = 0

        # Retrieval similarity
        if similar:
            avg_distance = sum(s["similarity_distance"] for s in similar) / len(similar)
            total_similarity += avg_distance

        # Confidence tracking
        confidence_correct_pairs.append(
            (result.get("confidence_score", 0), is_correct)
        )

    severity_accuracy = correct_severity / total
    avg_latency = total_latency / total
    avg_similarity = total_similarity / total

    print("\n===== Evaluation Results =====")
    print(f"Total Samples: {total}")
    print(f"Severity Accuracy: {round(severity_accuracy, 3)}")
    print(f"Average Latency (s): {round(avg_latency, 3)}")
    print(f"Average Similarity Distance: {round(avg_similarity, 3)}")

    print("\nConfidence vs Correctness:")
    for conf, correct in confidence_correct_pairs:
        print(f"Confidence: {round(conf,3)} | Correct: {correct}")

if __name__ == "__main__":
    evaluate()
