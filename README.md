# Reaction Performance Tracker

This Python application measures your reaction and typing performance by prompting you to type random strings as quickly and accurately as possible. It records your response times, analyzes your performance, and saves results for future reference.

## Features

- Random string typing trials (case sensitive)
- Tracks accuracy and response time
- Calculates baseline, average, consistency, trend, and focus score
- Saves session results to a JSON file
- Visualizes performance with a scatter plot

## Requirements

- Python 3.7+
- `numpy`
- `matplotlib`

Install dependencies with:
```
pip install numpy matplotlib
```

## Usage

1. Run the script:
    ```
    python main.py
    ```
2. Follow the on-screen instructions.
3. After completing the trials, view your performance summary and plot.
4. Results are saved in `neuro_results.json`.

## Output

- **Summary Report:** Baseline, average time, consistency, trend slope, and focus score.
- **Plot:** Scatter plot of time taken per trial, colored by correctness.
- **Data File:** All sessions appended to `neuro_results.json`.

## License

MIT License
