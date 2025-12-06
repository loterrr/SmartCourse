#!/usr/bin/env python3
"""Smart Course Recommendation Engine (improved)

This module provides a small, testable recommendation engine suitable for
integration with a PHP/JS backend. It focuses on content-based signals and
includes sensible defaults for cold-start users.

Improvements made:
- Type hints and input validation
- Configurable weights and `top_n` parameter
- Loadable course catalog from `backend/courses.json` if present
- Logging to `backend/logs/recommendation.log`
- Small, deterministic tie-breaker for stable outputs
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# Setup logging to backend/logs
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "recommendation.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8")],
)
logger = logging.getLogger(__name__)


class CourseRecommendationEngine:
    def __init__(self, weights: Optional[Dict[str, float]] = None) -> None:
        # Allow overriding weights for experimentation or A/B tests
        self.weights = weights or {
            "career": 0.25,
            "learning": 0.20,
            "workload": 0.15,
            "difficulty": 0.20,
            "major": 0.20,
        }

        self.course_database = self._load_courses()
        self.major_requirements = self._load_major_requirements()

def _load_courses(self) -> List[Dict[str, Any]]:
        """Load courses from backend/courses.json if present; otherwise return built-in catalog."""
        catalog_path = Path(__file__).resolve().parent / "courses.json"
        if catalog_path.exists():
            try:
                with open(catalog_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    logger.info("Loaded %d courses from %s", len(data), catalog_path)
                    return data
            except Exception:
                logger.exception("Failed to load courses.json; falling back to built-in catalog")

        return [

            {"id": 1, "code": "CS101", "name": "Introduction to Computer Science", "department": "Technology", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Software Engineering", "Data Science", "IT"], "learning_style": ["Visual", "Hands-on"], "workload_hours": 8},
            {"id": 2, "code": "MATH151", "name": "Calculus I", "department": "Enhgineering", "credits": 4, "difficulty": 4, "prerequisites": [], "career_relevance": ["Engineering", "Data Science", "Finance"], "learning_style": ["Analytical", "Practice-based"], "workload_hours": 12},
            {"id": 3, "code": "ENG101", "name": "English Composition", "department": "Education", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["All"], "learning_style": ["Reading", "Writing"], "workload_hours": 6},
            {"id": 4, "code": "PHYS101", "name": "General Physics I", "department": "Engineering", "credits": 4, "difficulty": 4, "prerequisites": ["MATH151"], "career_relevance": ["Engineering", "Science", "Medical"], "learning_style": ["Visual", "Analytical"], "workload_hours": 10},
            {"id": 5, "code": "BIO101", "name": "Introduction to Biology", "department": "Science", "credits": 4, "difficulty": 3, "prerequisites": [], "career_relevance": ["Medical", "Research", "Healthcare"], "learning_style": ["Visual", "Reading"], "workload_hours": 9},
            {"id": 6, "code": "ECON101", "name": "Principles of Economics", "department": "Business", "credits": 3, "difficulty": 3, "prerequisites": [], "career_relevance": ["Business", "Finance", "Policy"], "learning_style": ["Analytical", "Reading"], "workload_hours": 7},
            {"id": 7, "code": "CHEM101", "name": "General Chemistry", "department": "Science", "credits": 4, "difficulty": 4, "prerequisites": [], "career_relevance": ["Medical", "Engineering", "Research"], "learning_style": ["Hands-on", "Analytical"], "workload_hours": 11},
            {"id": 8, "code": "PSYCH101", "name": "Introduction to Psychology", "department": "Social Science", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Healthcare", "Education", "Research"], "learning_style": ["Reading", "Discussion"], "workload_hours": 6},
            {"id": 9, "code": "HIST101", "name": "World History", "department": "Social Science", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Education", "Law", "Policy"], "learning_style": ["Reading", "Writing"], "workload_hours": 7},
            {"id": 10, "code": "ART101", "name": "Introduction to Visual Arts", "department": "Art", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Design", "Media", "Education"], "learning_style": ["Visual", "Hands-on"], "workload_hours": 8},
            {"id": 11, "code": "INT001", "name": "Drawing", "department": "Creative", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 12, "code": "INT002", "name": "Visual Arts", "department": "Creative", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 13, "code": "INT003", "name": "Designing Buildings", "department": "Creative", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 14, "code": "INT004", "name": "Interior Design", "department": "Creative", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 15, "code": "INT005", "name": "Product Design", "department": "Creative", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 16, "code": "INT006", "name": "Animation", "department": "Creative", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 17, "code": "INT007", "name": "Storyboarding", "department": "Creative", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 18, "code": "INT008", "name": "Computer Programming", "department": "Technology", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 19, "code": "INT009", "name": "Cybersecurity", "department": "Technology", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 20, "code": "INT010", "name": "Artificial Intelligence", "department": "Technology", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 21, "code": "INT011", "name": "Gaming", "department": "Technology", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 22, "code": "INT012", "name": "Hardware & Electronics", "department": "Technology", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 23, "code": "INT013", "name": "Robotics", "department": "Technology", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 24, "code": "INT014", "name": "Construction", "department": "Engineering", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 25, "code": "INT015", "name": "Machinery & Mechanics", "department": "Engineering", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 26, "code": "INT016", "name": "Power Systems", "department": "Engineering", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 27, "code": "INT017", "name": "Chemistry & Materials", "department": "Science", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 28, "code": "INT018", "name": "Biology", "department": "Science", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 29, "code": "INT019", "name": "Physics", "department": "Science", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 30, "code": "INT020", "name": "Scientific Research", "department": "Science", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 31, "code": "INT021", "name": "Human Behavior", "department": "Social Science", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 32, "code": "INT022", "name": "Politics & Law", "department": "Social Science", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 33, "code": "INT023", "name": "Teaching", "department": "Education", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 34, "code": "INT024", "name": "Business", "department": "Business", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 35, "code": "INT025", "name": "Finance", "department": "Business", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 36, "code": "INT026", "name": "Leadership", "department": "Business", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 37, "code": "INT027", "name": "Hospitality", "department": "Business", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["General"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
        ]

    def _load_major_requirements(self) -> Dict[str, List[str]]:
        """
        Maps majors to key course requirements. 
        Modified to include both Core and Interest-based options from the SQL dump.
        """
        return {
            "Technology": ["CS101", "INT008", "INT009", "INT010", "INT011", "INT012", "INT013"],
            "Social Science": ["PSYCH101", "HIST101", "ECON101", "INT021", "INT022"],
            "Engineering": ["MATH151", "PHYS101", "CHEM101", "INT014", "INT015", "INT016"],
            "Creative": ["INT001", "INT002", "INT003", "INT004", "INT005", "INT006", "INT007"],
            "Art": ["ART101", "INT001", "INT002"],
            "Science": ["BIO101", "CHEM101", "PHYS101", "INT017", "INT018", "INT019", "INT020"],
            "Education": ["INT023", "PSYCH101", "ENG101"],
            "Business": ["ECON101", "INT024", "INT025", "INT026", "INT027"],
            "Undecided": ["ENG101", "MATH151", "CS101", "HIST101"],
        }

    @staticmethod
    def _calculate_gpa_score(gpa: float) -> float:
        return max(0.0, min(gpa / 4.0, 1.0))

    @staticmethod
    def _match_career_interests(student_interests: List[str], course_relevance: List[str]) -> float:
        if not student_interests or "All" in course_relevance:
            return 0.5
        matches = sum(1 for interest in student_interests if interest in course_relevance)
        return matches / max(len(student_interests), 1)

    @staticmethod
    def _match_learning_style(student_style: str, course_styles: List[str]) -> float:
        if not student_style:
            return 0.5
        return 1.0 if student_style in course_styles else 0.3

    @staticmethod
    def _calculate_workload_compatibility(student_hours: float, course_hours: float) -> float:
        if student_hours >= course_hours:
            return 1.0
        if student_hours >= course_hours * 0.7:
            return 0.7
        return 0.4

    def _is_major_requirement(self, course_code: str, major: str) -> bool:
        return course_code in self.major_requirements.get(major, [])

    def _calculate_difficulty_match(self, gpa: float, difficulty: int) -> float:
        gpa_score = self._calculate_gpa_score(gpa)
        if gpa_score >= 0.9 and difficulty <= 4:
            return 1.0
        if gpa_score >= 0.75 and difficulty <= 3:
            return 0.9
        if gpa_score >= 0.65 and difficulty <= 2:
            return 0.8
        if difficulty <= 2:
            return 0.7
        return 0.5

    def generate_recommendations(self, student_data: Dict[str, Any], top_n: int = 8) -> List[Dict[str, Any]]:
        """Generate top-N course recommendations for a student.

        Inputs:
        - student_data: dict with optional keys: student_id, gpa, major, career_interests (list), learning_style, study_hours
        - top_n: number of recommendations to return

        Returns:
        - list of recommendation dicts sorted by confidence_score (desc)
        """
        # Validate and normalize inputs
        try:
            gpa = float(student_data.get("gpa", 3.0))
        except (TypeError, ValueError):
            gpa = 3.0

        major = student_data.get("major", "Undecided") or "Undecided"
        career_interests = student_data.get("career_interests") or []
        learning_style = student_data.get("learning_style", "Visual") or "Visual"
        try:
            study_hours = float(student_data.get("study_hours", 10))
        except (TypeError, ValueError):
            study_hours = 10.0

        recommendations: List[Dict[str, Any]] = []

        for course in self.course_database:
            career_score = self._match_career_interests(career_interests, course.get("career_relevance", []))
            learning_score = self._match_learning_style(learning_style, course.get("learning_style", []))
            workload_score = self._calculate_workload_compatibility(study_hours, float(course.get("workload_hours", 8)))
            difficulty_score = self._calculate_difficulty_match(gpa, int(course.get("difficulty", 3)))

            major_req = self._is_major_requirement(course.get("code", ""), major)
            major_bonus = 1.3 if major_req else 1.0

            base_score = (
                career_score * self.weights["career"]
                + learning_score * self.weights["learning"]
                + workload_score * self.weights["workload"]
                + difficulty_score * self.weights["difficulty"]
                + (1.0 if major_req else 0.5) * self.weights["major"]
            )

            final_score = base_score * major_bonus
            # Confidence scaled 0-100
            confidence = max(0.0, min(final_score * 100.0, 100.0))

            reasoning = self._generate_reasoning(course, major, career_score, learning_score, workload_score, difficulty_score)

            recommendations.append(
                {
                    "course_id": course.get("id"),
                    "course_code": course.get("code"),
                    "course_name": course.get("name"),
                    "department": course.get("department"),
                    "credits": course.get("credits"),
                    "confidence_score": round(confidence, 2),
                    "reasoning": reasoning,
                    "is_major_requirement": major_req,
                }
            )

        # Stable sort: primary by confidence desc, secondary by course_code asc
        recommendations.sort(key=lambda x: (-x["confidence_score"], x.get("course_code", "")))
        top = recommendations[: max(1, int(top_n))]
        logger.info("Generated %d recommendations for major=%s gpa=%.2f", len(top), major, gpa)
        return top

    def _generate_reasoning(self, course: Dict[str, Any], major: str, career_score: float, learning_score: float, workload_score: float, difficulty_score: float) -> str:
        reasons: List[str] = []
        if self._is_major_requirement(course.get("code", ""), major):
            reasons.append(f"Required for {major} major")
        if career_score > 0.7:
            reasons.append("Strong alignment with your career interests")
        elif career_score > 0.4:
            reasons.append("Relevant to your career goals")
        if learning_score > 0.8:
            reasons.append("Matches your learning style perfectly")
        if workload_score > 0.8:
            reasons.append("Workload fits your study schedule")
        elif workload_score < 0.5:
            reasons.append("Challenging workload - plan accordingly")
        if difficulty_score > 0.8:
            reasons.append("Good match for your academic level")
        elif difficulty_score < 0.6:
            reasons.append("May require extra effort based on your GPA")
        if int(course.get("difficulty", 3)) <= 2:
            reasons.append("Great foundational course for freshmen")
        return " • ".join(reasons) if reasons else "General education requirement"


def cli_main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing input file"}))
        sys.exit(1)

    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(json.dumps({"error": "Input file not found"}))
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        student_data = json.load(f)

    engine = CourseRecommendationEngine()
    recs = engine.generate_recommendations(student_data)
    print(json.dumps(recs, indent=2))


if __name__ == "__main__":
    cli_main()
