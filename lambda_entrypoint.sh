#!/bin/bash
set -e

if [ "$RUN_MODE" = "local" ]; then
    echo "Starting in local mode..."
    exec python main.py
else
    echo "Starting in Lambda mode..."
    exec python -m awslambdaric main.lambda_handler
fi