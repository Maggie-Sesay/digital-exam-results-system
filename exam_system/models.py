

import re
from datetime import date

from .grading import GradeScale


class Subject:
    """A subject (course or module) in which candidates sit an examination."""

    
    DEFAULT_PASS_MARK = 40
    DEFAULT_CREDIT_HOURS = 3
    count = 0  # total number of Subject objects created

    def __init__(self, code, title, credit_hours=DEFAULT_CREDIT_HOURS, pass_mark=None):
        code = str(code).strip().upper()
        title = str(title).strip()
        credit_hours = int(credit_hours)
        if pass_mark is None:
            pass_mark = Subject.DEFAULT_PASS_MARK

    
        if not code:
            raise ValueError("Subject code cannot be empty.")
        if not title:
            raise ValueError("Subject title cannot be empty.")
        if credit_hours <= 0:
            raise ValueError("Credit hours must be greater than zero.")
        if not GradeScale.is_valid_score(pass_mark):
            raise ValueError("Pass mark must be a number from 0 to 100.")

        
        self.code = code
        self.title = title
        self.credit_hours = credit_hours
        self.pass_mark = pass_mark

        Subject.count += 1

    # ------------------------------------------------------------------
    # Class method (alternative constructor)
    # ------------------------------------------------------------------
    @classmethod
    def from_tuple(cls, data):
        """Create a Subject from a (code, title, credit_hours) tuple.

        Example:
            >>> Subject.from_tuple(("PROG211", "Object-Oriented Programming 1", 3))
        """
        code, title, credit_hours = data  # tuple unpacking
        return cls(code, title, credit_hours)

    # ------------------------------------------------------------------
    # Instance methods
    # ------------------------------------------------------------------
    def has_passed(self, score):
        """Return True if the score meets this subject's pass mark."""
        return score >= self.pass_mark

    def update_record(self, title=None, credit_hours=None, pass_mark=None):
        """Change one or more details of this subject."""
        if title is not None:
            if not str(title).strip():
                raise ValueError("Subject title cannot be empty.")
            self.title = str(title).strip()
        if credit_hours is not None:
            if int(credit_hours) <= 0:
                raise ValueError("Credit hours must be greater than zero.")
            self.credit_hours = int(credit_hours)
        if pass_mark is not None:
            if not GradeScale.is_valid_score(pass_mark):
                raise ValueError("Pass mark must be a number from 0 to 100.")
            self.pass_mark = pass_mark

    def display_info(self):
        """Print this subject's details."""
        print(f"  {self.code:<10}{self.title:<34}{self.credit_hours:>3} cr   pass {self.pass_mark}")

    def __str__(self):
        return f"{self.code} - {self.title}"


class Candidate:
    """An examination candidate, identified only by an anonymous index number."""

    # ---- Class attributes: shared by every Candidate object ----
    ID_PREFIX = "EXM"
    ID_PATTERN = re.compile(r"^[A-Z]{2,5}-\d{4}-\d{4}$")  # e.g. EXM-2026-0001
    _next_serial = 1  # used by register() to issue the next index number
    count = 0         # total number of Candidate objects created

    def __init__(self, candidate_id, programme, level):
        candidate_id = str(candidate_id).strip().upper()
        programme = str(programme).strip()
        level = str(level).strip()

        if not Candidate.is_valid_id(candidate_id):
            raise ValueError(
                f"Invalid index number {candidate_id!r}. Expected a format like EXM-2026-0001."
            )
        if not programme:
            raise ValueError("Programme cannot be empty.")
        if not level:
            raise ValueError("Level cannot be empty.")

        # ---- Instance attributes ----
        self.candidate_id = candidate_id
        self.programme = programme
        self.level = level
        self.scores = {}  # dictionary: {subject_code: score}

        Candidate.count += 1


    @classmethod
    def register(cls, programme, level, year=None):
        """Create a new Candidate with an automatically issued index number.

        The class (cls) keeps track of the next serial number, so every
        candidate registered this way receives a unique, anonymous ID.
        """
        if year is None:
            year = date.today().year
        candidate_id = f"{cls.ID_PREFIX}-{year}-{cls._next_serial:04d}"
        cls._next_serial += 1
        return cls(candidate_id, programme, level)

    @classmethod
    def reset_serial(cls, start=1):
        """Restart index-number numbering (for example, at a new exam session)."""
        cls._next_serial = start


    @staticmethod
    def is_valid_id(candidate_id):
        """Return True if the text matches the index-number format."""
        return bool(Candidate.ID_PATTERN.match(str(candidate_id).strip().upper()))


    def record_score(self, subject, score):
        """Record this candidate's score in a Subject.
        """
        if not isinstance(subject, Subject):
            raise TypeError("record_score() expects a Subject object.")
        if not GradeScale.is_valid_score(score):
            raise ValueError("Score must be a number from 0 to 100.")
        self.scores[subject.code] = float(score)

    def update_record(self, programme=None, level=None):
        """Change the candidate's programme and/or level."""
        if programme is not None:
            if not str(programme).strip():
                raise ValueError("Programme cannot be empty.")
            self.programme = str(programme).strip()
        if level is not None:
            if not str(level).strip():
                raise ValueError("Level cannot be empty.")
            self.level = str(level).strip()

    def calculate_gpa(self, subjects):

        total_points = 0.0
        total_credits = 0
        for code, score in self.scores.items():
            credits = subjects[code].credit_hours
            letter, grade_point, remark = GradeScale.grade_for(score)
            total_points += grade_point * credits
            total_credits += credits
        if total_credits == 0:
            return 0.0
        return round(total_points / total_credits, 2)

    def failed_subjects(self, subjects):
        """Return a tuple of subject codes this candidate has failed."""
        failed = ()
        for code, score in self.scores.items():
            if not subjects[code].has_passed(score):
                failed += (code,)
        return failed

    def result_status(self, subjects):
        """Return 'PASS', 'REFER' (resit needed) or 'NO RESULTS'."""
        if not self.scores:
            return "NO RESULTS"
        return "REFER" if self.failed_subjects(subjects) else "PASS"

    def display_info(self):
        """Print the candidate's basic details."""
        print(f"  Index Number : {self.candidate_id}")
        print(f"  Programme    : {self.programme}")
        print(f"  Level        : {self.level}")
        print(f"  Subjects sat : {len(self.scores)}")

    def __str__(self):
        return f"{self.candidate_id} ({self.programme}, {self.level})"
