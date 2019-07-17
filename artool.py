import os
import datetime
import json
import getpass
import argparse

from pydriller import RepositoryMining


# You can hack in your options here, if you like.
user = None
working_tree_dir = None
start_date = None
end_date = None


if __name__ == '__main__':
    if user is None:
        user = getpass.getuser()
    if working_tree_dir is None:
        working_tree_dir = os.getcwd()
    if start_date is None:
        now = datetime.datetime.now()
        start_date = datetime.datetime(year=now.year, month=now.month, day=1, tzinfo=now.tzinfo)

    parser = argparse.ArgumentParser(prog='Author\'s Rights Tool', description='Tool used to extract diffs from git commits.')
    parser.add_argument('-u', '--user', default=user, help=f'User name to filter commits by (defaults to \'{user}\').')
    parser.add_argument('-d', '--working-tree-dir', default=working_tree_dir, help=f'Path to git working directory (defaults to \'{working_tree_dir}\').')
    parser.add_argument('-s', '--start-date', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), default=start_date, help=f'Start date for filtering commits, in iso format (e.g. \'2017-10-21\') (defaults to \'{start_date}\').')
    parser.add_argument('-e', '--end-date', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), default=end_date, help=f'End date for filtering commits, in iso format (e.g. \'2017-10-21\') (defaults to \'{end_date}\').')

    args = parser.parse_args()

    user = args.user
    working_tree_dir = args.working_tree_dir
    start_date = args.start_date
    end_date = args.end_date

    print(f'Using git working directory: {working_tree_dir}')
    print(f'List of {user}\'s commits since {start_date.date().isoformat()}' + (f' to {end_date.date().isoformat()}:' if end_date is not None else ':'))
    commits = list(RepositoryMining(working_tree_dir, since=start_date, to=end_date, only_no_merge=True, only_authors=[user]).traverse_commits())
    for idx, commit in enumerate(commits):
        print('{}: {}'.format(idx, commit.msg))

    print('Enter lists of lists of commit numbers in json format (for example: [[0, 1], [2, 3]]):')
    commits_str = input()

    try:
        commits_idxs_lists = json.loads(commits_str)
    except Exception as exc:
        raise Exception('Input is not a valid json.') from exc

    if not isinstance(commits_idxs_lists, list):
        raise Exception('Input must be a list of lists of numbers.')

    invalid_lists = [l for l in commits_idxs_lists if not isinstance(l, list)]
    if len(invalid_lists) > 0:
        raise Exception(f'The following inputs should be lists, not single values: {invalid_lists}')

    for i, commits_idxs in enumerate(commits_idxs_lists):
        invalid_commits = [idx for idx in commits_idxs if (not isinstance(idx, int)) or (idx < 0) or (idx >= len(commits))]
        if len(invalid_commits) > 0:
            print(f'The following commit indices are invalid: {invalid_commits}')
            exit(1)

        selected_commits = [commits[idx] for idx in commits_idxs]
        with open(f'diff-{i}.diff', 'w', encoding='utf-8') as f:
            for idx, commit in enumerate(selected_commits):
                print('Idx: {} Hash {}, author {}, message {}'.format(idx, commit.hash, commit.author.name, commit.msg), file=f)

            print(f'', file=f)
            print(f'', file=f)

            for idx, commit in enumerate(selected_commits):
                print(f'==================================================================================================', file=f)
                print('Idx: {} Hash {}, author {}, message {}'.format(idx, commit.hash, commit.author.name, commit.msg), file=f)
                print(f'==================================================================================================', file=f)
                print(f'', file=f)

                for modified_file in commit.modifications: # here you have the list of modified files
                    print(f'============== File: {modified_file.filename} ==============', file=f)
                    print(modified_file.diff, file=f)
