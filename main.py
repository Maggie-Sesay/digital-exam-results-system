"""
main.py
-------
Text-based menu for the Digital Exam & Results Management System.

Usage:
    python main.py          # interactive menu
    python main.py --demo   # automatic demonstration using sample data

The interface is plain text and keyboard-only, so it works with screen
readers, on low-specification computers and without an internet connection
(inclusive and accessible design - a DPG principle).
"""

import sys

from exam_system import Candidate, ExamRegistry, GradeScale, Subject

# Menu options stored as a tuple of tuples: (key, description).
MENU = (
    ("1", "Register a subject"),
    ("2", "Register a candidate"),
    ("3", "Record a score"),
    ("4", "Update a candidate's details"),
    ("5", "Display all subjects"),
    ("6", "Display all candidates"),
    ("7", "Print a candidate's result slip"),
    ("8", "Show subject statistics"),
    ("9", "Show grading scale"),
    ("10", "Export results to CSV"),
    ("11", "Load sample data"),
    ("0", "Exit"),
)


# ----------------------------------------------------------------------
# Input helpers - re-ask until the user gives a usable answer
# ----------------------------------------------------------------------
def ask(prompt):
    return input(f"  {prompt}").strip()


def ask_required(prompt):
    while True:
        answer = ask(prompt)
        if answer:
            return answer
        print("  ! This field is required. Please try again.")


def ask_number(prompt, cast=float):
    while True:
        answer = ask(prompt)
        try:
            return cast(answer)
        except ValueError:
            print("  ! Please enter a number.")


def heading(text):
    print("\n" + "  " + "#" * 68)
    print(f"  # {text}")
    print("  " + "#" * 68)


# ----------------------------------------------------------------------
# Menu actions
# ----------------------------------------------------------------------
def register_subject(registry):
    code = ask_required("Subject code (e.g. PROG211): ")
    title = ask_required("Subject title: ")
    credits = ask_number(f"Credit hours [{Subject.DEFAULT_CREDIT_HOURS}]: ", int)
    subject = registry.add_subject(Subject(code, title, credits))
    print(f"  > Subject registered: {subject}")


def register_candidate(registry):
    print("  (No names or personal details are collected - an anonymous index number is issued.)")
    programme = ask_required("Programme: ")
    level = ask_required("Level (e.g. Year 1): ")
    candidate = registry.add_candidate(Candidate.register(programme, level))
    print(f"  > Candidate registered with index number {candidate.candidate_id}")


def record_score(registry):
    candidate_id = ask_required("Candidate index number: ")
    subject_code = ask_required("Subject code: ")
    score = ask_number("Score (0-100): ")
    registry.record_score(candidate_id, subject_code, score)
    letter, grade_point, remark = GradeScale.grade_for(score)
    print(f"  > Score saved: {score:.1f} = grade {letter} ({remark})")


def update_candidate(registry):
    candidate = registry.get_candidate(ask_required("Candidate index number: "))
    print("  Press Enter to keep the current value.")
    programme = ask(f"Programme [{candidate.programme}]: ") or None
    level = ask(f"Level [{candidate.level}]: ") or None
    candidate.update_record(programme=programme, level=level)
    print(f"  > Updated: {candidate}")


def print_slip(registry):
    registry.print_result_slip(ask_required("Candidate index number: "))


def export_csv(registry):
    file_name = ask("File name [results.csv]: ") or "results.csv"
    rows = registry.export_results_csv(file_name)
    print(f"  > Exported {rows} result rows to {file_name}")


def load_sample(registry):
    sample = ExamRegistry.with_sample_data()
    registry.exam_title = sample.exam_title
    registry.subjects = sample.subjects
    registry.candidates = sample.candidates
    print(f"  > Loaded {len(registry.subjects)} subjects and {len(registry.candidates)} candidates.")


# Each menu key maps to the function that handles it (a dictionary of functions).
ACTIONS = {
    "1": register_subject,
    "2": register_candidate,
    "3": record_score,
    "4": update_candidate,
    "5": lambda r: r.display_subjects(),
    "6": lambda r: r.display_candidates(),
    "7": print_slip,
    "8": lambda r: r.display_statistics(),
    "9": lambda r: GradeScale.display(),
    "10": export_csv,
    "11": load_sample,
}


