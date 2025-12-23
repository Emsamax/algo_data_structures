
# README.md

.venv to heavy to put in git
run the command

```bash
 python -m venv .venv
 # activate with : 
 source .venv/bin/activate

```

then install the packages below with 

```bash
pip install graphviz matplotlib memory-profiler
```


to see packages manualy installed in .venv 

```bash
 pip list --not-required > README.md

Package         Version
--------------- -------
graphviz        0.21
matplotlib      3.10.8
memory-profiler 0.61.0
pip             25.3

```

```bash
pip install argparse
```

get random english words using  

```bash
curl https://random-word-api.herokuapp.com/word?number=10000 > dataset_n
```

3 datasets of size 100, 10000, 10000 words