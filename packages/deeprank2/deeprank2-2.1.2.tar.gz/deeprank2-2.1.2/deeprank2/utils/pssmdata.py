from typing import Dict, List, Optional

from deeprank2.molstruct.aminoacid import AminoAcid


class PssmRow:
    """Holds data for one position-specific scoring matrix row."""

    def __init__(self, conservations: Dict[AminoAcid, float], information_content: float):
        self._conservations = conservations
        self._information_content = information_content

    @property
    def conservations(self) -> Dict[AminoAcid, float]:
        return self._conservations

    @property
    def information_content(self) -> float:
        return self._information_content

    def get_conservation(self, amino_acid: AminoAcid) -> float:
        return self._conservations[amino_acid]


class PssmTable:
    """Holds data for one position-specific scoring table."""

    def __init__(self, rows: Optional[List[PssmRow]] = None):
        if rows is None:
            self._rows = {}
        else:
            self._rows = rows

    def __contains__(self, residue) -> bool:
        return residue in self._rows

    def __getitem__(self, residue) -> PssmRow:
        return self._rows[residue]

    def update(self, other):
        """Can be used to merge two non-overlapping scoring tables."""

        self._rows.update(other._rows) # pylint: disable=protected-access
