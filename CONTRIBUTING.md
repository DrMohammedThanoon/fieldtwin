# Contribute to FieldTwin

Welcome to SamaBeyond's terrain research project. Start with the [live application](https://samabeyond.github.io/fieldtwin/) and [scientific closeout](docs/PHASE5_SCIENTIFIC_CLOSEOUT.md).

## Choose a contribution

- Improve accessibility, maps, explanations or responsive layouts.
- Report a reproducibility problem with the command and actual output.
- Propose a scientific improvement with traceable source evidence and an explicit validation plan.

Open an issue with an owner, objective, input, expected artifact, verification method and fallback. Follow [AGENTS.md](AGENTS.md) and use a feature branch based on current main.

## Verify your change

For the frontend, run `npm ci --prefix app` and `npm run build --prefix app`. For scientific code, use the `fieldtwin` conda environment and run the relevant pytest tests. Never rerun a frozen held-out experiment to improve its score.

Keep raw DEMs, model binaries, credentials and local environment files out of Git. Preserve measured results, failed experiments and provenance. Explain changed behavior and actual checks in the pull request, then request independent review before merge.

## Scientific language

Terrain similarity does not establish rover safety, novelty or field suitability. Describe route searches as numerical experiments and physical rover trials as proposals. Cite evidence beside claims and retain uncertainty.
