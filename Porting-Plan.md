# Porting Plan for Python 3.2.5

This document proposes a phased approach for making **docopt-ng** run under Python
3.2.5.  The current codebase targets Python 3.7+ and extensively uses modern
syntax and modules.  Porting to 3.2.5 will require removing unsupported
language features, providing backports for missing modules and adjusting the
packaging configuration.

Each phase below is designed to be a reasonable work unit for Codex.  After
each phase, the test-suite (`pytest`) should be executed under Python 3.2.5 to
catch regressions.

## Phase 1 – Baseline and Environment

1. Set up a Python **3.2.5** environment and confirm that the project does not
   currently install or run there.
2. Run the test-suite on a modern interpreter to establish the baseline.
   Currently `pytest` reports 614 passing tests.
3. Note the `requires-python` field in `pyproject.toml` which is presently
   `">=3.7"`【F:pyproject.toml†L5-L14】.
   This will need to be relaxed in later phases.

## Phase 2 – Remove Incompatible Future Import and Update Typing

1. `docopt/__init__.py` uses `from __future__ import annotations`【F:docopt/__init__.py†L25】
   which does not exist in Python 3.2.5.  Remove this import.
2. Replace uses of builtin generics and the union operator:
   - e.g. parameters such as `collected: list[_Pattern] | None` and
     `name: str | None` at lines 105–119【F:docopt/__init__.py†L105-L119】.
   - Convert to old style `typing.List` and `typing.Union` type hints, or omit
     annotations entirely for Python 3.2 compatibility.
3. Introduce a vendored copy of the `typing` module (available as a backport on
   PyPI) so type hints can still be imported under 3.2.

## Phase 3 – Replace F‑Strings

1. Several diagnostic messages use f‑strings, for example
   the error at line 433 and the corrections printed around
   lines 465–468 and 530–560【F:docopt/__init__.py†L430-L568】.
2. Convert all f‑strings to `str.format()` or `%` formatting which are
   available in Python 3.2.
3. Search the entire repository for remaining `f"` strings and update them.

## Phase 4 – Provide Backports for Missing Modules

1. Python 3.2 lacks the `pathlib` module used in the test suite and may miss
   other modern libraries.  Add conditional imports with fallbacks to
   `pathlib2` or local shims.
2. Ensure that `NamedTuple` (currently imported from `typing` at line 31) is
   available by using the backport.
3. Review other dependencies (e.g., `importlib.metadata`) and vendor backports
   as needed.

## Phase 5 – Packaging Adjustments

1. The current project is built with `pdm-backend`.  Python 3.2 cannot install
   this directly.  Provide a legacy `setup.py` or use a simpler build backend so
   the package can be installed without modern tooling.
2. Update `requires-python` in `pyproject.toml` to allow Python 3.2.5.
3. Update continuous integration or local scripts to run tests under Python 3.2.

## Phase 6 – Syntax and Library Compatibility Sweep

1. Search for additional syntax introduced after 3.2 (e.g., set literals,
   dictionary comprehensions with unpacking, keyword‑only arguments) and refactor
   as required.
2. Review standard library APIs for differences (e.g., `re.fullmatch` is not
   available in 3.2) and provide polyfills where used.
3. Execute the full test-suite under Python 3.2.5 and fix any runtime errors.

## Phase 7 – Final Verification and Cleanup

1. Run `pytest` on Python 3.2.5 and on modern Python versions to ensure
   cross-version compatibility.
2. Review documentation and update the README to reflect support for Python 3.2.
3. Tag a release and update version metadata in `docopt/_version.py`.

---

Following these phases sequentially should systematically migrate the project to
Python 3.2.5 while keeping the codebase in a working state at each step.
