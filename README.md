# DPI-HT-01 Financial Crime Scene Assignment

Static reviewer app and machine-readable submission for the DPI-HT-01 case.

## What is included

- Main dashboard at `/`
- Compact assessor page at `/review`
- Machine-readable answer at `/submission.json`
- Completed decision log with all 100 decision IDs
- AI review trail for all 25 material judgments
- Reconciled profit and loss, cash flow and balance sheet
- Supporting schedules, reconciliations, uncertainties and board recommendation

## Local checks

```bash
npm run build
npm start
```

Then open:

- `http://localhost:4173/`
- `http://localhost:4173/review`
- `http://localhost:4173/submission.json`

This project has no external runtime dependencies, no database, no login and no paid API.

## Publishing to GitHub and Vercel

1. Create a GitHub repository and push this folder.
2. In Vercel, import the GitHub repository.
3. Use the default static project settings. The build command is `npm run build`.
4. After deployment, check the public URLs `/`, `/review` and `/submission.json` in a private browser window.

The original assignment and evidence files are preserved in their supplied folder structure.
