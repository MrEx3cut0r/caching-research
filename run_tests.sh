#!/bin/bash
echo "Starting tests..."
sleep 2

echo "1. Health check..."
pytest tests/test_simple.py::TestSimple::test_health -v

echo "2. Cache aside test..."
pytest tests/test_simple.py::TestSimple::test_create_cache_aside -v

echo "3. Get test..."
pytest tests/test_simple.py::TestSimple::test_get_cache_aside -v

echo "4. All strategies..."
pytest tests/test_simple.py::TestSimple::test_all_strategies_simple -v -s
