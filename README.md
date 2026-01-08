# Suffix Array vs Prefix Trie Comparison

**SUBJECT 5**
This project implements and compares two string data structures: a **Suffix Array** and a **Prefix Trie** with string inversion.

## 1. Setup Environment

The `.venv` directory is excluded from this repository. To initialize your local environment:

```bash
# Create the virtual environment
python -m venv .venv

# Activate the environment
source .venv/bin/activate

# Install required packages
pip install numpy matplotlib graphviz memory-profiler scipy snakeviz

```

### Required Libraries (Detailed List)

To ensure the environment matches the development setup, here are the main libraries and their versions:

```bash
pip list --not-required
```

```text
Package         Version
--------------- -------
graphviz        0.21
matplotlib      3.10.8
memory-profiler 0.61.0
numpy           1.26.0
pip             25.3
scipy           1.16.3
snakeviz        2.2.0

```

*Note: For the automated benchmarks, ensure `hyperfine` is installed on your system (`sudo apt install hyperfine` on Linux).*

## 2. Dataset Management

The project uses three incremental datasets. You can generate other using the following commands:

```bash
mkdir -p datasets
curl "[https://random-word-api.herokuapp.com/word?number=100](https://random-word-api.herokuapp.com/word?number=100)" > datasets/dataset_n.txt
```

## 3. Usage & CLI Arguments

The `main.py` script allows you to run specific experiments manually:

| Argument          | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| `--array`         | Run the Suffix Array implementation.                          |
| `--trie`          | Run the Prefix Trie implementation.                           |
| `-d`, `--dataset` | Choose dataset ID (1, 2, or 3).                               |
| `-i`, `--invert`  | Invert strings before insertion (Trie becomes a Suffix Trie). |
| `--profile`       | Enable cProfile and export `.prof` files to `profiling/`.     |
| `--graph`         | Generate GraphViz visualizations (save to `graphs/`).         |
| `--verbose`       | Display detailed execution logs.                              |

**Example Command:**

```bash
python main.py --trie -d 2 --invert --profile --verbose

```

## 4. Automated Benchmarking

A dedicated script `benchmark.sh` is provided to automate the entire testing suite across all datasets.

### Running the suite:

```bash
chmod +x benchmark.sh
./benchmark.sh

```

### Generated Outputs:

* **`benchmarks/`**: Hyperfine execution reports in JSON and Markdown.
* **`profiling/`**: `cProfile` data. Use `snakeviz profiling/file.prof` to analyze.
* **`hyperfine_graphs/`**: Visual performance charts (Whisker and Histograms).
