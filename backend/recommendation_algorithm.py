#!/usr/bin/env python3
"""Smart Course Recommendation Engine"""

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Setup logging
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
    def __init__(self, course_data: List[Dict[str, Any]] = None, weights: Optional[Dict[str, float]] = None) -> None:
        self.weights = weights or {
            "career": 0.25,
            "learning": 0.20,
            "workload": 0.15,
            "difficulty": 0.20,
            "major": 0.20,
        }
        
        # Use provided data or fallback to empty list (which will trigger cold start or error)
        self.course_database = course_data if course_data else []
        
        # Load major requirements (Keep this or move to DB if you want)
        self.major_requirements = {
            "Technology": ["CS101", "INT008", "INT009", "INT010"],
            "Social Science": ["PSYCH101", "HIST101", "ECON101"],
            "Engineering": ["MATH151", "PHYS101", "CHEM101"],
            "Creative": ["INT001", "INT002", "ART101"],
            "Business": ["ECON101", "INT024", "INT025"],
            "Undecided": ["ENG101", "MATH151", "CS101"],
        }

    # ... (Keep helper methods: _calculate_gpa_score, _match_career_interests, etc.) ...
    # IMPORTANT: Ensure _is_major_requirement, _calculate_difficulty_match, etc. are included here
    
    @staticmethod
    def _calculate_gpa_score(gpa: float) -> float:
        return max(0.0, min(gpa / 4.0, 1.0))

    @staticmethod
    def _match_career_interests(student_interests: List[str], course_relevance: List[str]) -> float:
        if not student_interests or "All" in course_relevance:
            return 0.5
        # Clean inputs for better matching (lowercase)
        s_interests = [s.lower().strip() for s in student_interests]
        c_relevance = [c.lower().strip() for c in course_relevance]
        
        matches = sum(1 for interest in s_interests if interest in c_relevance)
        # Check for "General" match
        if "general" in c_relevance:
             return 0.4
             
        return matches / max(len(s_interests), 1)

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
        # Simple lookup, could be improved with DB data if passed
        return course_code in self.major_requirements.get(major, [])

    def _calculate_difficulty_match(self, gpa: float, difficulty: int) -> float:
        gpa_score = self._calculate_gpa_score(gpa)
        if gpa_score >= 0.9 and difficulty <= 4: return 1.0
        if gpa_score >= 0.75 and difficulty <= 3: return 0.9
        if gpa_score >= 0.65 and difficulty <= 2: return 0.8
        if difficulty <= 2: return 0.7
        return 0.5
    
    def _generate_reasoning(self, course, major, career_score, learning_score, workload_score, difficulty_score):
        reasons = []
        if self._is_major_requirement(course.get("code"), major):
            reasons.append(f"Core requirement for {major}")
        if career_score > 0.6:
            reasons.append("Aligns with your career interests")
        if learning_score > 0.8:
            reasons.append(f"Matches your {course.get('learning_style',[])[0]} learning style")
        if workload_score > 0.8:
            reasons.append("Fits your study schedule")
        
        return " • ".join(reasons) if reasons else "General elective"

    def generate_recommendations(self, student_data: Dict[str, Any], top_n: int = 8) -> List[Dict[str, Any]]:
        # Normalize inputs
        gpa = float(student_data.get("gpa", 3.0))
        major = student_data.get("major", "Undecided")
        career_interests = student_data.get("career_interests") or []
        learning_style = student_data.get("learning_style", "Visual")
        study_hours = float(student_data.get("study_hours", 10.0))

        recommendations = []

        for course in self.course_database:
            # Safely get course attributes
            c_relevance = course.get("career_relevance", [])
            c_styles = course.get("learning_style", [])
            c_workload = float(course.get("workload_hours", 8))
            c_difficulty = int(course.get("difficulty", 3))

            career_score = self._match_career_interests(career_interests, c_relevance)
            learning_score = self._match_learning_style(learning_style, c_styles)
            workload_score = self._calculate_workload_compatibility(study_hours, c_workload)
            difficulty_score = self._calculate_difficulty_match(gpa, c_difficulty)
            
            major_req = self._is_major_requirement(course.get("code"), major)
            
            # Weighted Sum
            score = (
                career_score * self.weights["career"] +
                learning_score * self.weights["learning"] +
                workload_score * self.weights["workload"] +
                difficulty_score * self.weights["difficulty"] +
                (1.0 if major_req else 0.5) * self.weights["major"]
            )
            
            # Boost major requirements
            if major_req: score *= 1.2

            confidence = min(score * 100, 100)
            
            if confidence > 40: # Filter out very low matches
                recommendations.append({
                    "course_id": course.get("id"),
                    "course_code": course.get("code"),
                    "course_name": course.get("name"),
                    "department": course.get("department"),
                    "credits": course.get("credits"),
                    "confidence_score": round(confidence, 1),
                    "reasoning": self._generate_reasoning(course, major, career_score, learning_score, workload_score, difficulty_score)
                })

        recommendations.sort(key=lambda x: x["confidence_score"], reverse=True)
        return recommendations[:top_n]

def cli_main():
    # Expect: script.py <student_json_path> <course_json_path>
    if len(sys.argv) < 3:
        # Fallback error for missing args
        print(json.dumps({"error": "Missing input files"}))
        sys.exit(1)

    student_file = Path(sys.argv[1])
    course_file = Path(sys.argv[2])

    if not student_file.exists() or not course_file.exists():
        print(json.dumps({"error": "Input files not found"}))
        sys.exit(1)

    try:
        with open(student_file, "r", encoding="utf-8") as f:
            student_data = json.load(f)
            
        with open(course_file, "r", encoding="utf-8") as f:
            course_data = json.load(f)
            
        engine = CourseRecommendationEngine(course_data=course_data)
        recs = engine.generate_recommendations(student_data)
        
        # Only print the final JSON to stdout
        print(json.dumps(recs))
        
    except Exception as e:
        logger.exception("Engine Failure")
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    cli_main()
