import time
import random
import string
import statistics
import numpy as np
import json
import os
import matplotlib.pyplot as plt

def generate_random_string(length=3):
    """Generate a random alphanumeric string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def run_trials(total_trials=5):
    """Run typing test for the specified number of trials."""
    results = []
    print("\nWelcome to Reaction - Performance Tracker!")
    print("Type the prompted string exactly as shown (case sensitive).")
    print("Try to be both fast and accurate.\n")
    for i in range(1, total_trials + 1):
        target = generate_random_string()
        print(f"Trial {i}: Type -> {target}")
        start = time.time()
        user_input = input("Your input: ").strip()
        end = time.time()
        time_taken = round(end - start, 3)
        correct = user_input == target
        results.append({
            "trial": i,
            "prompt": target,
            "input": user_input,
            "time": time_taken,
            "correct": correct
        })
        status = "Correct" if correct else "Incorrect"
        print(f"[{status}] Time: {time_taken} sec\n")
    return results

def compute_trend(times):
    """Compute the slope of response time trend using least squares."""
    x = np.arange(len(times))
    y = np.array(times)
    A = np.vstack([x, np.ones(len(x))]).T
    slope, _ = np.linalg.lstsq(A, y, rcond=None)[0]
    return slope

def summarize(results):
    """Display detailed results and compute performance summary."""
    correct_trials = [r for r in results if r["correct"]]
    print("\n--- Trial Details ---")
    for r in results:
        status = "Correct" if r["correct"] else "Incorrect"
        print(f"Trial {r['trial']} | Prompt: '{r['prompt']}' | Typed: '{r['input']}' | {status} | Time: {r['time']}s")
    if len(correct_trials) < 2:
        print("\nNot enough correct trials to analyze performance.")
        return {}
    times = [r["time"] for r in correct_trials]
    baseline = round(sum(times[:5]) / min(len(times), 5), 3)
    average = round(sum(times) / len(times), 3)
    consistency = round(statistics.stdev(times), 3) if len(times) > 1 else 0.0
    slope = compute_trend(times)
    raw_score = 100 - (slope * 100) - (consistency * 10)
    focus_score = round(min(max(raw_score, 0), 100), 2)
    print("\n--- Summary Report ---")
    print(f"Baseline (first 5): {baseline} sec")
    print(f"Average Time     : {average} sec")
    print(f"Consistency (std): {consistency}")
    print(f"Trend Slope      : {slope:.4f}")
    print(f"Focus Score      : {focus_score}/100")
    return {
        "baseline": baseline,
        "average": average,
        "std_dev": consistency,
        "slope": slope,
        "focus_score": focus_score,
        "session_trials": results
    }

def plot_scatter_with_line(results):
    """Plot a scatter plot of trial number vs time, colored by correctness, with a connecting line."""
    times = [r["time"] for r in results]
    correct = [r["correct"] for r in results]
    x = list(range(1, len(times)+1))
    colors = ['green' if c else 'red' for c in correct]
    plt.figure(figsize=(8,4))
    plt.scatter(x, times, c=colors, s=60, edgecolor='black', zorder=3)
    plt.plot(x, times, color='blue', linestyle='-', linewidth=1.5, alpha=0.6, zorder=2)
    plt.xticks(x)
    plt.xlabel('Trial Number')
    plt.ylabel('Time Taken (seconds)')
    plt.title('Typing Performance: Time per Trial')
    plt.grid(True, linestyle='--', alpha=0.5, zorder=0)
    plt.tight_layout()
    plt.show()

def append_to_file(results, summary, filename="neuro_results.json"):
    """Append the current session to the results JSON file."""
    session_data = {
        "trials": results,
        "summary": summary
    }
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []
    else:
        data = []
    data.append(session_data)
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nResults appended to {filename}")

if __name__ == "__main__":
    all_results = run_trials(total_trials=5)
    summary = summarize(all_results)
    if summary:
        append_to_file(all_results, summary)
        plot_scatter_with_line(all_results)