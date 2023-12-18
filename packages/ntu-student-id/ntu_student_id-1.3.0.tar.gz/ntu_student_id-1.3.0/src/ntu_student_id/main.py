import json
import os
import re


class Parser:
    def __init__(
        self, student_id: str, accept_evil: bool = True, evil_delimiter: str = " "
    ):
        self.is_over_hundred = False
        self.evil_delimiter = evil_delimiter
        self.accept_evil = accept_evil

        self.student_id = self._set_student_id(student_id)
        self.department_list = self._set_department_list()
        self.is_evil = self._evil_checker()

        self.department_code = self._set_department_code()

        if not self.accept_evil and self.is_evil:
            raise ValueError("Evil Student ID")

    def _set_department_list(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        with open(f"{abs_path}/data/departments.json", "r") as file:
            data = json.loads(file.read())

        return data

    def _validate_student_id(self, student_id: str) -> bool:
        student_id = student_id.strip().upper()

        pattern = r"^[BTRDAVCPFJQDHKS]{1}[0-9]{2}[0-9A-Z]{1}[0-9]{5}$"
        if not re.match(pattern, student_id):
            return False

        return True

    def _set_student_id(self, student_id: str) -> str:
        if self._validate_student_id(student_id):
            return student_id
        else:
            raise ValueError("Invalid Student ID")

    def _validate_department_code(self, department_code: str) -> bool:
        if self.department_list.get(department_code):
            return True
        else:
            raise ValueError("Invalid Department Code")

    def _set_department_code(self) -> str:
        if self.is_over_hundred:
            return f"{self.student_id[3:6]}0"
        else:
            return self.student_id[3:7]

    def _evil_checker(self) -> bool:
        if not self.student_id[3:7].endswith("0"):
            try:
                self._validate_department_code(self.student_id[3:7])
                return True
            except ValueError:
                self.is_over_hundred = True
                self._validate_department_code(f"{self.student_id[3:6]}0"),
        else:
            self._validate_department_code(self.student_id[3:7])
        return False

    def _department_builder(self, type: str):
        output = ""

        if self.is_evil:
            output = self.department_list.get(f"{self.department_code[0:3]}0").get(type)
            if output and self.department_list.get(self.department_code).get(type):
                output += self.evil_delimiter
                output += self.department_list.get(self.department_code).get(type)
        else:
            output = self.department_list.get(self.department_code).get(type)

        return output

    def all(self) -> dict:
        if self.is_evil:
            return {
                "short": self.short(),
                "full": self.full(),
                "additional": self.additional(),
            }
        return self.department_list.get(self.department_code)

    def short(self) -> str:
        return self._department_builder("short")

    def full(self) -> str:
        return self._department_builder("full")

    def additional(self) -> str:
        return self._department_builder("additional")

    def __str__(self):
        return self.full()
