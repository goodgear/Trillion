"""
Transcript Converter for ARMAC
--------------------------------
Parses trading transcripts (e.g., Chris Kmer's price‑action breakdown)
and converts them into structured JSON for calibration and engine testing.
"""

import json
import re
from pathlib import Path

def extract_sections(text):
    """
    Extracts the three key framework components:
    Direction, Confirmation, and Invalidation.
    """
    sections = {
        "direction": None,
        "confirmation": None,
        "invalidation": None
    }

    # Direction: look for trend, higher highs/lows, break of structure
    direction_pattern = r"(higher high|higher low|break of structure|trend line)"
    direction_match = re.findall(direction_pattern, text, re.IGNORECASE)
    if direction_match:
        sections["direction"] = {
            "pattern": list(set(direction_match)),
            "signal": "break_of_structure",
            "description": "Trend identification using higher highs/lows and break of structure."
        }

    # Confirmation: fair value gaps, validation, response areas
    confirm_pattern = r"(fair value gap|confirmation|validate|response)"
    confirm_match = re.findall(confirm_pattern, text, re.IGNORECASE)
    if confirm_match:
        sections["confirmation"] = {
            "pattern": list(set(confirm_match)),
            "signal": "trend_continuation",
            "description": "Confirmation using fair value gaps and validated response levels."
        }

    # Invalidation: change of character, break and retest, reversal
    invalid_pattern = r"(change of character|break and retest|reversal|trend falling apart)"
    invalid_match = re.findall(invalid_pattern, text, re.IGNORECASE)
    if invalid_match:
        sections["invalidation"] = {
            "pattern": list(set(invalid_match)),
            "signal": "trend_reversal",
            "description": "Invalidation when trend fails and change of character occurs."
        }

    return sections


def convert_transcript_to_json(transcript_path, output_path):
    """
    Reads transcript text, extracts trading logic, and saves structured JSON.
    """
    text = Path(transcript_path).read_text(encoding="utf-8")
    structured_data = extract_sections(text)

    output = {
        "source": Path(transcript_path).name,
        "framework": structured_data,
        "metadata": {
            "author": "Chris Kmer",
            "concepts": ["Direction", "Confirmation", "Invalidation"],
            "version": "1.0"
        }
    }

    Path(output_path).write_text(json.dumps(output, indent=4))
    print(f"Transcript conversion complete → {output_path}")


if __name__ == "__main__":
    # Example usage
    transcript_file = "Once You Master Price Action, Trading Becomes Ridi.txt"
    output_file = "transcript_logic.json"
    convert_transcript_to_json(transcript_file, output_file)
