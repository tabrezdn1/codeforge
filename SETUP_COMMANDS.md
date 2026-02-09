# CodeForge - Setup Commands (Copy-Paste Ready)

## Step 1: Clone (first time only)

```bash
git clone https://github.com/tabrezdn1/codeforge.git
cd codeforge
```

## Step 2: Python setup (first time only)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install google-adk google-cloud-storage pypdf pydantic python-dotenv httpx requests
```

## Step 3: Set environment variables

```bash
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

## Step 4: Test which Gemini model works

Try these one by one. The one that returns a "hello" response is your model:

### Test gemini-2.5-flash

```bash
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" "https://us-central1-aiplatform.googleapis.com/v1/projects/$(gcloud config get-value project)/locations/us-central1/publishers/google/models/gemini-2.5-flash:generateContent" -d '{"contents":[{"parts":[{"text":"Say hello"}]}]}'
```

### Test gemini-2.0-flash

```bash
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" "https://us-central1-aiplatform.googleapis.com/v1/projects/$(gcloud config get-value project)/locations/us-central1/publishers/google/models/gemini-2.0-flash:generateContent" -d '{"contents":[{"parts":[{"text":"Say hello"}]}]}'
```

### Test gemini-1.5-flash

```bash
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" "https://us-central1-aiplatform.googleapis.com/v1/projects/$(gcloud config get-value project)/locations/us-central1/publishers/google/models/gemini-1.5-flash:generateContent" -d '{"contents":[{"parts":[{"text":"Say hello"}]}]}'
```

### Test gemini-1.5-pro

```bash
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" "https://us-central1-aiplatform.googleapis.com/v1/projects/$(gcloud config get-value project)/locations/us-central1/publishers/google/models/gemini-1.5-pro:generateContent" -d '{"contents":[{"parts":[{"text":"Say hello"}]}]}'
```

## Step 5: Check if Vertex AI API is enabled

```bash
gcloud services list --enabled --filter="name:aiplatform"
```

If nothing shows up, enable it:

```bash
gcloud services enable aiplatform.googleapis.com
```

## Step 6: Kill old process and launch

```bash
fuser -k 8080/tcp 2>/dev/null; adk web --port 8080
```

Or use a different port:

```bash
adk web --port 8081
```

## Reconnecting after Cloud Shell timeout

```bash
cd ~/codeforge
source .venv/bin/activate
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
adk web --port 8080
```
