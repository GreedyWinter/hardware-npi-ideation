# Deployment

The recommended public demo target is Hugging Face Spaces using the Gradio SDK.

## Hugging Face Space Settings

- Space SDK: Gradio
- App file: `app.py`
- Python dependencies: `requirements.txt`
- Visibility: Public

## Secrets

Add this secret only if Gemini-backed structured generation is desired:

```text
GEMINI_API_KEY
```

Optional model override:

```text
GEMINI_MODEL=gemini-2.5-flash
```

Without `GEMINI_API_KEY`, the app still runs with deterministic local fallback agents.

## Public Demo Checklist

- Create a public Hugging Face Space.
- Connect the GitHub repository or upload the repository files.
- Add `GEMINI_API_KEY` as a Space secret.
- Confirm the app launches.
- Add the public Space URL to the README.
- Record the demo video using the script in `docs/demo_script.md`.

## Why Gradio

Gradio provides a direct interactive demo path, works well for Kaggle judges, and can be hosted publicly without building a custom frontend or backend service.
