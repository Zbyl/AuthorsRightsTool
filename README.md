# AuthorsRightsTool

Tool for extracting commit diffs from a git repository.

The main purpose of this tool is to help during creation of Author's Rights reports for tax purposes in Poland.

# Running

```
> pip install -r requirements.txt
> python artool.py -d /path/to/my/git/repo -u "Bill Gates"

Using git working directory: /path/to/my/git/repo
List of Bill Gates's commits since 2019-07-01:
0: Added bells and whistles.
1: Added comments in frobnication.py.
2: Made feature_value semi-regular.
Enter lists of lists of commit numbers in json format (for example: [[0, 1], [2, 3]]):
[[0, 1], [2]]
```

# Output

For each list of commit indices in the input, output consists of `diff-N.diff` file that contains:
- list of commit messages,
- concatenated diffs of selected commits.

So in the example above, for input `[[0, 1], [2]]`, the output would be:
- `diff-0.diff` file that contains commits `0` and `1`,
- `diff-1.diff` file that contains commit `2`.

# Usage

```
usage: Author's Rights Tool [-h] [-u USER] [-d WORKING_TREE_DIR]
                            [-s START_DATE] [-e END_DATE]

Tool used to extract diffs from git commits.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User name to filter commits by (defaults to
                        name of current user).
  -d WORKING_TREE_DIR, --working-tree-dir WORKING_TREE_DIR
                        Path to git working directory (defaults to
                        current directory).
  -s START_DATE, --start-date START_DATE
                        Start date for filtering commits, in iso format (e.g.
                        '2017-10-21') (defaults to start of current month).
  -e END_DATE, --end-date END_DATE
                        End date for filtering commits, in iso format (e.g.
                        '2017-10-21') (defaults to 'None').
```