def show_menu():
    print("\n  " + "=" * 50)
    print("  DIGITAL EXAM & RESULTS MANAGEMENT SYSTEM")
    print("  " + "=" * 50)
    for key, label in MENU:
        print(f"  {key:>2}. {label}")
    print("  " + "=" * 50)


def run_menu():
    registry = ExamRegistry("End of Semester Examinations")
    while True:
        show_menu()
        choice = ask("Choose an option: ")
        if choice == "0":
            print("  Goodbye.")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("  ! Invalid option. Enter a number from the menu.")
            continue
        try:
            action(registry)
        except (ValueError, LookupError, TypeError, OSError) as error:
            # Friendly message instead of a crash (accessible design).
            print(f"  ! {error}")


# ----------------------------------------------------------------------
# Automatic demonstration (used for the sample output and screenshots)
# ----------------------------------------------------------------------
def run_demo():
    heading("TASK 1 - Creating objects and making them interact")
    oop = Subject("PROG211", "Object-Oriented Programming 1", 4)
    web = Subject.from_tuple(("DCOMP204", "Web Design", 3))  # class method
    print(f"  Created Subject object : {oop}")
    print(f"  Created Subject object : {web}")

    Candidate.reset_serial()
    student = Candidate.register("BSc Software Engineering", "Year 2", 2026)  # class method
    print(f"  Created Candidate      : {student}")

    student.record_score(oop, 78)  # Candidate object receives a Subject object
    student.record_score(web, 36)
    print(f"  Scores recorded        : {student.scores}")
    print(f"  Passed {web.code}?       : {web.has_passed(student.scores[web.code])}")

    student.update_record(level="Year 3")  # instance method
    print(f"  After update_record()  : {student}")

    heading("TASK 2 - Storing many objects in a DICTIONARY")
    registry = ExamRegistry.with_sample_data(2026)
    print("  registry.candidates keys:")
    for key in registry.candidates:
        print(f"    {key!r}")
    registry.display_subjects()
    registry.display_candidates()

    heading("TASK 3 - Instance, class and static methods")
    first = registry.get_candidate("EXM-2026-0001")
    new_candidate = Candidate.register("Diploma in ICT", "Year 1", 2026)
    demos = (
        ("Instance", "first.calculate_gpa(subjects)", first.calculate_gpa(registry.subjects)),
        ("Instance", "first.result_status(subjects)", first.result_status(registry.subjects)),
        ("Class", "Candidate.register(...)", new_candidate.candidate_id),
        ("Static", "GradeScale.grade_for(67)", GradeScale.grade_for(67)),
        ("Static", "Candidate.is_valid_id('EXM-2026-0001')", Candidate.is_valid_id("EXM-2026-0001")),
        ("Static", "Candidate.is_valid_id('John Doe')", Candidate.is_valid_id("John Doe")),
    )
    for kind, call, result in demos:
        print(f"  {kind:<9}{call:<40} -> {result}")
    print(f"  Class attributes (objects created so far): Subject.count = {Subject.count}, "
          f"Candidate.count = {Candidate.count}")
    registry.print_result_slip("EXM-2026-0003")
    registry.print_result_slip("EXM-2026-0002")

    heading("BONUS - Tuples (immutable grading scale)")
    print(f"  GradeScale.BANDS[0] = {GradeScale.BANDS[0]}")
    GradeScale.display()
    try:
        GradeScale.BANDS[0] = (90, "A", 4.0, "Excellent")
    except TypeError as error:
        print(f"  Attempt to edit the scale was blocked: TypeError: {error}")

    heading("REPORTING and VALIDATION")
    registry.display_statistics()
    for bad_score in (105, -3):
        try:
            registry.record_score("EXM-2026-0001", "PROG211", bad_score)
        except ValueError as error:
            print(f"  Score {bad_score} rejected: {error}")
    try:
        registry.get_candidate("EXM-2026-9999")
    except LookupError as error:
        print(f"  Lookup rejected: {error}")


def main(argv):
    if "--demo" in argv:
        run_demo()
    else:
        try:
            run_menu()
        except (KeyboardInterrupt, EOFError):
            print("\n  Goodbye.")


if __name__ == "__main__":
    main(sys.argv[1:])
