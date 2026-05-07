"""Mock data used when external services are unavailable."""

from __future__ import annotations

CONSTANTS = {
    "default_markets": ["Bhopal", "Indore", "Jabalpur"],
}

MOCK_MANDI_PRICES = {
    "tomato": {"Bhopal": 22.0, "Indore": 18.0, "Jabalpur": 20.0},
    "onion": {"Bhopal": 30.0, "Indore": 28.0, "Jabalpur": 27.0},
    "potato": {"Bhopal": 24.0, "Indore": 21.0, "Jabalpur": 23.0},
    "wheat": {"Bhopal": 26.0, "Indore": 25.0, "Jabalpur": 24.0},
    "rice": {"Bhopal": 34.0, "Indore": 33.0, "Jabalpur": 32.0},
}
