import json
import os
import re


class Parser:
    def __init__(self, student_id: str):
        self.student_id = self._set_student_id(student_id)
        self.department_list = self._set_department_list()
        self.department_code = self._set_department_code()

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
        if department_code in self.department_list.keys():
            return True
        else:
            return False

    def _set_department_code(self) -> str:
        if self._validate_department_code(self.student_id[3:7]):
            return self.student_id[3:7]
        else:
            raise ValueError("Invalid Department Code")

    def all(self) -> dict:
        return self.department_list.get(self.department_code)

    def short(self) -> str:
        return self.department_list.get(self.department_code).get("short")

    def full(self) -> str:
        return self.department_list.get(self.department_code).get("full")

    def additional(self) -> str:
        return self.department_list.get(self.department_code).get("additional")

    def __str__(self):
        return self.full()
