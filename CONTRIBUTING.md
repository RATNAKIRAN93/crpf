# Contributing Guidelines

Thank you for your interest in contributing!

## Ways to Contribute
- Report bugs (open an issue with reproduction steps)
- Improve documentation or examples
- Add tests for existing functionality
- Implement new features (open an issue first to discuss larger changes)

## Development Setup
1. Clone the repository
2. (Optional) Create a Python virtual environment
3. Install Python dependencies:
```
pip install -r requirements.txt
```
4. Install frontend dependencies:
```
cd siem-frontend && npm ci
```

## Running Tests
```
pytest -q
npm test -- --watch=false
```

## Pull Request Checklist
- Code formatted and linted (future: add linters)
- Tests added/updated for changes
- Documentation updated if needed
- No secrets or credentials committed

## Commit Messages
Use clear, concise messages:
```
feat: add anomaly correlation module
fix: handle empty log batch in detector
chore: update dependencies
```

## Security Issues
If you discover a potential security issue, please follow the steps in `SECURITY.md` instead of opening a public issue.

## License
By contributing you agree your contributions are licensed under the project MIT License.
