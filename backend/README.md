Backend recommendation engine

Files added/changed:
- `recommendation_algorithm.py`: Improved, testable recommendation engine. Supports loading `courses.json` and logs to `logs/recommendation.log`.
- `test_recommendation.py`: Basic pytest suite for core behaviors.
- `sample_student.json`: Example student input for manual testing.

Quickstart

1. Install dependencies (use the workspace `requirements.txt`):

   pip install -r ../requirements.txt

2. Run the recommender from the backend folder:

   python recommendation_algorithm.py sample_student.json

3. Run tests from the `backend` folder:

   pytest -q

Notes

- You can extend the course catalog by adding `backend/courses.json` with an array of course objects matching the example schema in the built-in catalog.
- The engine intentionally remains lightweight and deterministic to make unit testing straightforward.
