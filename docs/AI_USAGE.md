
# FieldTwin — Artificial Intelligence Usage Disclosure

**Version:** 1.0
**Project:** NASA Space Apps Challenge 2026
**Execution Plan:** FieldTwin v6.2
**Status:** Initial disclosure; update throughout development

## 1. Purpose

This document records the use of artificial intelligence in FieldTwin's research, software development, scientific analysis, and presentation.

AI tools support the team but do not replace scientific verification, human judgment, or independent evaluation.

## 2. AI-Assisted Development

AI assistants may support:

- Software architecture planning.
- Python code development.
- React and TypeScript development.
- Debugging and error investigation.
- Test generation.
- Documentation drafting.
- Scientific methodology discussion.
- User interface design.
- Literature discovery.
- Presentation preparation.

Every AI-generated contribution must be reviewed by a responsible team member.

## 3. AI Tools Register

Record each AI tool actually used.

| Tool | Purpose | Verification | Status |
|---|---|---|---|
| ChatGPT | Planning and initial documentation | Human review | Used |
| Other AI assistants | To be recorded when used | Required | Pending |

Additional tools must be documented when introduced.

Do not claim that a particular tool performed a task unless it actually did.

## 4. Scientific AI/ML

FieldTwin distinguishes between:

**AI development assistance:** AI tools used to help write, explain, or review software and documentation.

**Scientific machine learning:** Algorithms implemented within FieldTwin to analyze or rank terrain candidates.

These are different activities.

Using an AI coding assistant does not establish that FieldTwin contains a scientifically validated ML model.

## 5. Scientific Model Evaluation

An interpretable physical-feature baseline must be implemented first.

Before ML evaluation, create:

`docs/MODEL_BENCHMARK.md`

The benchmark must specify:

- Model objectives.
- Input features.
- Independent reference evidence.
- Geographic holdout strategy.
- Baseline comparison.
- Primary performance metric.
- Improvement threshold.
- Uncertainty and failure criteria.

Record actual results in:

`outputs/validated/model_comparison.json`

Retain ML only if it demonstrates measurable scientific or operational value under the predeclared evaluation protocol.

## 6. Human Verification

Human reviewers must verify:

1. NASA dataset eligibility and provenance.
2. Scientific references and citations.
3. Geographic coordinates and reference systems.
4. Terrain calculations and measurement units.
5. Statistical methodology.
6. Model evaluation and reported metrics.
7. Software functionality.
8. Scientific limitations.
9. Novelty claims.
10. Final presentation statements.

AI-generated explanations are not substitutes for original scientific sources.

## 7. Prohibited Practices

FieldTwin must not:

- Fabricate datasets or observations.
- Invent geographic coordinates.
- Generate fictional scientific measurements.
- Fabricate publications or citations.
- Claim unperformed tests succeeded.
- Present generated images as actual satellite observations.
- Report unmeasured model performance.
- Claim unverified scientific novelty.
- Conceal material scientific uncertainty.
- Submit unsupported AI-generated scientific conclusions.

## 8. AI-Generated Visual Content

AI-generated images or diagrams may be used for explanatory or design purposes if permitted by applicable competition rules.

Such materials must not be presented as authentic NASA observations.

Scientific figures representing measured data must originate from verified datasets and reproducible processing.

Where necessary, label visual assets as:

- Scientific observation.
- Derived scientific visualization.
- Conceptual illustration.
- AI-generated illustration.

## 9. Data Privacy and Security

Never provide AI systems with:

- Passwords.
- API tokens.
- Private SSH keys.
- Confidential institutional information.
- Restricted datasets without authorization.
- Personal information unnecessary for the task.

Public NASA data may be used according to the relevant source's applicable terms.

## 10. AI Contribution Log

Record material AI-assisted contributions.

| Date | Tool | Task | Human reviewer | Verification |
|---|---|---|---|---|
| 2026-11-14 | ChatGPT | Initial repository documentation and setup guidance | Project lead | Review ongoing |

Update this table throughout development.

For substantial scientific contributions, retain relevant prompts, methodological decisions, and review evidence when practical.

## 11. Blue Team / Red Team Review

### Blue Team

Evaluate whether AI assistance improves:

- Development quality.
- Scientific workflow.
- Code clarity.
- Reproducibility.
- Presentation effectiveness.

### Red Team

Investigate:

- AI hallucinations.
- Unsupported scientific claims.
- Fabricated references.
- Incorrect geospatial assumptions.
- Model overfitting.
- Data leakage.
- Misleading AI-generated visualizations.
- Unverified code behavior.

Critical findings must be corrected before final submission.

## 12. Final Submission Disclosure

Before submitting FieldTwin, document:

- AI tools actually used.
- Their material contributions.
- Whether scientific ML was implemented.
- Whether ML demonstrated measurable value.
- Human verification procedures.
- Scientific limitations.
- Any required competition-specific AI disclosures.

Verify the applicable NASA Space Apps 2026 rules before submission.

## 13. References

NASA Space Apps Challenge:
https://www.spaceappschallenge.org/2026/

NASA Space Apps AI and Data Guidance:
https://github.com/nasa/spaceapps/discussions/1849

NASA Scientific Data:
https://science.nasa.gov/

---

**Operating principle:** AI may accelerate development, but every scientific result must remain independently verifiable.
