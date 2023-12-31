# Contribution Guide

## Tidiness

* Whenever a step is changed or a new step is added, the [step description](./STEPS.md) should be updated.
* Wherever possible, type hints should be used
* 3 and more def parameters should normally be separated with newlines like this:
  ```python
  def my_func(
      param1: str,
      param2: int,
      param3: bool
  ) -> None:
  ```
* KISS

## Git

Always use a feature branch

```shell
git checkout -b [IssueNo]_my-new-feature
```

Always rebase before pushing:

```shell
git fetch --prune origin
git rebase origin/dev
```

Always commit with a [good commit message](https://cbea.ms/git-commit/), which starts with the Issue number.
Commits require a signature using GPG, SSH, or S/MIME. Read [about commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification).
Also include a sign-off statement, which can be done like so:

```shell
git commit -s
```

Push into a new branch and open a PR.

Example:

```shell
git push origin [IssueNo]_my-new-feature
```

## Tests

Execution of unit tests:

```shell
TEST_SKIP_IT=1 python -m unittest discover -v -s tests/ -p 'test_*.py'
```
To run integration tests, too, omit the `TEST_SKIP_IT=1`

## Layout

This project uses a [flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
