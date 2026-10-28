# Reflection

## 1. Which issues were the easiest to fix, and which were the hardest?

The easiest were the style issues. Docstrings, snake_case names, long lines and the f-string were all mechanical changes, and the tool output said exactly what to change. The parameterised SQL query was also quick once I knew the `?` placeholder syntax.

The hardest was removing `eval`. The obvious replacement, `ast.literal_eval`, does not work here because it cannot evaluate a comparison such as `7 + 1 <= 13`. I had to work out what the function was actually for (checking that one slot ends before the next one starts) and change it to take numbers instead of a string. Removing the `global` was harder in the same way. Pylint only says "don't use global", so I had to decide where the value should come from instead. Computing it from the database turned out to be simpler and also fixed a bug.

## 2. Did the tools report any false positives? What did they miss?

Bandit's B105 (hardcoded password) is a heuristic based on the variable name, so it can raise false positives. Here it was correct, though. Pylint and Flake8 both flagged the same long lines (C0301 and E501), so the reports overlap but neither is wrong.

The tools missed a real logic bug. `removeSlot` deleted the row but never reduced `booked_minutes`, so after removing the 45-minute show the counter still said 105 minutes instead of 60. No static analysis tool can know that two pieces of state are meant to stay in sync. I found it by reading the code. Pylint's complaint about the `global` statement pointed in the right direction, but it did not identify the bug.

## 3. How would you integrate static analysis into a real development workflow?

- **Locally:** run Flake8 and Pylint in the editor on save, and use a `pre-commit` hook so badly formatted code never reaches a commit.
- **In CI:** run all three tools on every pull request. Fail the build on any Bandit Medium/High finding, any Flake8 error, or a Pylint score below a threshold (for example 9.5).
- **Configuration:** keep the settings in the repository (`.pylintrc`, `setup.cfg`/`.flake8`, `.bandit`) so everyone uses the same rules. When a warning is a deliberate exception, suppress it on that specific line with a comment explaining why (`# nosec`, `# pylint: disable=...`) rather than turning the check off globally.

## 4. What tangible improvements did you see in the code after applying the fixes?

- **Security:** the SQL injection and arbitrary code execution through `eval` are both gone, and there is no secret stored in the source.
- **Correctness:** the booked-minutes total is now computed from the database, so it is always accurate, even after a slot is removed.
- **Readability:** consistent naming, docstrings and short lines make the file easier to read and review.
- **Reusability:** with the `__main__` guard, the module can be imported (for example by tests) without running the demo.
- **Measured:** Pylint went from 2.41 to 10.00/10, and Bandit and Flake8 went from 3 and 4 issues to none, with the program's output unchanged.
