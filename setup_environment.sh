#!/bin/bash
set -e

echo "============================================="
echo "  CodeForge - GCP Environment Setup"
echo "============================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Edit .env and set your GOOGLE_CLOUD_PROJECT before continuing."
    echo "  nano .env"
    echo ""
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | grep -v '^\s*$' | xargs)

# Validate required vars
if [ -z "$GOOGLE_CLOUD_PROJECT" ] || [ "$GOOGLE_CLOUD_PROJECT" = "your-gcp-project-id" ]; then
    echo "ERROR: GOOGLE_CLOUD_PROJECT not set in .env"
    echo "  Edit .env and set your project ID."
    exit 1
fi

echo "Project:  $GOOGLE_CLOUD_PROJECT"
echo "Location: $GOOGLE_CLOUD_LOCATION"
echo "Bucket:   $GOOGLE_CLOUD_STORAGE_BUCKET"
echo ""

# Set the gcloud project
gcloud config set project "$GOOGLE_CLOUD_PROJECT"

# Phase 1: Enable APIs
echo "Phase 1: Enabling GCP APIs..."
gcloud services enable aiplatform.googleapis.com --project="$GOOGLE_CLOUD_PROJECT" --quiet
gcloud services enable storage.googleapis.com --project="$GOOGLE_CLOUD_PROJECT" --quiet
echo "  APIs enabled."

# Phase 2: Create GCS bucket
echo ""
echo "Phase 2: Creating GCS bucket..."
gsutil mb -p "$GOOGLE_CLOUD_PROJECT" -l "$GOOGLE_CLOUD_LOCATION" \
    "gs://$GOOGLE_CLOUD_STORAGE_BUCKET/" 2>/dev/null && echo "  Bucket created." || echo "  Bucket already exists."

# Phase 3: Upload sample documents
echo ""
echo "Phase 3: Uploading sample requirement documents..."
gsutil cp data/sample_requirements/*.md "gs://$GOOGLE_CLOUD_STORAGE_BUCKET/requirements/"
echo "  Sample documents uploaded."

# Phase 4: Verify setup
echo ""
echo "Phase 4: Verifying..."
gcloud services list --enabled --filter="name:aiplatform" --project="$GOOGLE_CLOUD_PROJECT" --format="value(name)" | grep -q "aiplatform" && \
    echo "  Vertex AI API:     ENABLED" || echo "  Vertex AI API:     NOT ENABLED (check manually)"
gsutil ls "gs://$GOOGLE_CLOUD_STORAGE_BUCKET/" > /dev/null 2>&1 && \
    echo "  GCS Bucket:        ACCESSIBLE" || echo "  GCS Bucket:        NOT ACCESSIBLE"

echo ""
echo "============================================="
echo "  Setup Complete!"
echo "============================================="
echo ""
echo "Next steps:"
echo "  1. python3 dry_run.py          # Validate everything"
echo "  2. adk web --port 8080         # Launch the web UI"
echo ""
