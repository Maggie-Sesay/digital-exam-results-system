# Digital Exam & Results Management System

An open-source, privacy-respecting Python program that helps an exams office register subjects and candidates, record scores, grade them, and print provisional result slips — built with Object-Oriented Programming (OOP) and aligned with the **Digital Public Goods (DPG) Standard**.

> **Course:** PROG211 Object-Oriented Programming 1 — Individual Assignment (10%)
> **Institution:** Limkokwing University of Creative Technology, Sierra Leone
> **Domain:** Education — *Digital Exam & Results Management System*
> **Student:** Margaret Sesay 905005886
> **Lecturer:** Amandus Benjamin Coker

---

## 1. The real-world problem

In many schools and colleges, exam scores are still recorded on paper mark sheets or loose spreadsheets. Results are graded by hand, grade points are calculated manually, and result slips are typed one by one. This is slow, error-prone (a wrong grade boundary or GPA sum affects a student's progression), and personal details are often copied into many places where they are not needed.

This program solves that by:

- issuing every candidate an **anonymous index number** instead of storing names;
- grading every score against **one fixed, official grading scale**;
- calculating a **credit-weighted GPA** and pass/refer status automatically;
- printing **provisional result slips** and **subject statistics** (pass rate, average, highest, lowest);
- **exporting results to CSV**, an open format any spreadsheet program can read.

---

## 2. How to run

**Requirements:** Python 3.8 or newer. No extra packages — only the Python standard library is used.

```bash
git clone https://github.com/Maggie-Sesay/digital-exam-results-system.git
cd digital-exam-results-system

python main.py          # interactive menu
python main.py --demo   # automatic demonstration with sample data
python -m unittest discover -s tests -v   # run the 17 automated tests
```

On some computers the command is `python3` instead of `python`.

---

## 3. Project structure

```
digital-exam-results-system/
├── main.py                  # menu interface + --demo mode
├── exam_system/             # reusable package
│   ├── __init__.py
│   ├── grading.py           # GradeScale  (tuple-based grading scale, static methods)
│   ├── models.py            # Subject, Candidate  (core domain classes)
│   └── registry.py          # ExamRegistry  (dictionary storage, add/display, reports)

├── LICENSE                  # MIT open-source licence
└── README.md
```

---

## 4. How the assignment requirements are met

| Requirement (brief) | Where it is in the code |
|---|---|
| **Task 1 — at least two classes** | `Subject`, `Candidate` (models.py), `ExamRegistry` (registry.py), `GradeScale` (grading.py) |
| Attributes | `Subject`: `code`, `title`, `credit_hours`, `pass_mark` · `Candidate`: `candidate_id`, `programme`, `level`, `scores` |
| Methods such as `update_record()` / `display_info()` | Both `Subject` and `Candidate` have `update_record()` and `display_info()` |
| Object creation and interaction | `candidate.record_score(subject, score)` — a `Candidate` object receives a `Subject` object; `ExamRegistry` combines both to print result slips |
| **Task 2 — one data structure** | **Dictionary.** `registry.subjects = {code: Subject}` and `registry.candidates = {index_number: Candidate}`; each candidate's `scores = {subject_code: score}` |
| Function to **add** records | `ExamRegistry.add_subject()`, `ExamRegistry.add_candidate()` |
| Function to **display** records | `ExamRegistry.display_subjects()`, `ExamRegistry.display_candidates()`, `print_result_slip()` |
| *Bonus — tuples* | `GradeScale.BANDS` (immutable grading scale), `Subject.from_tuple()`, `GradeScale.grade_for()` returns a tuple, `failed_subjects()` returns a tuple, the `MENU` is a tuple of tuples |
| **Task 3 — instance method** | `record_score()`, `calculate_gpa()`, `result_status()`, `update_record()`, `has_passed()`, `display_info()` |
| **Class method** (`@classmethod`) | `Candidate.register()` (issues the next anonymous ID), `Candidate.reset_serial()`, `Subject.from_tuple()`, `ExamRegistry.with_sample_data()` |
| **Static method** (`@staticmethod`) | `GradeScale.is_valid_score()`, `GradeScale.grade_for()`, `GradeScale.display()`, `Candidate.is_valid_id()` |
| Class attributes | `Subject.DEFAULT_PASS_MARK`, `Subject.count`, `Candidate.ID_PREFIX`, `Candidate.count` |

**Why a dictionary?** Exam officers always look up a record by its subject code or index number. A dictionary finds a record directly by that key and naturally prevents duplicates — two candidates can never share an index number.

---

## 5. Alignment with Digital Public Goods (DPG) standards

The assignment names four DPG principles. Each is built into the program, not just described:

### Open source
- Published publicly on GitHub under the **MIT Licence** (see `LICENSE`), so anyone may use, study, change and share it.
- Uses only the Python standard library — no paid or proprietary dependencies.

### Inclusive and accessible design
- **Plain-text, keyboard-only interface** that works with screen readers. No information is shown by colour alone.
- Runs **offline** on low-specification and older computers, on Windows, macOS and Linux.
- Clear prompts in simple English, with examples (e.g. `Subject code (e.g. PROG211)`).
- **Mistakes never crash the program:** invalid input shows a friendly message (`! Please enter a number.`) and asks again.

### Privacy-respecting (no sensitive personal data stored)
- **Privacy by design:** the `Candidate` class has *no* attributes for name, date of birth, phone, address, email or photograph — the program cannot store them even by mistake.
- Candidates are identified only by an **anonymous index number** (`EXM-2026-0001`) issued by `Candidate.register()`. The link between an index number and a real person stays with the exams office, outside the software.
- Data is held in memory only. The optional CSV export contains index numbers, programme, level and grades — no personal data. An automated test (`test_no_personal_data_attributes`) checks this.

### Modular and reusable
- Split into a reusable package (`exam_system`) with one responsibility per module: grading, domain models, storage/reporting. The menu (`main.py`) is separate from the logic.
- Another institution can change its grading scale by editing **only** `GradeScale.BANDS`, or change the pass mark with `Subject.DEFAULT_PASS_MARK`.
- The package can be imported into other programs: `from exam_system import ExamRegistry, Subject, Candidate`.

### Mapping to the nine DPG Standard indicators

| # | DPG indicator | How this project addresses it |
|---|---|---|
| 1 | Relevance to the SDGs | SDG 4 (Quality Education) — faster, accurate, fair results; SDG 16 (Strong Institutions) — transparent, consistent grading |
| 2 | Approved open licence | MIT Licence |
| 3 | Clear ownership | Author and copyright stated in `LICENSE` and this README |
| 4 | Platform independence | Standard-library Python only; runs on any operating system |
| 5 | Documentation | This README, code comments and docstrings in every class and method |
| 6 | Data extraction | Export to CSV, a non-proprietary format (menu option 10) |
| 7 | Privacy and applicable laws | No personal data collected; anonymous IDs only |
| 8 | Standards and best practices | PEP 8 style, input validation, 17 automated unit tests |
| 9 | Do no harm by design | Immutable grading scale prevents tampering; duplicate and invalid records are rejected |

---

## 6. Example usage (sample input / output)

### Interactive menu

```
  ==================================================
  DIGITAL EXAM & RESULTS MANAGEMENT SYSTEM
  ==================================================
   1. Register a subject
   2. Register a candidate
   3. Record a score
   4. Update a candidate's details
   5. Display all subjects
   6. Display all candidates
   7. Print a candidate's result slip
   8. Show subject statistics
   9. Show grading scale
  10. Export results to CSV
  11. Load sample data
   0. Exit
  ==================================================
  Choose an option: 1
  Subject code (e.g. PROG211): PROG211
  Subject title: Object-Oriented Programming 1
  Credit hours [3]: 4
  > Subject registered: PROG211 - Object-Oriented Programming 1

  Choose an option: 2
  (No names or personal details are collected - an anonymous index number is issued.)
  Programme: BSc Software Engineering
  Level (e.g. Year 1): Year 2
  > Candidate registered with index number EXM-2026-0001

  Choose an option: 3
  Candidate index number: EXM-2026-0001
  Subject code: MATH201
  Score (0-100): abc
  ! Please enter a number.
  Score (0-100): 37
  > Score saved: 37.0 = grade F (Fail)

  Choose an option: 3
  Candidate index number: EXM-2026-0001
  Subject code: PROG211
  Score (0-100): 120
  ! Score must be a number from 0 to 100.
```

### Result slip (option 7)

```
  ====================================================================
  PROVISIONAL RESULT SLIP - END OF SEMESTER EXAMINATIONS
  ====================================================================
  Index Number : EXM-2026-0001
  Programme    : BSc Software Engineering
  Level        : Year 2
  Subjects sat : 2
  --------------------------------------------------------------------
  Code      Subject                        Score  Grade  Remark
  --------------------------------------------------------------------
  PROG211   Object-Oriented Programming 1   81.0      A  Excellent
  MATH201   Discrete Mathematics            37.0      F  Fail
  --------------------------------------------------------------------
  GPA: 2.29    Status: REFER
  Resit required in: MATH201
  ====================================================================
```

### Using the classes in your own code

```python
from exam_system import ExamRegistry, Subject, Candidate, GradeScale

registry = ExamRegistry("Mid-Semester Tests 2026")
oop = registry.add_subject(Subject.from_tuple(("PROG211", "Object-Oriented Programming 1", 4)))
student = registry.add_candidate(Candidate.register("Diploma in ICT", "Year 1"))

registry.record_score(student.candidate_id, "PROG211", 74)
print(GradeScale.grade_for(74))            # ('A', 4.0, 'Excellent')
print(student.calculate_gpa(registry.subjects))   # 4.0
registry.print_result_slip(student.candidate_id)
```

### Grading scale (sample, configurable)

| Score | Grade | Points | Remark |
|---|---|---|---|
| 70–100 | A | 4.0 | Excellent |
| 60–69 | B | 3.0 | Very Good |
| 50–59 | C | 2.0 | Credit |
| 40–49 | D | 1.0 | Pass |
| 0–39 | F | 0.0 | Fail |

All sample data in this repository is fictional.

---

