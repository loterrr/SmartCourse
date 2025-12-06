from __future__ import annotations
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import math

# Setup logging to file only (not stdout)
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
        self.weights = weights or {
            "career": 0.30,
            "learning": 0.10,
            "workload": 0.10,
            "difficulty": 0.20,
            "major": 0.30,
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
            except Exception as e:
                logger.exception("Failed to load courses.json; falling back to built-in catalog")

        # Built-in course catalog
        return [
            {"id": 1, "code": "CS101", "name": "Introduction to Computer Science", "department": "Technology", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Software Engineering", "IT", "Data Science"], "learning_style": ["Visual", "Hands-on"], "workload_hours": 8},
            {"id": 2, "code": "MATH151", "name": "Calculus I", "department": "Engineering", "credits": 4, "difficulty": 4, "prerequisites": [], "career_relevance": ["Engineering", "Data Science", "Finance"], "learning_style": ["Analytical", "Practice-based"], "workload_hours": 12},
            {"id": 3, "code": "ENG101", "name": "English Composition", "department": "Education", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["All"], "learning_style": ["Reading", "Writing"], "workload_hours": 6},
            {"id": 4, "code": "PHYS101", "name": "General Physics I", "department": "Engineering", "credits": 4, "difficulty": 4, "prerequisites": ["MATH151"], "career_relevance": ["Engineering", "Science", "Medical"], "learning_style": ["Visual", "Analytical"], "workload_hours": 10},
            {"id": 5, "code": "BIO101", "name": "Introduction to Biology", "department": "Science", "credits": 4, "difficulty": 3, "prerequisites": [], "career_relevance": ["Medical", "Research", "Healthcare"], "learning_style": ["Reading", "Visual"], "workload_hours": 9},
            {"id": 6, "code": "ECON101", "name": "Principles of Economics", "department": "Business", "credits": 3, "difficulty": 3, "prerequisites": [], "career_relevance": ["Business", "Finance", "Policy"], "learning_style": ["Analytical", "Reading"], "workload_hours": 7},
            {"id": 7, "code": "CHEM101", "name": "General Chemistry", "department": "Science", "credits": 4, "difficulty": 4, "prerequisites": [], "career_relevance": ["Medical", "Engineering", "Research"], "learning_style": ["Hands-on", "Analytical"], "workload_hours": 11},
            {"id": 8, "code": "PSYCH101", "name": "Introduction to Psychology", "department": "Social Science", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Healthcare", "Education", "Research"], "learning_style": ["Reading", "Discussion"], "workload_hours": 6},
            {"id": 9, "code": "HIST101", "name": "World History", "department": "Social Science", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Education", "Law", "Policy"], "learning_style": ["Reading", "Writing"], "workload_hours": 7},
            {"id": 10, "code": "ART101", "name": "Introduction to Visual Arts", "department": "Art", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Design", "Media", "Education"], "learning_style": ["Visual", "Hands-on"], "workload_hours": 8},
            {"id": 11, "code": "INT001", "name": "Drawing", "department": "Creative", "credits": 3, "difficulty": 1, "prerequisites": [], "career_relevance": ["Art", "Design", "Media"], "learning_style": ["Visual", "Hands-on"], "workload_hours": 5},
            {"id": 12, "code": "INT002", "name": "Visual Arts", "department": "Creative", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Art", "Design"], "learning_style": ["Visual", "Hands-on"], "workload_hours": 6},
            {"id": 13, "code": "INT003", "name": "Designing Buildings", "department": "Engineering", "credits": 3, "difficulty": 3, "prerequisites": [], "career_relevance": ["Architecture", "Construction"], "learning_style": ["Visual", "Analytical"], "workload_hours": 7},
            {"id": 14, "code": "INT004", "name": "Interior Design", "department": "Creative", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Interior Design", "Architecture"], "learning_style": ["Visual", "Hands-on"], "workload_hours": 6},
            {"id": 15, "code": "INT005", "name": "Product Design", "department": "Creative", "credits": 3, "difficulty": 3, "prerequisites": [], "career_relevance": ["Design", "Engineering"], "learning_style": ["Visual", "Hands-on"], "workload_hours": 7},
            {"id": 16, "code": "INT006", "name": "Animation", "department": "Creative", "credits": 3, "difficulty": 3, "prerequisites": [], "career_relevance": ["Media", "Film", "Art"], "learning_style": ["Visual", "Hands-on"], "workload_hours": 7},
            {"id": 17, "code": "INT007", "name": "Storyboarding", "department": "Creative", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Animation", "Film", "Media"], "learning_style": ["Visual", "Reading"], "workload_hours": 6},
            {"id": 18, "code": "INT008", "name": "Computer Programming", "department": "Technology", "credits": 3, "difficulty": 3, "prerequisites": [], "career_relevance": ["Software Engineering", "IT"], "learning_style": ["Analytical", "Hands-on"], "workload_hours": 8},
            {"id": 19, "code": "INT009", "name": "Cybersecurity", "department": "Technology", "credits": 3, "difficulty": 3, "prerequisites": [], "career_relevance": ["Cybersecurity", "IT"], "learning_style": ["Analytical", "Hands-on"], "workload_hours": 8},
            {"id": 20, "code": "INT010", "name": "Artificial Intelligence", "department": "Technology", "credits": 3, "difficulty": 4, "prerequisites": ["CS101"], "career_relevance": ["AI", "Software", "Data Science"], "learning_style": ["Analytical", "Visual"], "workload_hours": 10},
            {"id": 21, "code": "INT011", "name": "Gaming", "department": "Technology", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Game Development", "IT"], "learning_style": ["Hands-on", "Visual"], "workload_hours": 7},
            {"id": 22, "code": "INT012", "name": "Hardware & Electronics", "department": "Technology", "credits": 3, "difficulty": 3, "prerequisites": [], "career_relevance": ["Electronics", "Engineering"], "learning_style": ["Hands-on", "Analytical"], "workload_hours": 8},
            {"id": 23, "code": "INT013", "name": "Robotics", "department": "Technology", "credits": 3, "difficulty": 3, "prerequisites": ["CS101"], "career_relevance": ["Robotics", "Engineering"], "learning_style": ["Hands-on", "Analytical"], "workload_hours": 9},
            {"id": 24, "code": "INT014", "name": "Construction", "department": "Engineering", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Construction", "Architecture"], "learning_style": ["Hands-on", "Visual"], "workload_hours": 7},
            {"id": 25, "code": "INT015", "name": "Machinery & Mechanics", "department": "Engineering", "credits": 3, "difficulty": 3, "prerequisites": [], "career_relevance": ["Mechanical Engineering"], "learning_style": ["Hands-on", "Analytical"], "workload_hours": 8},
            {"id": 26, "code": "INT016", "name": "Power Systems", "department": "Engineering", "credits": 3, "difficulty": 3, "prerequisites": [], "career_relevance": ["Electrical Engineering"], "learning_style": ["Analytical", "Visual"], "workload_hours": 8},
            {"id": 27, "code": "INT017", "name": "Chemistry & Materials", "department": "Science", "credits": 3, "difficulty": 3, "prerequisites": [], "career_relevance": ["Chemical Engineering", "Materials Science"], "learning_style": ["Analytical", "Hands-on"], "workload_hours": 8},
            {"id": 28, "code": "INT018", "name": "Biology", "department": "Science", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Biology", "Healthcare"], "learning_style": ["Reading", "Visual"], "workload_hours": 7},
            {"id": 29, "code": "INT019", "name": "Physics", "department": "Science", "credits": 3, "difficulty": 3, "prerequisites": [], "career_relevance": ["Engineering", "Physics"], "learning_style": ["Analytical", "Visual"], "workload_hours": 8},
            {"id": 30, "code": "INT020", "name": "Scientific Research", "department": "Science", "credits": 3, "difficulty": 3, "prerequisites": [], "career_relevance": ["Research", "Science"], "learning_style": ["Reading", "Analytical"], "workload_hours": 7},
            {"id": 31, "code": "INT021", "name": "Human Behavior", "department": "Social Science", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Psychology", "Education"], "learning_style": ["Reading", "Visual"], "workload_hours": 6},
            {"id": 32, "code": "INT022", "name": "Politics & Law", "department": "Social Science", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Law", "Government"], "learning_style": ["Reading", "Discussion"], "workload_hours": 7},
            {"id": 33, "code": "INT023", "name": "Teaching", "department": "Education", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Education"], "learning_style": ["Reading", "Discussion"], "workload_hours": 6},
            {"id": 34, "code": "INT024", "name": "Business", "department": "Business", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Business", "Management"], "learning_style": ["Reading", "Analytical"], "workload_hours": 6},
            {"id": 35, "code": "INT025", "name": "Finance", "department": "Business", "credits": 3, "difficulty": 3, "prerequisites": ["ECON101"], "career_relevance": ["Finance", "Business"], "learning_style": ["Analytical", "Reading"], "workload_hours": 8},
            {"id": 36, "code": "INT026", "name": "Leadership", "department": "Business", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Management", "Business"], "learning_style": ["Discussion", "Reading"], "workload_hours": 6},
            {"id": 37, "code": "INT027", "name": "Hospitality", "department": "Business", "credits": 3, "difficulty": 2, "prerequisites": [], "career_relevance": ["Hospitality", "Tourism"], "learning_style": ["Hands-on", "Visual"], "workload_hours": 6}
        ]

        def _load_major_requirements(self) -> Dict[str, List[str]]:
            return {
                "Technology": [
                    "CS101",
                    "MATH151",
                    "ENG101",
                    "INT008",
                    "INT009",
                    "INT010",
                    "INT011",
                    "INT012",
                    "INT013",
                ],
        
                "Engineering": [
                    "MATH151",
                    "PHYS101",
                    "CHEM101",
                    "ENG101",
                    "INT003",
                    "INT024",
                    "INT025",
                    "INT026",
                ],
        
                "Science": [
                    "BIO101",
                    "CHEM101",
                    "MATH151",
                    "ENG101",
                    "INT018",
                    "INT020",
                    "INT017",
                    "INT019",
                    "PHYS101",
                ],
        
                "Social Science": [
                    "PSYCH101",
                    "HIST101",
                    "INT021",
                    "INT022",
                    "PHYS101", 
                ],
        
                "Business": [
                    "ECON101",
                    "MATH151",
                    "ENG101",
                    "INT024",
                    "INT025",
                    "INT026",
                    "INT027",
                ],
        
                "Creative Arts": [
                    "ART101",
                    "INT001",
                    "INT002",
                    "INT004",
                    "INT005",
                    "INT006",
                    "INT007",
                ],
        
                "Education": [
                    "ENG101",
                    "PSYCH101",
                    "INT023",
                ],
        
                "Undecided": [
                    "ENG101",
                    "MATH151",
                    "PSYCH101",
                    "ART101",
                ],
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

    def _match_learning_style(self, student_style, course_styles):
        if not student_style:
            return 0.5
        
        # Perfect match
        if student_style in course_styles:
            return 1.0
        
        # Compatible styles
        compatible = {
            "Visual": ["Hands-on", "Analytical"],
            "Hands-on": ["Visual", "Analytical"],
            "Analytical": ["Visual", "Hands-on", "Reading"],
            "Reading": ["Writing", "Discussion", "Analytical"],
            "Writing": ["Reading", "Discussion"],
            "Discussion": ["Reading", "Writing"],
        }
        
        if student_style in compatible:
            for style in course_styles:
                if style in compatible[student_style]:
                    return 0.75
        
        return 0.35

    @staticmethod
    def _calculate_workload_compatibility(student_hours: float, course_hours: float) -> float:
        if student_hours >= course_hours:
            return 1.0
        if student_hours >= course_hours * 0.7:
            return 0.7
        return 0.4

    def _is_major_requirement(self, course_code: str, major: str) -> bool:
        return course_code in self.major_requirements.get(major, [])

    def _calculate_difficulty_match(self, gpa, difficulty):
        # Find optimal difficulty for this GPA
        if gpa >= 3.8:
            optimal = 3.5
        elif gpa >= 3.4:
            optimal = 3.0
        elif gpa >= 3.0:
            optimal = 2.5
        elif gpa >= 2.6:
            optimal = 2.0
        else:
            optimal = 1.5
        
        # Score based on distance from optimal
        distance = abs(difficulty - optimal)
        
        if distance == 0:
            return 1.0
        elif distance <= 0.5:
            return 0.95
        elif distance <= 1.0:
            return 0.85
        elif distance <= 1.5:
            return 0.70
        elif distance <= 2.0:
            return 0.55
        else:
            return 0.40

    def generate_recommendations(self, student_data: Dict[str, Any], top_n: int = 15) -> List[Dict[str, Any]]:
        """Generate top-N course recommendations for a student."""
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

        recommendations = []

        for course in self.course_database:
            career_score = self._match_career_interests(career_interests, course.get("career_relevance", []))
            learning_score = self._match_learning_style(learning_style, course.get("learning_style", []))
            workload_score = self._calculate_workload_compatibility(study_hours, float(course.get("workload_hours", 8)))
            difficulty_score = self._calculate_difficulty_match(gpa, int(course.get("difficulty", 3)))

            major_req = self._is_major_requirement(course.get("code", ""), major)
            major_bonus = 1 if major_req else 0.3

            base_score = (
                career_score * self.weights["career"]
                + learning_score * self.weights["learning"]
                + workload_score * self.weights["workload"]
                + difficulty_score * self.weights["difficulty"]
                + (1.0 if major_req else 0.5) * self.weights["major"]
            )

            final_score = base_score * major_bonus
            confidence = base_score * 100

            reasoning = self._generate_reasoning(course, major, career_score, learning_score, workload_score, difficulty_score)

            recommendations.append({
                "course_id": course.get("id"),
                "course_code": course.get("code"),
                "course_name": course.get("name"),
                "department": course.get("department"),
                "credits": course.get("credits"),
                "confidence_score": round(confidence, 2),
                "reasoning": reasoning,
                "is_major_requirement": major_req,
            })

        recommendations.sort(key=lambda x: (-x["confidence_score"], x.get("course_code", "")))
        top = recommendations[:max(1, int(top_n))]
        logger.info("Generated %d recommendations for major=%s gpa=%.2f", len(top), major, gpa)
        return top

    def _generate_reasoning(self, course: Dict[str, Any], major: str, career_score: float, 
                          learning_score: float, workload_score: float, difficulty_score: float) -> str:
        reasons = []
        if self._is_major_requirement(course.get("code", ""), major):
            reasons.append(f"Required for {major} major")
        if career_score > 0.7:
            reasons.append("Strong alignment with career interests")
        elif career_score > 0.4:
            reasons.append("Relevant to career goals")
        if learning_score > 0.8:
            reasons.append("Matches learning style perfectly")
        if workload_score > 0.8:
            reasons.append("Workload fits study schedule")
        elif workload_score < 0.5:
            reasons.append("Challenging workload")
        if difficulty_score > 0.8:
            reasons.append("Good match for academic level")
        elif difficulty_score < 0.6:
            reasons.append("May require extra effort")
        if int(course.get("difficulty", 3)) <= 2:
            reasons.append("Great foundational course")
        return " • ".join(reasons) if reasons else "General education requirement"


def cli_main() -> None:
    try:
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
        
        # Output ONLY clean JSON to stdout
        print(json.dumps(recs))
        sys.exit(0)
        
    except Exception as e:
        logger.exception("Fatal error in recommendation engine")
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    cli_main()
