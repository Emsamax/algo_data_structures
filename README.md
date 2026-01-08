
# README.md

.venv to heavy to put in git
run the command

```bash
 python -m venv .venv
 # activate with : 
 source .venv/bin/activate

```

then install the packages below with.

```bash
pip install graphviz matplotlib memory-profiler argparse
```

to see packages manualy installed in .venv.

```bash
 pip list --not-required > README.md

Package         Version
--------------- -------
graphviz        0.21
matplotlib      3.10.8
memory-profiler 0.61.0
pip             25.3
scipy           1.16.3

```

get random english words using  

```bash
curl https://random-word-api.herokuapp.com/word?number=10000 > dataset_n
```

3 datasets of size 100, 10000, 10000 words

## Benchmarking and graphs

**make sure to have these:**

```bash
pip install numpy matplotlib scipy 
```

find the scripts dir of hyperfine to generate benchmark graphs

```bash
sudo find / -name "plot_whisker.py" 2>/dev/null
[sudo] password for shrek:
/usr/lib/hyperfine/scripts/plot_whisker.py
```

To get the benchmark graph from json export with hyperfine

```bash
hyperfine --warmup 2  'python main.py --trie -d 1 ' --export-json benchmark.json
Benchmark 1: python main.py --trie -d 1
  Time (mean ± σ):     180.0 ms ±  28.6 ms    [User: 1443.0 ms, System: 26.9 ms]
  Range (min … max):   147.1 ms … 240.3 ms    19 runs

 /usr/lib/hyperfine/scripts/plot_whisker.py  benchmark.json
```
