import json
from recommendation_algorithm import CourseRecommendationEngine


def test_generate_recommendations_basic():
    engine = CourseRecommendationEngine()
    student = {
        "student_id": "s1",
        "gpa": 3.6,
        "major": "Computer Science",
        "career_interests": ["Software Engineering"],
        "learning_style": "Hands-on",
        "study_hours": 10,
    }
    recs = engine.generate_recommendations(student, top_n=5)
    assert isinstance(recs, list)
    assert len(recs) <= 5

    top = recs[0]
    assert "course_code" in top
    assert "confidence_score" in top


def test_missing_fields_and_defaults():
    engine = CourseRecommendationEngine()
    student = {"student_id": "s2"}
    recs = engine.generate_recommendations(student, top_n=3)
    assert len(recs) == 3
    for r in recs:
        assert "course_code" in r
        assert 0.0 <= r["confidence_score"] <= 100.0
