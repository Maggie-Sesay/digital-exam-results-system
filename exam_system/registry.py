"""
registry.py
-----------
ExamRegistry stores and manages every Subject and Candidate for one
examination session.

DATA STRUCTURE: DICTIONARY
Records are kept in Python dictionaries, keyed by each object's unique ID:

    self.subjects   = {"PROG211": <Subject>, "DCOMP204": <Subject>, ...}
    self.candidates = {"EXM-2026-0001": <Candidate>, ...}

A dictionary was chosen over a list because exam officers always look a
record up by its code or index number. A dictionary finds a record directly
by its key, and it rejects duplicates naturally: two candidates can never
share an index number.
"""

import csv

from .grading import GradeScale
from .models import Candidate, Subject


class ExamRegistry:
    """Holds all subjects, candidates and scores for one exam session."""

    LINE_WIDTH = 68

    def __init__(self, exam_title):
        self.exam_title = str(exam_title).strip()
        self.subjects = {}    # {subject_code: Subject}
        self.candidates = {}  # {candidate_id: Candidate}

    # ------------------------------------------------------------------
    # ADD records to the dictionary
    # ------------------------------------------------------------------
    def add_subject(self, subject):
        """Add a Subject object to the registry, keyed by its code."""
        if not isinstance(subject, Subject):
            raise TypeError("add_subject() expects a Subject object.")
        if subject.code in self.subjects:
            raise ValueError(f"Subject {subject.code} is already registered.")
        self.subjects[subject.code] = subject
        return subject

    def add_candidate(self, candidate):
        """Add a Candidate object to the registry, keyed by index number."""
        if not isinstance(candidate, Candidate):
            raise TypeError("add_candidate() expects a Candidate object.")
        if candidate.candidate_id in self.candidates:
            raise ValueError(f"Candidate {candidate.candidate_id} is already registered.")
        self.candidates[candidate.candidate_id] = candidate
        return candidate

    # ------------------------------------------------------------------
    # LOOK UP records by key
    # ------------------------------------------------------------------
    def get_subject(self, subject_code):
        code = str(subject_code).strip().upper()
        if code not in self.subjects:
            raise LookupError(f"No subject with code {code}.")
        return self.subjects[code]

    def get_candidate(self, candidate_id):
        cid = str(candidate_id).strip().upper()
        if cid not in self.candidates:
            raise LookupError(f"No candidate with index number {cid}.")
        return self.candidates[cid]

    def record_score(self, candidate_id, subject_code, score):
        """Find both objects by key, then let the Candidate record the score."""
        candidate = self.get_candidate(candidate_id)
        subject = self.get_subject(subject_code)
        candidate.record_score(subject, score)
        return candidate


    def display_subjects(self):
        """Loop through the subjects dictionary and print every subject."""
        print(f"\n  REGISTERED SUBJECTS ({len(self.subjects)})")
        print("  " + "-" * self.LINE_WIDTH)
        if not self.subjects:
            print("  No subjects registered yet.")
            return
        for subject in self.subjects.values():
            subject.display_info()
        print("  " + "-" * self.LINE_WIDTH)

    def display_candidates(self):
        """Loop through the candidates dictionary and print a summary table."""
        print(f"\n  REGISTERED CANDIDATES ({len(self.candidates)})")
        print("  " + "-" * self.LINE_WIDTH)
        if not self.candidates:
            print("  No candidates registered yet.")
            return
        print(f"  {'Index Number':<16}{'Programme':<26}{'Level':<8}{'Sat':>4}{'GPA':>6}  Status")
        print("  " + "-" * self.LINE_WIDTH)
        for cid, candidate in self.candidates.items():
            gpa = candidate.calculate_gpa(self.subjects)
            status = candidate.result_status(self.subjects)
            print(
                f"  {cid:<16}{candidate.programme[:25]:<26}{candidate.level[:7]:<8}"
                f"{len(candidate.scores):>4}{gpa:>6.2f}  {status}"
            )
        print("  " + "-" * self.LINE_WIDTH)

    def print_result_slip(self, candidate_id):
        """Print a full provisional result slip for one candidate."""
        candidate = self.get_candidate(candidate_id)
        width = self.LINE_WIDTH

        print("\n  " + "=" * width)
        print(f"  PROVISIONAL RESULT SLIP - {self.exam_title}".upper())
        print("  " + "=" * width)
        candidate.display_info()
        print("  " + "-" * width)

        if not candidate.scores:
            print("  No scores recorded for this candidate yet.")
            print("  " + "=" * width)
            return

        print(f"  {'Code':<10}{'Subject':<30}{'Score':>6}{'Grade':>7}  Remark")
        print("  " + "-" * width)
        for code, score in candidate.scores.items():
            subject = self.subjects[code]
            letter, grade_point, remark = GradeScale.grade_for(score)
            print(f"  {code:<10}{subject.title[:29]:<30}{score:>6.1f}{letter:>7}  {remark}")
        print("  " + "-" * width)

        gpa = candidate.calculate_gpa(self.subjects)
        status = candidate.result_status(self.subjects)
        failed = candidate.failed_subjects(self.subjects)
        print(f"  GPA: {gpa:.2f}    Status: {status}")
        if failed:
            print(f"  Resit required in: {', '.join(failed)}")
        print("  " + "=" * width)

    # ------------------------------------------------------------------
    # REPORTING
    # ------------------------------------------------------------------
    def subject_statistics(self, subject_code):
        """Return a dictionary of statistics for one subject."""
        subject = self.get_subject(subject_code)
        sat = passed = 0
        total = 0.0
        highest = None
        lowest = None
        for candidate in self.candidates.values():
            if subject.code in candidate.scores:
                score = candidate.scores[subject.code]
                sat += 1
                total += score
                if subject.has_passed(score):
                    passed += 1
                highest = score if highest is None else max(highest, score)
                lowest = score if lowest is None else min(lowest, score)
        return {
            "code": subject.code,
            "sat": sat,
            "passed": passed,
            "pass_rate": round(passed / sat * 100, 1) if sat else 0.0,
            "average": round(total / sat, 1) if sat else 0.0,
            "highest": highest,
            "lowest": lowest,
        }

    def display_statistics(self):
        """Print pass rate and score statistics for every subject."""
        print("\n  SUBJECT STATISTICS")
        print("  " + "-" * self.LINE_WIDTH)
        print(f"  {'Code':<10}{'Sat':>5}{'Passed':>8}{'Pass %':>9}{'Average':>9}{'High':>7}{'Low':>7}")
        print("  " + "-" * self.LINE_WIDTH)
        for code in self.subjects:
            s = self.subject_statistics(code)
            high = f"{s['highest']:.0f}" if s["highest"] is not None else "-"
            low = f"{s['lowest']:.0f}" if s["lowest"] is not None else "-"
            print(
                f"  {code:<10}{s['sat']:>5}{s['passed']:>8}{s['pass_rate']:>8.1f}%"
                f"{s['average']:>9.1f}{high:>7}{low:>7}"
            )
        print("  " + "-" * self.LINE_WIDTH)

    def export_results_csv(self, file_path):
        """Export all results to a CSV file (an open, non-proprietary format).

        Only anonymous index numbers, subject codes and grades are written,
        so the exported file contains no personal data.
        Returns the number of result rows written.
        """
        rows = 0
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(("candidate_id", "programme", "level", "subject_code",
                             "score", "grade", "grade_point", "remark"))
            for cid, candidate in self.candidates.items():
                for code, score in candidate.scores.items():
                    letter, grade_point, remark = GradeScale.grade_for(score)
                    writer.writerow((cid, candidate.programme, candidate.level,
                                     code, score, letter, grade_point, remark))
                    rows += 1
        return rows


    @classmethod
    def with_sample_data(cls, year=2026):
        """Return a registry pre-loaded with sample subjects, candidates and scores.

        All sample data is fictional and anonymous.
        """
        registry = cls(f"End of Semester Examinations {year}")

        # Subjects are built from tuples using the Subject.from_tuple() class method.
        subject_data = (
            ("PROG211", "Object-Oriented Programming 1", 4),
            ("DCOMP204", "Web Design", 3),
            ("MATH201", "Discrete Mathematics", 3),
            ("NETW201", "Computer Networks", 3),
        )
        for data in subject_data:
            registry.add_subject(Subject.from_tuple(data))

        # Candidates receive automatic anonymous IDs from Candidate.register().
        Candidate.reset_serial()
        candidate_data = (
            ("BSc Software Engineering", "Year 2", (78, 65, 54, 71)),
            ("BSc Software Engineering", "Year 2", (62, 48, 35, 58)),
            ("Diploma in ICT", "Year 1", (88, 92, 74, 81)),
            ("BSc Business IT", "Year 2", (45, 57, 41, 39)),
        )
        codes = tuple(registry.subjects)  # ("PROG211", "DCOMP204", ...)
        for programme, level, scores in candidate_data:
            candidate = registry.add_candidate(Candidate.register(programme, level, year))
            for code, score in zip(codes, scores):
                registry.record_score(candidate.candidate_id, code, score)

        return registry
