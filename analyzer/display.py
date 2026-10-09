"""Helpers that turn analysis results into things a GUI can show (no tkinter in here)."""

RATING_COLORS = {
    "Weak": "#d9534f",
    "Medium": "#f0ad4e",
    "Strong": "#3a9ad9",
    "Very Strong": "#2e9e4f",
}
DEFAULT_COLOR = "#999999"


def color_for_rating(rating):
    """Color used for a rating label and score bar (grey for unknown ratings)."""
    return RATING_COLORS.get(rating, DEFAULT_COLOR)


def headline(report):
    """Short summary shown above the score bar, e.g. 'Medium - 57/100'."""
    return f"{report['rating']} - {report['score']}/100"


def bar_fraction(score):
    """Convert a 0-100 score into a 0.0-1.0 fraction, clamped to that range."""
    return max(0, min(100, score)) / 100
