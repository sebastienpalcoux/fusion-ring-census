# Laptop censuses for ranks 3–8

`python3 scripts/run_laptop.py --rank R --bound M` runs the existing exact
programs with no wall-clock limit on your own computer. It enumerates **all rings
through M**, including every duality type and noncommutative case, then checks
every tensor and every unit-fixing permutation independently. It applies no
categorifiability filter. A previous partial attempt is restarted, not resumed.

## Installation and commands

Python 3.9+ and GNU g++ with C++17/OpenMP are required; no Python packages, AI
models, paid APIs or internet connection are used by the computation. Linux and
Ubuntu under Windows Subsystem for Linux are supported. In Ubuntu/WSL:

```bash
sudo apt-get update
sudo apt-get install -y python3 g++ unzip
unzip Fusion_Census_Laptop.zip
cd Fusion_Census_Laptop
python3 scripts/run_laptop.py --rank 6 --bound 8
```

In a repository checkout, run the last command from the repository root.
On macOS, install Python and GNU GCC with Homebrew (`brew install python gcc`),
then set `CXX` to the installed versioned GNU compiler, for example
`export CXX=g++-15` **only if that executable is installed**. Apple's `g++` alias
is not the GNU OpenMP compiler. Native Windows is not tested; use WSL Ubuntu.

Run one command at a time, choosing a bound you want to attempt:

| Rank | Released complete bound / classes | Example command | Supported bound |
|---:|---:|---|---:|
| 3 | 1000 / 460,353 | `python3 scripts/run_laptop.py --rank 3 --bound 1000` | 1–1000 |
| 4 | 128 / 889,530 | `python3 scripts/run_laptop.py --rank 4 --bound 129` | 1–1000 |
| 5 | 19 / 34,133 | `python3 scripts/run_laptop.py --rank 5 --bound 20` | 1–32 |
| 6 | 7 / 9,613 | `python3 scripts/run_laptop.py --rank 6 --bound 8` | 1–15 |
| 7 | 3 / 1,421 | `python3 scripts/run_laptop.py --rank 7 --bound 4` | 1–15 |
| 8 | 1 / 96 | `python3 scripts/run_laptop.py --rank 8 --bound 2` | 1–15 |

Rank 3 at 1000 is a reproduction, not an extension: it already reaches the
supported ceiling. Other examples start at the nearest unfinished bound. These
are allowed inputs, not completion-time or memory guarantees. Higher bounds can
be much more costly. Keep the computer awake and connected to power.

`--mult M` is an alias for `--bound M`. The default thread count follows CPU
affinity (or available logical CPUs), capped at 64. You can limit it, e.g.
`--threads 8`. Only parallel phases use all these threads; serial phases remain
serial. The launcher never silently overwrites an earlier attempt. Use a fresh
`--output-dir my-next-attempt` if you need to rerun the same bound.

## Progress, verification and returned files

Reports and logs are under `runs/rankR_MM/`, where R and M are replaced by the
chosen integers. For example:

```bash
tail -f runs/rank6_M8/logs/selfdual.log
```

Inspect `run.json` for the current phase; the self-dual log does not exist until
that phase begins. Progress jobs have unequal cost and are not a runtime forecast.
Compilation products are reused if the driver requests the same content-keyed
build again. Separate launcher invocations use separate output/build directories.

Only after every duality search completes normally, every tensor passes the
independent checker, no based-isomorphism duplicate remains, and the entire
available old count prefix agrees, does the launcher create:

`runs/rankR_multiplicityM_verified.zip`

Send that ZIP for review and repository integration. It contains compressed
tensors/parameters, exact-multiplicity counts, completion logs, verifier reports,
source/baseline provenance and SHA-256 checksums. It excludes build products and
partial collections. A completed smaller bound is a reproduction and cannot
replace a larger released dataset. New results do not automatically edit GitHub,
manuscripts or OEIS. If interrupted or failed, no verified ZIP is produced;
keep diagnostic logs, but do not interpret partial output as census counts.

The local mode requires `--verify` and rejects GitHub Actions and all timed-mode
flags. Hosted workflow budgets remain finite and unchanged. Reports use standard
JSON (`null` for unlimited allowance); C++ receives `inf` only as its clock
allowance. No mathematical pruning or arithmetic rule is changed. For ranks 7–8
at bounds 11–15 the parallel prefix length is five instead of six, keeping the
partition below the solver's two-million-job ceiling without omitting any prefix.

## Rebuilding the standalone package

From a clean repository checkout:

```bash
python3 scripts/build_laptop_package.py --out /tmp/Fusion_Census_Laptop.zip
```

The package contains code, systems, coverage arguments, count manifest,
license/attribution and lightweight tests; it does not duplicate the large released
tensor datasets. Its baseline is a snapshot of the source revision. Package
checksums are checked before any computation. Only mocked numerical subprocesses
are used in `tests/test_laptop.py`; no laptop frontier was run while preparing it.
