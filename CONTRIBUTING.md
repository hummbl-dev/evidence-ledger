# Contributing

Thank you for your interest in contributing. This project follows a stdlib-first, zero-runtime-dependency philosophy.

## Development Setup

`ash
git clone https://github.com/hummbl-dev/<repo>.git
cd <repo>
pip install -e ".[dev]"
pytest -v
`

Requires Python 3.10+.

## Rules

1. **Zero runtime dependencies.** Production code uses only the Python standard library. Test dependencies (pytest) go in the [dev] extras only.
2. **All changes go through pull requests.** Branch protection on main requires CI to pass. Create a feature branch, open a PR, wait for green.
3. **Tests required.** Any new feature or bug fix must include a test that would fail without the change. Run pytest -v before pushing.
4. **Conventional Commits.** Use eat:, ix:, docs:, chore:, 	est: prefixes.
5. **No AI attribution in commits.** Do not add Co-authored-by, Generated-by, or equivalent AI/vendor trailers to commit messages.

## Pull Request Checklist

- [ ] Branch is rebased on latest main
- [ ] pytest -v passes locally
- [ ] No new runtime dependencies added (stdlib only)
- [ ] Commit messages follow Conventional Commits
- [ ] No secrets, internal URLs, or private infrastructure details

## License

By contributing, you agree that your contributions are dual-licensed under [Apache 2.0](LICENSE-APACHE) and [MIT](LICENSE-MIT).
