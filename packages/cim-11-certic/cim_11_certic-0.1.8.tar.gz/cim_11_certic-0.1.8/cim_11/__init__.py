import sqlite3
import os
from typing import List, Union
from contextlib import contextmanager

_DB_FILE = "{}/cim-11.sqlite3".format(os.path.dirname(__file__))


@contextmanager
def _db_cursor():
    db = sqlite3.connect(f"file:{_DB_FILE}?mode=ro", uri=True)
    cursor = db.cursor()
    yield cursor
    db.close()


class Concept:
    def __init__(
        self,
        idc_id: str,
        icode: str = None,
        label: str = None,
        parent_idc_id: str = None,
    ):
        self.idc_id = idc_id
        self.icode = icode
        self.label = label
        self.parent_idc_id = parent_idc_id

    @property
    def children(self) -> List["Concept"]:
        items = []
        with _db_cursor() as cursor:
            for row in cursor.execute(
                "SELECT idc_id, icode, label, parent_idc_id from cim11 where parent_idc_id = ?",
                (self.idc_id,),
            ):
                items.append(Concept(row[0], row[1], row[2], row[3]))
        return items

    @property
    def parent(self) -> Union["Concept", None]:
        with _db_cursor() as cursor:
            for row in cursor.execute(
                "SELECT idc_id, icode, label, parent_idc_id from cim11 where idc_id = ?",
                (self.parent_idc_id,),
            ):
                return Concept(row[0], row[1], row[2], row[3])

    def __str__(self):
        if self.icode:
            return f"{self.icode} {self.label}"


def root_concepts() -> List[Concept]:
    """
    Fetches the root concepts from the database.

    :return: A list of Concept objects representing the root concepts.
    """
    items = []
    with _db_cursor() as cursor:
        for row in cursor.execute(
            "SELECT idc_id, icode, label, parent_idc_id from cim11 where parent_idc_id is null"
        ):
            if row[1] not in ["X", "V"]:
                items.append(Concept(row[0], row[1], row[2], row[3]))
        return items


def label_search(terms: str) -> List[Concept]:
    """
    Search for concepts based on given terms.

    :param terms: The terms to search for.
    :return: A list of concepts matching the search terms.
    """
    def fts_escape(user_input: str) -> str:
        wrds = []
        for wrd in user_input.split(" "):
            wrds.append('"' + wrd.replace('"', '""') + '"')
        return " ".join(wrds)

    dedup = []
    terms = fts_escape(terms)
    items = []
    with _db_cursor() as cursor:
        for row in cursor.execute(
            "SELECT idc_id, icode, label, parent_idc_id from cim11 where label match ? and icode is not null order by icode",
            (terms,),
        ):
            if row[1] not in ["X", "V"] and row[1] not in dedup:
                items.append(Concept(row[0], row[1], row[2], row[3]))
                dedup.append(row[1])
    return items


def icode_search(code: str, partial=True) -> List[Concept]:
    """
    Searches for concepts in the database based on the provided code.

    :param code: The code to search for concepts with.
    :param partial: Set to True to search for concepts with codes starting with the provided code. Set to False to search for concepts with exact codes.
    :return: A list of Concept objects that match the search criteria.
    """
    items = []
    dedup = []
    partial_suffix = "%" if partial else ""
    with _db_cursor() as cursor:
        for row in cursor.execute(
            "SELECT idc_id, icode, label, parent_idc_id from cim11 where icode like ? order by icode",
            (f"{code}{partial_suffix}",),
        ):
            if row[1] not in ["X", "V"] and row[1] not in dedup:
                items.append(Concept(row[0], row[1], row[2], row[3]))
                dedup.append(row[1])
    return items


def icode_details(complete_code: str) -> Union[Concept, None]:
    """
    Retrieve the details of a concept using its complete code.

    :param complete_code: The complete code of the concept.
    :return: The Concept object corresponding to the complete code, or None if not found.
    """
    with _db_cursor() as cursor:
        for row in cursor.execute(
            "SELECT idc_id, icode, label, parent_idc_id from cim11 where icode = ?",
            (complete_code,),
        ):
            return Concept(row[0], row[1], row[2], row[3])
