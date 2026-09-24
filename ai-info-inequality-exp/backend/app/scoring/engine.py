import json
from pathlib import Path
from typing import Dict, Any, Tuple

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "ground_truth"

class ScoringEngine:
    SCENARIO_FILES = {
        "PMEGP": DATA_DIR / "pmegp.json",
        "PM_VISHWAKARMA": DATA_DIR / "pm_vishwakarma.json",
        "PM_SVANIDHI": DATA_DIR / "pm_svanidhi.json"
    }

    @classmethod
    def load_rubric(cls, task_id: str) -> Dict[str, Any]:
        file_path = cls.SCENARIO_FILES.get(task_id)
        if not file_path or not file_path.exists():
            raise ValueError(f"Ground truth rubric file not found for task_id: {task_id}")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def score_decision(cls, task_id: str, answers: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        rubric_data = cls.load_rubric(task_id)
        fields = rubric_data["ground_truth_rubric"]["fields"]

        total_score = 0.0
        breakdown = {}

        for field in fields:
            key = field["field_key"]
            points = field["points"]
            field_type = field["field_type"]

            submitted_val = answers.get(key)

            if submitted_val is None:
                breakdown[key] = {
                    "points_earned": 0.0,
                    "max_points": points,
                    "status": "MISSING",
                    "submitted": None,
                    "correct": field.get("correct_answer") or field.get("correct_items")
                }
                continue

            if field_type == "boolean":
                is_correct = bool(submitted_val) == bool(field["correct_answer"])
                earned = points if is_correct else 0.0
                breakdown[key] = {
                    "points_earned": earned,
                    "max_points": points,
                    "status": "CORRECT" if is_correct else "INCORRECT",
                    "submitted": submitted_val,
                    "correct": field["correct_answer"]
                }
                total_score += earned

            elif field_type == "number":
                try:
                    num_val = float(submitted_val)
                    accepted_range = field["accepted_range"]
                    is_correct = accepted_range[0] <= num_val <= accepted_range[1]
                    earned = points if is_correct else 0.0
                    breakdown[key] = {
                        "points_earned": earned,
                        "max_points": points,
                        "status": "CORRECT" if is_correct else "INCORRECT",
                        "submitted": num_val,
                        "correct": field["correct_answer"]
                    }
                    total_score += earned
                except (ValueError, TypeError):
                    breakdown[key] = {
                        "points_earned": 0.0,
                        "max_points": points,
                        "status": "INVALID_TYPE",
                        "submitted": submitted_val,
                        "correct": field["correct_answer"]
                    }

            elif field_type == "multi_select":
                correct_items = set(field["correct_items"])
                if isinstance(submitted_val, list):
                    submitted_items = set(submitted_val)
                    
                    correct_hits = len(submitted_items.intersection(correct_items))
                    invalid_hits = len(submitted_items.difference(correct_items))
                    
                    per_item_pts = points / len(correct_items)
                    earned = max(0.0, (correct_hits * per_item_pts) - (invalid_hits * 0.25))
                    earned = min(points, earned)

                    breakdown[key] = {
                        "points_earned": round(earned, 2),
                        "max_points": points,
                        "status": "FULL_CREDIT" if earned == points else "PARTIAL_CREDIT" if earned > 0 else "INCORRECT",
                        "submitted": submitted_val,
                        "correct": field["correct_items"]
                    }
                    total_score += earned
                else:
                    breakdown[key] = {
                        "points_earned": 0.0,
                        "max_points": points,
                        "status": "INVALID_TYPE",
                        "submitted": submitted_val,
                        "correct": field["correct_items"]
                    }

        total_score = round(max(0.0, min(10.0, total_score)), 2)
        return total_score, breakdown
