import pandas as pd
import pytest

from src.mapper import map_defects_to_requirements


def test_defects_are_mapped_to_requirements():
    requirements = pd.DataFrame(
        {
            "requirement_id": ["R001", "R002"],
            "description": [
                "User can log in",
                "System rejects invalid credentials",
            ],
            "priority": ["High", "High"],
        }
    )

    escaped_defects = pd.DataFrame(
        {
            "defect_id": ["D001"],
            "requirement_id": ["R002"],
            "description": ["Invalid credentials are accepted"],
            "severity": ["High"],
            "escape_phase": ["System Testing"],
        }
    )

    result = map_defects_to_requirements(
        requirements,
        escaped_defects,
    )

    assert len(result) == 1
    assert result.loc[0, "defect_id"] == "D001"
    assert result.loc[0, "requirement_id"] == "R002"
    assert (
        result.loc[0, "requirement_description"]
        == "System rejects invalid credentials"
    )


def test_unknown_requirement_id_raises_error():
    requirements = pd.DataFrame(
        {
            "requirement_id": ["R001"],
            "description": ["User can log in"],
            "priority": ["High"],
        }
    )

    escaped_defects = pd.DataFrame(
        {
            "defect_id": ["D001"],
            "requirement_id": ["R999"],
            "description": ["Unknown requirement defect"],
            "severity": ["High"],
            "escape_phase": ["System Testing"],
        }
    )

    with pytest.raises(ValueError, match="Unknown requirement IDs"):
        map_defects_to_requirements(
            requirements,
            escaped_defects,
        )