#!/bin/bash

# Build React app
echo "Building React app..."
cd react-ui
npm run build
cd ..

# Start Flask server
echo "Starting Flask server..."
export FLASK_APP=app
flask run --host=0.0.0.0 --port=5000
