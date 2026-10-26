"""
grading.py
----------
The official grading scale for the Digital Exam & Results Management System.

The scale is stored as a TUPLE OF TUPLES. A tuple cannot be changed after it
is created (it is immutable). That is exactly what an official grading scale
needs: no part of the program can edit the grade boundaries by mistake while
results are being processed.

To adapt the system for another institution, edit BANDS below - nothing else
in the program needs to change (modular and reusable - a DPG principle).
"""


class GradeScale:
    """Converts a raw exam score (0-100) into a letter grade.

    Every method in this class is a @staticmethod. Grading does not depend on
    any particular candidate or subject, so the methods need neither an object
    (self) nor the class (cls). The class simply groups related tools together.
    """

    # Each band is a tuple: (minimum score, letter grade, grade point, remark)
    # Bands are ordered from highest to lowest; the first band that matches wins.
    BANDS = (
        (70, "A", 4.0, "Excellent"),
        (60, "B", 3.0, "Very Good"),
        (50, "C", 2.0, "Credit"),
        (40, "D", 1.0, "Pass"),
        (0,  "F", 0.0, "Fail"),
    )

    MIN_SCORE = 0
    MAX_SCORE = 100

    @staticmethod
    def is_valid_score(score):
        """Return True if score is a number from 0 to 100 (inclusive)."""
        # bool is a subclass of int in Python, so reject True/False explicitly.
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            return False
        return GradeScale.MIN_SCORE <= score <= GradeScale.MAX_SCORE

    @staticmethod
    def grade_for(score):
        """Return a (letter, grade_point, remark) tuple for a valid score.

        Example:
            >>> GradeScale.grade_for(78)
            ('A', 4.0, 'Excellent')
        """
        if not GradeScale.is_valid_score(score):
            raise ValueError(f"Score must be a number from 0 to 100, got {score!r}.")

        # Tuple unpacking: each band is split into four named variables.
        for minimum, letter, grade_point, remark in GradeScale.BANDS:
            if score >= minimum:
                return (letter, grade_point, remark)

    @staticmethod
    def display():
        """Print the grading scale as a table."""
        print("\n  GRADING SCALE")
        print("  " + "-" * 44)
        print(f"  {'Score range':<14}{'Grade':<8}{'Points':<9}{'Remark'}")
        print("  " + "-" * 44)
        upper = GradeScale.MAX_SCORE
        for minimum, letter, grade_point, remark in GradeScale.BANDS:
            score_range = f"{minimum}-{upper}"
            print(f"  {score_range:<14}{letter:<8}{grade_point:<9.1f}{remark}")
            upper = minimum - 1
        print("  " + "-" * 44)
