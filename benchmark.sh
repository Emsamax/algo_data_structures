#!/bin/bash

DATASETS=(1 2 3)
BENCHMARK_DIR="benchmarks"
PROFILE_DIR="profiling"
GRAPH_DIR="hyperfine_graphs"
#get the dir of hyperfine's python scripts
echo -e "Searching for hyperfine's python scripts"
HYPERFINE_SCRIPTS_DIR=$(find /usr -name "plot_whisker.py" 2>/dev/null | head -n 1 | xargs dirname)
if [ -z "$HYPERFINE_SCRIPTS_DIR" ]; then
    echo -e "Error: Hyperfine scripts not found. Please ensure that you have installed hyperfine."
    exit 1
fi
echo -e "Found scripts at: $HYPERFINE_SCRIPTS_DIR"
echo -e "\nStarting benchmarking loop"

# Create output directories
mkdir -p $BENCHMARK_DIR $PROFILE_DIR $GRAPH_DIR

# Loop over datasets
for d in "${DATASETS[@]}"; do
    echo -e "\n[Dataset $d] Benchmarks and Profiling..."
    
    # run benchmark with Hyperfine
    hyperfine --warmup 2 --min-runs 5 --show-output --ignore-failure \
    --export-json "$BENCHMARK_DIR/comparison_d$d.json" \
    --export-markdown "$BENCHMARK_DIR/comparison_d$d.md" \
    "python main.py --array -d $d" \
    "python main.py --trie -d $d -i" 2>/dev/null
    
    # gerate Profiling Data using cProfile
    echo "  - Generating cProfile data for Dataset $d..."
    python main.py --array -d $d --profile > /dev/null 2>&1
    python main.py --trie -d $d -i --profile > /dev/null 2>&1
    
    # generate Visual Graphs using Hyperfine's scripts
    echo "  - Generating performance graphs for Dataset $d..."
    
    # whisker plot
    python3 "$HYPERFINE_SCRIPTS_DIR/plot_whisker.py" "$BENCHMARK_DIR/comparison_d$d.json" \
    --output "$GRAPH_DIR/whisker_d$d.png" 2>/dev/null
    
    # historigram plot
    python3 "$HYPERFINE_SCRIPTS_DIR/plot_histogram.py" "$BENCHMARK_DIR/comparison_d$d.json" \
    --output "$GRAPH_DIR/histogram_d$d.png" 2>/dev/null
    
    # progression plot
    python3 "$HYPERFINE_SCRIPTS_DIR/plot_progression.py" "$BENCHMARK_DIR/comparison_d$d.json" \
    --output "$GRAPH_DIR/progression_d$d.png" 2>/dev/null
    
done

echo -e "  Benchmarking and Graph Generation Complete"
echo "Results summary:"
echo "  - JSON/MD Reports: $BENCHMARK_DIR/"
echo "  - cProfile Logs:   $PROFILE_DIR/"
echo "  - Visual Charts:   $GRAPH_DIR/"