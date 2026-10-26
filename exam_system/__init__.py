"""
Digital Exam & Results Management System
========================================
An open-source, privacy-respecting exam results tool built with
Object-Oriented Programming in Python.

Import the main classes directly from the package:

    from exam_system import ExamRegistry, Subject, Candidate, GradeScale
"""

from .grading import GradeScale
from .models import Candidate, Subject
from .registry import ExamRegistry

__all__ = ("GradeScale", "Subject", "Candidate", "ExamRegistry")
__version__ = "1.0.0"
