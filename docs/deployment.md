# Cloud Run Deployment

The recommended public demo target is Google Cloud Run. This keeps the project aligned with the Google x Kaggle competition while providing a public interactive Gradio app URL.

## What Cloud Run Hosts

Cloud Run runs the Gradio app from `app.py` in the container defined by `Dockerfile`.

At runtime, Cloud Run provides a `PORT` environment variable. The app binds to `0.0.0.0:$PORT`, which is required for Cloud Run.

## Required Google Cloud Setup

You need:

- a Google Cloud project with billing enabled
- Cloud Run API enabled
- Cloud Build API enabled
- Secret Manager API enabled if storing `GEMINI_API_KEY` as a secret

Recommended region:

```text
us-central1
```

Recommended Cloud Run service name:

```text
hardware-npi-ideation
```

## Option A: Deploy From Google Cloud Shell

Cloud Shell is the easiest path because it already has `gcloud` installed and authenticated.

### 1. Open Cloud Shell

Go to:

```text
https://console.cloud.google.com/
```

Open Cloud Shell from the top-right terminal icon.

### 2. Set Variables

```bash
export PROJECT_ID="YOUR_PROJECT_ID"
export REGION="us-central1"
export SERVICE_NAME="hardware-npi-ideation"
gcloud config set project "$PROJECT_ID"
```

### 3. Enable APIs

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  --project "$PROJECT_ID"
```

### 4. Clone The Repository

```bash
git clone https://github.com/GreedyWinter/hardware-npi-ideation.git
cd hardware-npi-ideation
```

### 5. Add Gemini API Key As A Secret

Create the secret:

```bash
printf "YOUR_GEMINI_API_KEY" | gcloud secrets create gemini-api-key \
  --data-file=- \
  --project "$PROJECT_ID"
```

If the secret already exists, add a new version:

```bash
printf "YOUR_GEMINI_API_KEY" | gcloud secrets versions add gemini-api-key \
  --data-file=- \
  --project "$PROJECT_ID"
```

Do not commit API keys to the repository.

### 6. Deploy To Cloud Run

```bash
gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars GEMINI_MODEL=gemini-2.5-flash \
  --set-secrets GEMINI_API_KEY=gemini-api-key:latest \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 3 \
  --project "$PROJECT_ID"
```

The command will print a public service URL when deployment succeeds.

### 7. Verify

Open the service URL in a browser. The app should load with the cold-chain sensor sample scenario prefilled.

Click:

```text
Generate NPI Ideation Package
```

If `GEMINI_API_KEY` is configured correctly, the output should say it was generated with Gemini structured JSON. If not, the deterministic fallback still runs.

## Option B: Deploy Without Gemini Secret

For a quick public demo without Gemini-backed generation:

```bash
gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars GEMINI_MODEL=gemini-2.5-flash \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 3 \
  --project "$PROJECT_ID"
```

This deploys the app in deterministic fallback mode.

## After Deployment

Update the README with:

```text
Public demo: YOUR_CLOUD_RUN_SERVICE_URL
```

Then record the demo video using:

```text
docs/demo_script.md
```

## Troubleshooting

### Build fails during dependency install

Check Cloud Build logs from the deployment output.

### App starts but page does not load

Confirm `app.py` binds to Cloud Run's port. It should use:

```python
server_name="0.0.0.0"
server_port=int(os.environ.get("PORT", "7860"))
```

### Gemini output does not appear

Check that the secret exists:

```bash
gcloud secrets versions access latest --secret gemini-api-key --project "$PROJECT_ID"
```

Check that the service has the secret mounted as `GEMINI_API_KEY`:

```bash
gcloud run services describe "$SERVICE_NAME" --region "$REGION" --project "$PROJECT_ID"
```

### Service is public when it should not be

This demo is intended to be public for Kaggle judging. For private access, remove `--allow-unauthenticated` and configure IAM/IAP.
