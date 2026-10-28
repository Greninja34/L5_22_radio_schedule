# Identified Issues: `radio_schedule.py`

Line numbers refer to the original file. Results before and after the fixes:

| Tool   | Before                    | After            |
|--------|---------------------------|------------------|
| Pylint | 2.41/10 (22 messages)     | 10.00/10         |
| Bandit | 3 issues (2 Medium, 1 Low)| No issues        |
| Flake8 | 4 issues                  | No issues        |

## Issue table

High and medium severity issues come first.

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | SQL injection (Bandit B608, Medium) | Security | 11 | The INSERT query was built with `%` string formatting, so a show or host name containing `'` could break or change the SQL statement. | Use a parameterised query with `?` placeholders and pass the values as a tuple. |
| 2 | Use of `eval` (Bandit B307, Medium; Pylint W0123) | Security | 21 | `overlapFree` ran `eval()` on a string. Any code passed in would be executed. | Replace the formula string with three numeric arguments and return `start_hour + hours <= next_start_hour`. |
| 3 | Overly broad exception (Pylint W0718) | Bug | 22 | `except Exception` silently swallowed every error, including real bugs, and returned `False`. | Removed. Without `eval` there is nothing left that can fail, so no `try` is needed. |
| 4 | Hardcoded password (Bandit B105, Low) | Security | 5 | `STUDIO_PASSWORD = "onair2024"` stored a secret in source code, so it would end up in version control. | Read it from the environment with `os.environ.get("STUDIO_PASSWORD")`. |
| 5 | Global state and stale counter (Pylint W0603) | Bug | 6, 10, 12, 31 | `booked_minutes` was a global updated with `global`. `removeSlot` never subtracted from it, so the total was wrong after a removal (105 instead of 60). | Removed the global. Added `total_booked_minutes()`, which computes `SUM(minutes)` from the table, so it is always correct. |
| 6 | Multiple statements on one line (Flake8 E701, Pylint C0321) | Style | 27 | `if ...: return ...` was written on a single line. | Split it onto separate lines. The `booked_minutes > 0` check was dropped too, because an empty table already returns `[]`. |
| 7 | Line too long (Flake8 E501, Pylint C0301) | Style | 4, 11, 27 | Three lines were 110–135 characters long, over the 79-character limit. | Wrapped the SQL strings using implicit string concatenation inside parentheses. |
| 8 | Non-snake_case names (Pylint C0103) | Style | 9, 15, 19, 26, 31 | `addSlot`, `slotLabel`, `overlapFree`, `morningShows` and `removeSlot` did not follow the PEP 8 function naming convention. | Renamed to `add_slot`, `slot_label`, `overlap_free`, `morning_shows` and `remove_slot`. |
| 9 | Missing docstrings (Pylint C0114, C0116) | Style | 1, 9, 15, 19, 26, 31, 35 | The module and all six functions had no docstrings. | Added a one-line docstring to the module and to each function. |
| 10 | Old-style formatting (Pylint C0209) | Style | 11, 16 | `.format()` and `%` were used where an f-string is clearer. | Changed `slot_label` to use an f-string. Line 11 is fixed by #1. |
| 11 | Code runs on import | Design | 43 | `main()` was called at module level, so importing the file ran the demo. | Wrapped the call in `if __name__ == "__main__":`. |

## Verification

- `python radio_schedule.py` prints the same output before and after the fixes:
  ```
  Sunrise Beats hosted by Vik
  True ['Sunrise Beats']
  ```
- The tool reports are in `reports/before/` and `reports/after/` (`pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt`).
