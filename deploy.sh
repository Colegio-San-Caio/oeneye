#!/usr/bin/env bash

# Configuration
OWNER="clevjhon"
REPO="oeneye"
BRANCH="main"
API_URL="http://127.0.0.1:8000/api"

OMQ_HEADER="X-OMQ-Auth-Token: oeneye-internal-key"

echo "Step 1: Staging and pushing latest changes to GitHub..."
git add .
git commit -m "Auto-commit: update deployment state" || echo "No changes to commit."
git push origin "$BRANCH"

echo "Step 2: Triggering local deployment endpoint..."
CREATE_RESPONSE=$(curl -s -X POST "$API_URL/deploy" \
  -H "$OMQ_HEADER" \
  -H "Content-Type: application/json" \
  -d "{
    \"ref\": \"$BRANCH\",
    \"environment\": \"production\",
    \"auto_merge\": false,
    \"description\": \"Automated git push and deployment trigger via omqAuth pipeline\"
  }")

echo "Response from local API:"
echo "$CREATE_RESPONSE"
