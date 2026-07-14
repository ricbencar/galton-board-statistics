#!/usr/bin/env python3
r"""
GALTON BOARD SIMULATOR
======================

Purpose
-------
This program presents an animated Galton board, also called a quincunx or
bean machine. Balls pass through a triangular lattice of pegs and are directed
left or right at every row. The final receiving-bin histogram illustrates how
many independent random decisions generate a predictable probability
distribution.

The program deliberately separates:

1. the probability model, which is exact; and
2. the animation, which is a smooth visual representation of that model.

The visual bounce amplitude, fall speed, trails, highlights, collision rings,
and spark particles do not alter the probability assigned to a ball.

Mathematical model
------------------
Let the board have n peg rows. At row i, define the Bernoulli random variable

    X_i = 1  if the ball moves right,
    X_i = 0  if the ball moves left.

The decisions are independent, with

    P(X_i = 1) = p,
    P(X_i = 0) = 1 - p.

The final receiving-bin index K is the number of right movements:

    K = X_1 + X_2 + ... + X_n.

Therefore,

    K ~ Binomial(n, p),

and the exact probability of reaching bin k is

    P(K = k) = C(n, k) p^k (1 - p)^(n-k),

where

    C(n, k) = n! / [k! (n-k)!]

is the binomial coefficient.

The theoretical mean, variance, and standard deviation are

    E[K]   = n p,
    Var[K] = n p (1 - p),
    sigma  = sqrt(n p (1 - p)).

For a symmetric board, p = 0.5. In that case the coefficients C(n, k) form
row n of Pascal's triangle, and their sum is

    sum C(n, k) = 2^n.

As n increases, the binomial distribution approaches a normal distribution
under the usual normal-approximation conditions. The board therefore provides
a visual demonstration of repeated Bernoulli trials, Pascal's triangle, the
binomial theorem, and the emergence of the familiar bell-shaped curve.

Important implementation detail
-------------------------------
A ball's complete left/right sequence is generated once, when the ball is
released. Its final bin is therefore known from the exact Bernoulli sequence.
The animation subsequently moves the ball through smooth path segments.

The program also stores the theoretical contribution associated with every
settled ball. Consequently, if the user changes p during a run, the displayed
reference curve remains the correct accumulated expectation for the actual
sequence of configured probabilities rather than incorrectly applying only
the latest p value to all previous balls.

Runtime requirements
--------------------
* Python 3.10 or newer is recommended.
* Tkinter/Tk 8.6 is required for the graphical interface.
* No third-party Python package is required to run the script.
* The standard Windows installer from python.org normally includes Tkinter.

Verify Tkinter independently with:

    python -m tkinter

A small Tk test window should open. If it does not, repair or reinstall Python
with the optional Tcl/Tk and IDLE component enabled.

Direct execution
----------------
From Command Prompt in the script directory:

    python script.py

The program opens maximized on Windows. It also contains fallbacks for window
managers that do not support the Windows "zoomed" state.

Keyboard controls
-----------------
    Space       Pause or resume the simulation
    R           Reset balls, effects, counters, and histograms
    N           Release one ball immediately
    B           Queue a burst of 100 balls
    Up          Increase automatic release rate
    Down        Decrease automatic release rate
    H           Show or hide the help overlay
    Esc         Close the program through the controlled shutdown routine

Interface parameters
--------------------
    Release rate       Automatic balls released per second
    Fall speed         Animation speed only; probability is unchanged
    Right probability Probability p of moving right at every row
    Bounce amplitude   Visual lateral deflection around a peg
    Ball size          Diameter scale for newly released balls
    Impact intensity   Strength of collision rings and spark effects
    Marble gloss       Strength of highlights on the gray/white balls
    Board lighting     Intensity of frame, peg, and glass highlights
    Colour layout      Select one of five complete interface palettes

Display switches
----------------
    Trails             Show recent motion behind each moving ball
    Impacts            Show collision rings and spark particles
    Glass              Show the subtle protective-glass perimeter
    Marble piles       Draw representative settled balls in the bins
    Theory             Draw the accumulated exact binomial expectation

Colour layouts
--------------
    Scientific Blue    Original blue scientific interface
    Graphite Silver    Neutral dark gray and polished silver
    Emerald Laboratory Dark green technical palette
    Burgundy Copper    Deep burgundy with warm metal accents
    Violet Night       Indigo and violet low-light palette

All layouts retain gray/white balls for consistent path visibility.

Virtual environment and pip
---------------------------
The simulator itself needs no pip installation. A virtual environment is still
recommended when packaging the program, because it isolates the build tools
from the system Python installation.

Windows Command Prompt:

    py -3.10 -m venv .venv
    .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    python -m pip install pyinstaller

Windows PowerShell:

    py -3.10 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    python -m pip install pyinstaller

If PowerShell blocks activation scripts, either use Command Prompt or review
the local execution-policy settings. The virtual environment does not have to
be activated if commands are called through its full Python path.

Packaging as a Windows executable with PyInstaller
--------------------------------------------------
PyInstaller is commonly described as a Python compiler, but technically it
"freezes" the script, Python interpreter, and required libraries into a
distributable application. Build the Windows executable on Windows; PyInstaller
is not a general cross-compiler between operating systems.

Recommended one-folder build
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This form normally starts faster and is easier to diagnose:

    python -m PyInstaller ^
        --noconfirm ^
        --clean ^
        --windowed ^
        --onedir ^
        --name GaltonBoardSimulator ^
        script.py

The distributable application is written to:

    dist\GaltonBoardSimulator\script.exe

Single-file build
~~~~~~~~~~~~~~~~~
This form creates one convenient EXE, but it normally starts more slowly
because bundled files must be extracted at launch:

    python -m PyInstaller ^
        --noconfirm ^
        --clean ^
        --windowed ^
        --onefile ^
        --name script ^
        script.py

The executable is written to:

    dist\script.exe

Because the program uses no external images, configuration files, or data
files, no --add-data option is required. The --windowed option suppresses the
console window for this graphical application.

To rebuild from a clean virtual environment:

    rmdir /s /q build
    rmdir /s /q dist
    del GaltonBoardSimulator.spec
    python -m PyInstaller --noconfirm --clean --windowed --onefile ^
        --name GaltonBoardSimulator script.py

Deactivate the environment after building:

    deactivate

Program architecture
--------------------
* Dataclasses hold moving-ball, impact, spark, and layout state.
* Tk variables connect interface controls to simulation parameters.
* _generate_path() performs the exact Bernoulli experiment.
* _advance_ball() interpolates a ball along the precomputed path.
* _settle_ball() updates observed and accumulated theoretical distributions.
* _tick() is the single Tk animation loop.
* The WM_DELETE_WINDOW handler cancels the queued animation callback before
  destroying Tk, allowing the Windows title-bar X button to close cleanly.
* Drawing routines rebuild the Canvas scene every frame in a fixed layer order.
* Short-lived effects are removed as soon as their lifetime expires.
* Explicit live-ball and total-ball limits prevent unbounded resource use.

Numerical and graphical notes
-----------------------------
* The simulation is stochastic; repeated runs are not expected to produce the
  same individual paths.
* For reproducible demonstrations, call random.seed(<integer>) once during
  initialization before balls are generated.
* The 0.033-second upper bound on frame time prevents one delayed frame from
  causing an excessively large animation jump.
* Smoothstep interpolation, 3 t^2 - 2 t^3, makes path transitions visually
  smooth while preserving the already-selected left/right sequence.
* The displayed marble piles are a normalized graphical representation when
  counts become large; the printed counts and statistical calculations always
  use the complete integer totals.
"""

from __future__ import annotations

import math
import random
import time
import tkinter as tk
from collections import deque
from dataclasses import dataclass, field
from tkinter import ttk
from typing import Deque, Iterable


# ---------------------------------------------------------------------------
# Visual palette
# ---------------------------------------------------------------------------
#
# The constants are grouped semantically by the part of the apparatus they
# colour. Some historical names such as MAHOGANY, FELT, and BRASS remain from
# earlier visual themes; in the current blue design they represent frame,
# board-surface, and metal shades respectively. Keeping the names stable avoids
# unnecessary code churn while the comments document their current role.

# Active palette values. They are initialized to "Scientific Blue" and are
# replaced at runtime when the user selects another colour layout.
WALL_TOP = "#07111f"
WALL_BOTTOM = "#111a30"
WALL_SHADOW = "#020711"

MAHOGANY_DEEP = "#050a12"
MAHOGANY_DARK = "#0b1424"
MAHOGANY_MID = "#142844"
MAHOGANY_LIGHT = "#23486c"
MAHOGANY_HIGHLIGHT = "#58b9e9"

FELT_DEEP = "#071321"
FELT_MID = "#0d2238"
FELT_LIGHT = "#153a58"

BRASS_DARK = "#274963"
BRASS_MID = "#79a8c2"
BRASS_LIGHT = "#d7eef8"
BRASS_GLOW = "#effcff"

PARCHMENT = "#dbe9f3"
CREAM = "#edf7ff"
INK = "#08111c"
MUTED = "#7891aa"

GLASS_EDGE = "#6ea6c1"
GLASS_REFLECTION = "#c9ecfb"

THEORY_RED = "#ffcc66"
THEORY_HIGHLIGHT = "#ffe4a3"
HISTOGRAM_SHADOW = "#08111f"
HISTOGRAM_FILL = "#304f82"

# All five layouts deliberately use the same neutral ball tones. This preserves
# maximum contrast and makes the probability paths easy to compare.
BALL_COLORS = [
    "#2f343b",  # dark graphite
    "#4a515a",  # slate gray
    "#686f78",  # medium gray
    "#8c939c",  # soft silver
    "#b2b9c1",  # light silver
    "#d7dde3",  # pearl white
]

BALL_RIM = "#05090f"
BALL_HIGHLIGHT = "#e6f6ff"
BALL_SHADE = "#02050a"

# Interface colours.
SLIDER_BACKGROUND = "#d9ecff"
SLIDER_TROUGH = "#c6e3ff"
SLIDER_BORDER = "#a9cbed"
SLIDER_LIGHT = "#eef7ff"
SLIDER_DARK = "#8fb8df"

BUTTON_PRIMARY = "#79d6ff"
BUTTON_PRIMARY_ACTIVE = "#a5e6ff"
BUTTON_SECONDARY = "#f2a14a"
BUTTON_SECONDARY_ACTIVE = "#ffc06d"

STATUS_RUNNING = "#12302d"
STATUS_PAUSED = "#37291c"
PANEL_SUBTITLE = "#8da2bf"
PANEL_FOOTER = "#68809f"
SECTION_TEXT = "#efdcc5"

# Secondary rendering colours that previously appeared as isolated literals.
BOARD_SHADOW_1 = "#5b4938"
BOARD_SHADOW_2 = "#6b5845"
BOARD_SHADOW_3 = "#7d6750"
FRAME_OUTLINE = "#02060d"
FRAME_TEXTURE = "#0e2035"
SURFACE_OUTLINE = "#020a12"
SURFACE_TEXTURE = "#1b4c6a"
PEG_SHADOW = "#0d1e17"
PEG_OUTLINE = "#172d3d"
PEG_RIM = "#31546b"
PLATE_OUTLINE = "#19374b"
PLATE_TEXT = "#08141f"


# Five complete visual layouts. Keys correspond directly to the active palette
# globals above, allowing the rendering code to remain simple and fast.
COLOUR_LAYOUTS: dict[str, dict[str, str]] = {
    "Scientific Blue": {
        "WALL_TOP": "#07111f",
        "WALL_BOTTOM": "#111a30",
        "WALL_SHADOW": "#020711",
        "MAHOGANY_DEEP": "#050a12",
        "MAHOGANY_DARK": "#0b1424",
        "MAHOGANY_MID": "#142844",
        "MAHOGANY_LIGHT": "#23486c",
        "MAHOGANY_HIGHLIGHT": "#58b9e9",
        "FELT_DEEP": "#071321",
        "FELT_MID": "#0d2238",
        "FELT_LIGHT": "#153a58",
        "BRASS_DARK": "#274963",
        "BRASS_MID": "#79a8c2",
        "BRASS_LIGHT": "#d7eef8",
        "BRASS_GLOW": "#effcff",
        "PARCHMENT": "#dbe9f3",
        "CREAM": "#edf7ff",
        "INK": "#08111c",
        "MUTED": "#7891aa",
        "GLASS_EDGE": "#6ea6c1",
        "GLASS_REFLECTION": "#c9ecfb",
        "THEORY_RED": "#ffcc66",
        "THEORY_HIGHLIGHT": "#ffe4a3",
        "HISTOGRAM_SHADOW": "#08111f",
        "HISTOGRAM_FILL": "#304f82",
        "BALL_RIM": "#05090f",
        "BALL_HIGHLIGHT": "#e6f6ff",
        "BALL_SHADE": "#02050a",
        "SLIDER_BACKGROUND": "#d9ecff",
        "SLIDER_TROUGH": "#c6e3ff",
        "SLIDER_BORDER": "#a9cbed",
        "SLIDER_LIGHT": "#eef7ff",
        "SLIDER_DARK": "#8fb8df",
        "BUTTON_PRIMARY": "#79d6ff",
        "BUTTON_PRIMARY_ACTIVE": "#a5e6ff",
        "BUTTON_SECONDARY": "#f2a14a",
        "BUTTON_SECONDARY_ACTIVE": "#ffc06d",
        "STATUS_RUNNING": "#12302d",
        "STATUS_PAUSED": "#37291c",
        "PANEL_SUBTITLE": "#8da2bf",
        "PANEL_FOOTER": "#68809f",
        "SECTION_TEXT": "#efdcc5",
        "BOARD_SHADOW_1": "#07101d",
        "BOARD_SHADOW_2": "#0a1829",
        "BOARD_SHADOW_3": "#10243a",
        "FRAME_OUTLINE": "#02060d",
        "FRAME_TEXTURE": "#0e2035",
        "SURFACE_OUTLINE": "#020a12",
        "SURFACE_TEXTURE": "#1b4c6a",
        "PEG_SHADOW": "#020a12",
        "PEG_OUTLINE": "#172d3d",
        "PEG_RIM": "#31546b",
        "PLATE_OUTLINE": "#19374b",
        "PLATE_TEXT": "#08141f",
    },
    "Graphite Silver": {
        "WALL_TOP": "#101419",
        "WALL_BOTTOM": "#252d35",
        "WALL_SHADOW": "#05070a",
        "MAHOGANY_DEEP": "#080a0d",
        "MAHOGANY_DARK": "#12161b",
        "MAHOGANY_MID": "#252c34",
        "MAHOGANY_LIGHT": "#3b4651",
        "MAHOGANY_HIGHLIGHT": "#a8c1d2",
        "FELT_DEEP": "#0d1318",
        "FELT_MID": "#17232b",
        "FELT_LIGHT": "#223540",
        "BRASS_DARK": "#46515c",
        "BRASS_MID": "#9ba9b5",
        "BRASS_LIGHT": "#e8eef2",
        "BRASS_GLOW": "#ffffff",
        "PARCHMENT": "#e8edf1",
        "CREAM": "#f4f7f9",
        "INK": "#11161b",
        "MUTED": "#9aa8b4",
        "GLASS_EDGE": "#8aa7b5",
        "GLASS_REFLECTION": "#dcecf2",
        "THEORY_RED": "#65d8ff",
        "THEORY_HIGHLIGHT": "#b8efff",
        "HISTOGRAM_SHADOW": "#0b1015",
        "HISTOGRAM_FILL": "#5c7387",
        "BALL_RIM": "#080a0c",
        "BALL_HIGHLIGHT": "#ffffff",
        "BALL_SHADE": "#080a0d",
        "SLIDER_BACKGROUND": "#e5edf3",
        "SLIDER_TROUGH": "#d0dde6",
        "SLIDER_BORDER": "#aabac6",
        "SLIDER_LIGHT": "#ffffff",
        "SLIDER_DARK": "#8193a1",
        "BUTTON_PRIMARY": "#dcecf6",
        "BUTTON_PRIMARY_ACTIVE": "#ffffff",
        "BUTTON_SECONDARY": "#f0ad4e",
        "BUTTON_SECONDARY_ACTIVE": "#ffc56f",
        "STATUS_RUNNING": "#234737",
        "STATUS_PAUSED": "#55452f",
        "PANEL_SUBTITLE": "#a5b2bd",
        "PANEL_FOOTER": "#7f8c97",
        "SECTION_TEXT": "#edf2f5",
        "BOARD_SHADOW_1": "#090c10",
        "BOARD_SHADOW_2": "#11171d",
        "BOARD_SHADOW_3": "#19222a",
        "FRAME_OUTLINE": "#030405",
        "FRAME_TEXTURE": "#28343e",
        "SURFACE_OUTLINE": "#06090c",
        "SURFACE_TEXTURE": "#314959",
        "PEG_SHADOW": "#05090b",
        "PEG_OUTLINE": "#4f5b65",
        "PEG_RIM": "#60717e",
        "PLATE_OUTLINE": "#4f5b65",
        "PLATE_TEXT": "#11161b",
    },
    "Emerald Laboratory": {
        "WALL_TOP": "#061410",
        "WALL_BOTTOM": "#0d2b23",
        "WALL_SHADOW": "#020906",
        "MAHOGANY_DEEP": "#03110d",
        "MAHOGANY_DARK": "#072119",
        "MAHOGANY_MID": "#0d3d2d",
        "MAHOGANY_LIGHT": "#176047",
        "MAHOGANY_HIGHLIGHT": "#65d7ad",
        "FELT_DEEP": "#041a13",
        "FELT_MID": "#0a3024",
        "FELT_LIGHT": "#11513c",
        "BRASS_DARK": "#2c5d4a",
        "BRASS_MID": "#7ac6a7",
        "BRASS_LIGHT": "#dcfff0",
        "BRASS_GLOW": "#f4fff9",
        "PARCHMENT": "#ddf2e8",
        "CREAM": "#effff7",
        "INK": "#071a12",
        "MUTED": "#79a996",
        "GLASS_EDGE": "#6fb59b",
        "GLASS_REFLECTION": "#d6f5e9",
        "THEORY_RED": "#ffd166",
        "THEORY_HIGHLIGHT": "#ffe7a6",
        "HISTOGRAM_SHADOW": "#04120d",
        "HISTOGRAM_FILL": "#24745a",
        "BALL_RIM": "#030907",
        "BALL_HIGHLIGHT": "#f5fffb",
        "BALL_SHADE": "#020805",
        "SLIDER_BACKGROUND": "#d9f4e8",
        "SLIDER_TROUGH": "#bfe8d6",
        "SLIDER_BORDER": "#8dc8ad",
        "SLIDER_LIGHT": "#effff7",
        "SLIDER_DARK": "#66a88b",
        "BUTTON_PRIMARY": "#67e0b4",
        "BUTTON_PRIMARY_ACTIVE": "#a3f2d5",
        "BUTTON_SECONDARY": "#f2b24f",
        "BUTTON_SECONDARY_ACTIVE": "#ffd27e",
        "STATUS_RUNNING": "#1a573d",
        "STATUS_PAUSED": "#55452d",
        "PANEL_SUBTITLE": "#86b9a4",
        "PANEL_FOOTER": "#64917d",
        "SECTION_TEXT": "#e5fff3",
        "BOARD_SHADOW_1": "#03100c",
        "BOARD_SHADOW_2": "#061a14",
        "BOARD_SHADOW_3": "#0a281e",
        "FRAME_OUTLINE": "#010704",
        "FRAME_TEXTURE": "#0b3226",
        "SURFACE_OUTLINE": "#020b08",
        "SURFACE_TEXTURE": "#1e684f",
        "PEG_SHADOW": "#02100b",
        "PEG_OUTLINE": "#285a46",
        "PEG_RIM": "#3f8065",
        "PLATE_OUTLINE": "#285a46",
        "PLATE_TEXT": "#071a12",
    },
    "Burgundy Copper": {
        "WALL_TOP": "#19080f",
        "WALL_BOTTOM": "#32111e",
        "WALL_SHADOW": "#080207",
        "MAHOGANY_DEEP": "#14050a",
        "MAHOGANY_DARK": "#270a12",
        "MAHOGANY_MID": "#4b1423",
        "MAHOGANY_LIGHT": "#74263a",
        "MAHOGANY_HIGHLIGHT": "#e17d99",
        "FELT_DEEP": "#1d0911",
        "FELT_MID": "#3a1020",
        "FELT_LIGHT": "#5e1c31",
        "BRASS_DARK": "#6a3544",
        "BRASS_MID": "#c58a9c",
        "BRASS_LIGHT": "#f7dce4",
        "BRASS_GLOW": "#fff6f8",
        "PARCHMENT": "#f3e3e7",
        "CREAM": "#fff5f7",
        "INK": "#260b12",
        "MUTED": "#b98795",
        "GLASS_EDGE": "#b77f92",
        "GLASS_REFLECTION": "#f6dce5",
        "THEORY_RED": "#ffd166",
        "THEORY_HIGHLIGHT": "#ffe8ad",
        "HISTOGRAM_SHADOW": "#1a0810",
        "HISTOGRAM_FILL": "#7e3049",
        "BALL_RIM": "#0b0407",
        "BALL_HIGHLIGHT": "#fff9fa",
        "BALL_SHADE": "#080205",
        "SLIDER_BACKGROUND": "#f6dfe6",
        "SLIDER_TROUGH": "#edc4d0",
        "SLIDER_BORDER": "#d19aad",
        "SLIDER_LIGHT": "#fff5f8",
        "SLIDER_DARK": "#b56d83",
        "BUTTON_PRIMARY": "#f29ab2",
        "BUTTON_PRIMARY_ACTIVE": "#ffc1d0",
        "BUTTON_SECONDARY": "#e9a34c",
        "BUTTON_SECONDARY_ACTIVE": "#ffc570",
        "STATUS_RUNNING": "#36533b",
        "STATUS_PAUSED": "#63382d",
        "PANEL_SUBTITLE": "#c095a2",
        "PANEL_FOOTER": "#9d6d7d",
        "SECTION_TEXT": "#ffe8ee",
        "BOARD_SHADOW_1": "#110308",
        "BOARD_SHADOW_2": "#1d0710",
        "BOARD_SHADOW_3": "#2a0c18",
        "FRAME_OUTLINE": "#080104",
        "FRAME_TEXTURE": "#43101f",
        "SURFACE_OUTLINE": "#0d0207",
        "SURFACE_TEXTURE": "#75243c",
        "PEG_SHADOW": "#12040a",
        "PEG_OUTLINE": "#6c3445",
        "PEG_RIM": "#97566a",
        "PLATE_OUTLINE": "#6c3445",
        "PLATE_TEXT": "#260b12",
    },
    "Violet Night": {
        "WALL_TOP": "#0e0920",
        "WALL_BOTTOM": "#21143c",
        "WALL_SHADOW": "#04020a",
        "MAHOGANY_DEEP": "#080513",
        "MAHOGANY_DARK": "#160d29",
        "MAHOGANY_MID": "#2d1b50",
        "MAHOGANY_LIGHT": "#493174",
        "MAHOGANY_HIGHLIGHT": "#a985f0",
        "FELT_DEEP": "#0c081b",
        "FELT_MID": "#1d1236",
        "FELT_LIGHT": "#332058",
        "BRASS_DARK": "#4c3b6e",
        "BRASS_MID": "#a894cf",
        "BRASS_LIGHT": "#eee8ff",
        "BRASS_GLOW": "#ffffff",
        "PARCHMENT": "#ece7f8",
        "CREAM": "#f8f5ff",
        "INK": "#171023",
        "MUTED": "#998ab7",
        "GLASS_EDGE": "#8875ad",
        "GLASS_REFLECTION": "#e6ddff",
        "THEORY_RED": "#64e8ff",
        "THEORY_HIGHLIGHT": "#b8f5ff",
        "HISTOGRAM_SHADOW": "#0d0a1a",
        "HISTOGRAM_FILL": "#5c4690",
        "BALL_RIM": "#06040b",
        "BALL_HIGHLIGHT": "#ffffff",
        "BALL_SHADE": "#040207",
        "SLIDER_BACKGROUND": "#e9e0ff",
        "SLIDER_TROUGH": "#d6c5fa",
        "SLIDER_BORDER": "#b29bdc",
        "SLIDER_LIGHT": "#f8f4ff",
        "SLIDER_DARK": "#8d72bd",
        "BUTTON_PRIMARY": "#8de9ff",
        "BUTTON_PRIMARY_ACTIVE": "#c0f4ff",
        "BUTTON_SECONDARY": "#f1aa4d",
        "BUTTON_SECONDARY_ACTIVE": "#ffc672",
        "STATUS_RUNNING": "#294c42",
        "STATUS_PAUSED": "#54402f",
        "PANEL_SUBTITLE": "#aa99c9",
        "PANEL_FOOTER": "#8171a3",
        "SECTION_TEXT": "#f1ebff",
        "BOARD_SHADOW_1": "#07040f",
        "BOARD_SHADOW_2": "#100920",
        "BOARD_SHADOW_3": "#1a1030",
        "FRAME_OUTLINE": "#030107",
        "FRAME_TEXTURE": "#281942",
        "SURFACE_OUTLINE": "#05030b",
        "SURFACE_TEXTURE": "#4b3277",
        "PEG_SHADOW": "#07040f",
        "PEG_OUTLINE": "#493766",
        "PEG_RIM": "#6e5a91",
        "PLATE_OUTLINE": "#493766",
        "PLATE_TEXT": "#171023",
    },
}

COLOUR_LAYOUT_NAMES = tuple(COLOUR_LAYOUTS)


def activate_colour_layout(name: str) -> None:
    """Activate one named palette by updating the module's semantic colours.

    The drawing routines read the palette globals at render time. Updating them
    and rebuilding the Tk controls is therefore sufficient to change the entire
    interface without resetting the probability experiment.
    """
    palette = COLOUR_LAYOUTS.get(name)
    if palette is None:
        raise ValueError(f"Unknown colour layout: {name!r}")

    module_globals = globals()
    for colour_name, colour_value in palette.items():
        module_globals[colour_name] = colour_value



# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ImpactEffect:
    """State of one short-lived collision-ring animation.

    The ring starts at the peg contact point, expands with age, and fades when
    ``age`` reaches ``duration``. ``strength`` scales its size and line width.
    """

    x: float
    y: float
    color: str
    strength: float
    age: float = 0.0
    duration: float = 0.34


@dataclass
class Spark:
    """State of one small particle emitted by a visual peg collision.

    Sparks are purely decorative. Their position is integrated with a simple
    downward acceleration until ``age`` reaches the assigned lifetime.
    """

    x: float
    y: float
    vx: float
    vy: float
    life: float
    size: float
    age: float = 0.0


@dataclass
class Ball:
    """Complete probability and animation state for one moving ball.

    ``path`` is created from an exact sequence of Bernoulli decisions.
    ``impact_indices`` identifies path nodes at which collision effects should
    be emitted. ``segment`` and ``progress`` locate the ball within that path.
    """

    path: list[tuple[float, float]]
    impact_indices: set[int]
    bin_index: int
    right_probability: float
    radius: float
    color: str
    base_speed: float

    segment: int = 0
    progress: float = 0.0
    x: float = 0.0
    y: float = 0.0
    settled: bool = False
    rotation_phase: float = 0.0

    trail: Deque[tuple[float, float]] = field(
        default_factory=lambda: deque(maxlen=14)
    )

    def __post_init__(self) -> None:
        """
        Set the initial displayed position from the first path node.

        Dataclasses call this hook after all generated ``__init__`` assignments.
        """
        if self.path:
            self.x, self.y = self.path[0]


@dataclass(frozen=True)
class Layout:
    """Immutable geometric description of the current responsive board.

    A new instance is calculated from the actual Canvas dimensions. Drawing and
    animation routines receive the same instance during one frame, preventing
    inconsistencies if the window is resized between frames.
    """

    width: float
    height: float
    center_x: float

    board_left: float
    board_right: float
    board_top: float
    board_bottom: float

    inner_left: float
    inner_right: float
    inner_top: float
    inner_bottom: float

    funnel_y: float
    first_peg_y: float
    peg_dx: float
    peg_dy: float
    peg_radius: float
    nominal_ball_radius: float

    bin_left: float
    bin_right: float
    bin_top: float
    bin_bottom: float
    bin_width: float
    bins: int


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

class GaltonBoardApp:
    """Own the Tk interface, stochastic model, animation state, and rendering.

    The application uses one Tk ``after`` loop. It does not create worker
    threads, so every interface update and Canvas operation remains on Tk's
    required main thread.
    """

    # Number of independent Bernoulli decisions made by every ball.
    ROWS = 12
    TARGET_FPS = 60
    MAX_LIVE_BALLS = 420
    MAX_TOTAL_BALLS = 50_000

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the responsive GUI, model parameters, counters, and animation state.

        No balls are generated here. The first scheduled ``_tick`` starts after Tk has
        completed initial widget layout, allowing the Canvas to report useful dimensions.
        """
        self.root = root

        # The selected colour layout is independent of all model parameters and
        # remains unchanged when the experiment is reset.
        self.colour_layout = tk.StringVar(value="Scientific Blue")
        activate_colour_layout(self.colour_layout.get())

        self.root.title("Galton Board Simulator")
        self.root.geometry("1400x900")
        self.root.minsize(1100, 740)
        self.root.configure(bg=MAHOGANY_DEEP)

        # A board with n rows has n + 1 possible final right-move counts,
        # hence n + 1 receiving bins numbered from 0 through n.
        self.rows = self.ROWS
        self.bins = self.rows + 1

        # High-level application state controlled by buttons and keyboard.
        self.running = True
        self.show_help = False

        # Simulation parameters.
        self.release_rate = tk.DoubleVar(value=14.0)
        self.fall_speed = tk.DoubleVar(value=0.72)
        self.right_probability = tk.DoubleVar(value=0.50)
        self.bounce_amplitude = tk.DoubleVar(value=0.90)
        self.ball_scale = tk.DoubleVar(value=1.00)
        self.effect_intensity = tk.DoubleVar(value=0.82)

        # Aesthetic parameters.
        self.marble_gloss = tk.DoubleVar(value=0.88)
        self.board_lighting = tk.DoubleVar(value=0.84)

        self.trails_enabled = tk.BooleanVar(value=True)
        self.effects_enabled = tk.BooleanVar(value=True)
        self.theory_enabled = tk.BooleanVar(value=True)
        self.piles_enabled = tk.BooleanVar(value=True)
        self.glass_enabled = tk.BooleanVar(value=True)

        # Dynamic objects currently visible in the animated scene.
        self.balls: list[Ball] = []
        self.impacts: list[ImpactEffect] = []
        self.sparks: list[Spark] = []

        # Observed integer counts and accumulated theoretical expectations.
        # expected_counts is updated with the probability vector associated
        # with each settled ball, so changing p midway does not invalidate it.
        self.bin_counts = [0 for _ in range(self.bins)]
        self.expected_counts = [0.0 for _ in range(self.bins)]

        # Counters and fractional scheduling state. spawn_accumulator
        # preserves sub-ball timing between frames; burst_queue spreads a large
        # request over multiple frames to avoid a visible frame-time spike.
        self.total_released = 0
        self.total_settled = 0
        self.spawn_accumulator = 0.0
        self.burst_queue = 0

        self.last_time = time.perf_counter()
        self.smoothed_fps = float(self.TARGET_FPS)

        # Tk ``after`` callbacks must be cancelled explicitly during shutdown.
        # Without this state, the 60 FPS callback can remain queued while the
        # window is being destroyed, which may make the Windows close button
        # appear to freeze or can produce Tcl errors after destruction.
        self._closing = False
        self._after_id: str | None = None

        self._build_ui()
        self._bind_events()

        # Route the title-bar X button through the same controlled shutdown
        # routine used by the Escape key.
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        # Keep the callback identifier so it can be cancelled before Tk widgets
        # and Tcl commands are destroyed.
        self._after_id = self.root.after(80, self._tick)

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """
        Construct the Canvas, control panel, sliders, switches, buttons, and statistics.

        The standard ``TScale`` and ``TCheckbutton`` style names are intentionally used
        for compatibility with older Tk 8.6 installations on Windows.
        """
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=0)

        self.canvas = tk.Canvas(
            self.root,
            bg=WALL_TOP,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        panel = tk.Frame(self.root, width=320, bg=MAHOGANY_DEEP)
        panel.grid(row=0, column=1, sticky="ns")
        panel.grid_propagate(False)

        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Built-in style names are deliberately used for Windows/Tk compatibility.
        style.configure(
            "TScale",
            background=SLIDER_BACKGROUND,
            troughcolor=SLIDER_TROUGH,
            bordercolor=SLIDER_BORDER,
            lightcolor=SLIDER_LIGHT,
            darkcolor=SLIDER_DARK,
        )
        style.configure(
            "TCheckbutton",
            background=MAHOGANY_DARK,
            foreground=CREAM,
            font=("Segoe UI", 8),
        )
        style.map(
            "TCheckbutton",
            background=[("active", MAHOGANY_DARK)],
            foreground=[("active", CREAM)],
        )

        tk.Label(
            panel,
            text="GALTON BOARD",
            anchor="w",
            bg=MAHOGANY_DEEP,
            fg=CREAM,
            font=("Georgia", 24, "bold"),
        ).pack(fill="x", padx=22, pady=(18, 1))

        tk.Label(
            panel,
            text="Bernoulli-process and binomial-distribution simulator",
            anchor="w",
            bg=MAHOGANY_DEEP,
            fg=PANEL_SUBTITLE,
            font=("Segoe UI", 9),
        ).pack(fill="x", padx=22, pady=(0, 9))

        self.status_label = tk.Label(
            panel,
            text="RUNNING",
            bg=STATUS_RUNNING,
            fg=CREAM,
            padx=11,
            pady=4,
            font=("Segoe UI", 8, "bold"),
        )
        self.status_label.pack(anchor="w", padx=22, pady=(0, 8))

        simulation = self._card(panel)
        self._section_title(simulation, "SIMULATION").pack(anchor="w")

        first_row = tk.Frame(simulation, bg=MAHOGANY_DARK)
        first_row.pack(fill="x", pady=(6, 3))

        self.pause_button = self._button(
            first_row,
            "Pause",
            self.toggle_pause,
            accent=True,
        )
        self.pause_button.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self._button(first_row, "Reset", self.reset).pack(
            side="left", fill="x", expand=True, padx=(4, 0)
        )

        second_row = tk.Frame(simulation, bg=MAHOGANY_DARK)
        second_row.pack(fill="x", pady=(2, 4))

        self._button(second_row, "+1 ball", self.release_one).pack(
            side="left", fill="x", expand=True, padx=(0, 4)
        )
        self._button(second_row, "+100", self.release_burst).pack(
            side="left", fill="x", expand=True, padx=(4, 0)
        )

        self._slider(
            simulation,
            "Release rate",
            self.release_rate,
            1.0,
            65.0,
            lambda value: f"{float(value):.0f}/s",
        )
        self._slider(
            simulation,
            "Fall speed",
            self.fall_speed,
            0.35,
            1.20,
            lambda value: f"{float(value):.2f}×",
        )
        self._slider(
            simulation,
            "Right probability",
            self.right_probability,
            0.25,
            0.75,
            lambda value: f"{float(value):.3f}",
        )
        self._slider(
            simulation,
            "Bounce amplitude",
            self.bounce_amplitude,
            0.45,
            1.35,
            lambda value: f"{float(value):.2f}×",
        )
        self._slider(
            simulation,
            "Ball size",
            self.ball_scale,
            0.72,
            1.32,
            lambda value: f"{float(value):.2f}×",
        )
        self._slider(
            simulation,
            "Impact intensity",
            self.effect_intensity,
            0.0,
            1.25,
            lambda value: f"{float(value):.2f}",
        )

        appearance = self._card(panel)
        self._section_title(appearance, "APPEARANCE").pack(anchor="w")

        theme_row = tk.Frame(appearance, bg=MAHOGANY_DARK)
        theme_row.pack(fill="x", pady=(6, 3))

        tk.Label(
            theme_row,
            text="Colour layout",
            bg=MAHOGANY_DARK,
            fg=CREAM,
            font=("Segoe UI", 8),
        ).pack(side="left")

        theme_menu = tk.OptionMenu(
            theme_row,
            self.colour_layout,
            *COLOUR_LAYOUT_NAMES,
            command=self.change_colour_layout,
        )
        theme_menu.configure(
            bg=SLIDER_BACKGROUND,
            activebackground=SLIDER_LIGHT,
            fg=INK,
            activeforeground=INK,
            highlightthickness=1,
            highlightbackground=SLIDER_BORDER,
            bd=0,
            relief="flat",
            font=("Segoe UI", 8, "bold"),
            padx=5,
            pady=2,
            cursor="hand2",
        )
        theme_menu["menu"].configure(
            bg=SLIDER_BACKGROUND,
            activebackground=SLIDER_TROUGH,
            fg=INK,
            activeforeground=INK,
            font=("Segoe UI", 8),
        )
        theme_menu.pack(side="right", fill="x", expand=True, padx=(10, 0))

        self._slider(
            appearance,
            "Marble gloss",
            self.marble_gloss,
            0.20,
            1.00,
            lambda value: f"{float(value):.2f}",
        )
        self._slider(
            appearance,
            "Board lighting",
            self.board_lighting,
            0.25,
            1.00,
            lambda value: f"{float(value):.2f}",
        )

        checks = tk.Frame(appearance, bg=MAHOGANY_DARK)
        checks.pack(fill="x", pady=(5, 0))

        ttk.Checkbutton(
            checks,
            text="Trails",
            variable=self.trails_enabled,
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))

        ttk.Checkbutton(
            checks,
            text="Impacts",
            variable=self.effects_enabled,
        ).grid(row=0, column=1, sticky="w", padx=(0, 10))

        ttk.Checkbutton(
            checks,
            text="Glass",
            variable=self.glass_enabled,
        ).grid(row=0, column=2, sticky="w")

        checks2 = tk.Frame(appearance, bg=MAHOGANY_DARK)
        checks2.pack(fill="x", pady=(2, 0))

        ttk.Checkbutton(
            checks2,
            text="Marble piles",
            variable=self.piles_enabled,
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))

        ttk.Checkbutton(
            checks2,
            text="Theory",
            variable=self.theory_enabled,
        ).grid(row=0, column=1, sticky="w")

        statistics = self._card(panel)
        self._section_title(statistics, "LIVE STATISTICS").pack(anchor="w")

        self.stats_label = tk.Label(
            statistics,
            text="",
            justify="left",
            anchor="nw",
            bg=MAHOGANY_DARK,
            fg=CREAM,
            font=("Consolas", 8),
            pady=4,
        )
        self.stats_label.pack(fill="x")

        tk.Label(
            panel,
            text="Space pause   N one   B burst   R reset   H help",
            anchor="w",
            bg=MAHOGANY_DEEP,
            fg=PANEL_FOOTER,
            font=("Consolas", 8),
        ).pack(side="bottom", fill="x", padx=22, pady=13)

    def _card(self, parent: tk.Widget) -> tk.Frame:
        """
        Create and pack one visually grouped control-panel container.

        Returning the frame lets the caller add labels, controls, and statistics while
        centralizing border, padding, and background configuration.
        """
        frame = tk.Frame(
            parent,
            bg=MAHOGANY_DARK,
            highlightthickness=1,
            highlightbackground=MAHOGANY_LIGHT,
            padx=13,
            pady=9,
        )
        frame.pack(fill="x", padx=14, pady=4)
        return frame

    @staticmethod
    def _section_title(parent: tk.Widget, text: str) -> tk.Label:
        """
        Create a small uppercase-style heading for a control-panel section.
        """
        return tk.Label(
            parent,
            text=text,
            bg=MAHOGANY_DARK,
            fg=SECTION_TEXT,
            font=("Segoe UI", 8, "bold"),
        )

    @staticmethod
    def _button(
        parent: tk.Widget,
        text: str,
        command,
        *,
        accent: bool = False,
    ) -> tk.Button:
        """
        Create a consistently styled command button.

        ``accent`` selects the primary action colour; the callback itself is supplied
        by the caller and is executed by Tk on the main event thread.
        """
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=BUTTON_PRIMARY if accent else BUTTON_SECONDARY,
            activebackground=(
                BUTTON_PRIMARY_ACTIVE if accent else BUTTON_SECONDARY_ACTIVE
            ),
            fg=INK,
            activeforeground=INK,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=7,
            pady=6,
            font=("Segoe UI", 8, "bold"),
        )

    def _slider(
        self,
        parent: tk.Widget,
        label: str,
        variable: tk.DoubleVar,
        low: float,
        high: float,
        formatter,
    ) -> None:
        """
        Add a labelled Tk scale and a live formatted value readout.

        The Tk variable is the authoritative parameter value. The scale callback only
        updates the adjacent text label; simulation routines read the variable directly.
        """
        row = tk.Frame(parent, bg=MAHOGANY_DARK)
        row.pack(fill="x", pady=(3, 0))

        tk.Label(
            row,
            text=label,
            bg=MAHOGANY_DARK,
            fg=CREAM,
            font=("Segoe UI", 8),
        ).pack(side="left")

        value_label = tk.Label(
            row,
            text=formatter(variable.get()),
            bg=MAHOGANY_DARK,
            fg=BRASS_LIGHT,
            font=("Consolas", 8),
        )
        value_label.pack(side="right")

        def update_label(value: str) -> None:
            """
            Refresh the textual value displayed beside one slider.
            """
            value_label.configure(text=formatter(value))

        ttk.Scale(
            parent,
            from_=low,
            to=high,
            variable=variable,
            command=update_label,
            style="TScale",
        ).pack(fill="x", pady=(1, 0))

    def _bind_events(self) -> None:
        """
        Bind keyboard shortcuts to the same operations exposed by the control buttons.
        """
        self.root.bind("<space>", lambda _event: self.toggle_pause())
        self.root.bind("r", lambda _event: self.reset())
        self.root.bind("R", lambda _event: self.reset())
        self.root.bind("n", lambda _event: self.release_one())
        self.root.bind("N", lambda _event: self.release_one())
        self.root.bind("b", lambda _event: self.release_burst())
        self.root.bind("B", lambda _event: self.release_burst())
        self.root.bind("h", lambda _event: self.toggle_help())
        self.root.bind("H", lambda _event: self.toggle_help())
        self.root.bind("<Up>", lambda _event: self.adjust_release_rate(+2.0))
        self.root.bind("<Down>", lambda _event: self.adjust_release_rate(-2.0))
        self.root.bind("<Escape>", lambda _event: self.close())

    # ------------------------------------------------------------------
    # Controls
    # ------------------------------------------------------------------

    def change_colour_layout(self, selected_name: str) -> None:
        """
        Apply one of the five colour layouts without resetting the experiment.

        Tk widgets keep the colours assigned when they are created. The method
        therefore updates the active palette, destroys only the Canvas and side
        panel, and rebuilds those widgets. Simulation state, balls, counts,
        controls, the animation callback, and the close handler are preserved.
        """
        if self._closing:
            return

        if selected_name not in COLOUR_LAYOUTS:
            return

        activate_colour_layout(selected_name)
        self.root.configure(bg=MAHOGANY_DEEP)

        # Remove only interface widgets. Root bindings, WM_DELETE_WINDOW, and
        # the scheduled animation loop belong to the root and remain active.
        for child in self.root.winfo_children():
            child.destroy()

        self._build_ui()

        # Restore the correct operational labels after rebuilding.
        self.pause_button.configure(text="Pause" if self.running else "Resume")
        self.status_label.configure(
            text="RUNNING" if self.running else "PAUSED",
            bg=STATUS_RUNNING if self.running else STATUS_PAUSED,
        )

        # Draw immediately so a paused simulation also changes colour without
        # waiting for any state update.
        try:
            self.root.update_idletasks()
            self._draw(self._layout())
        except tk.TclError:
            # Ignore a late theme event if shutdown has already begun.
            pass

    def close(self) -> None:
        """
        Stop the animation loop and close the Tk application cleanly.

        The method is deliberately idempotent because Windows may deliver more
        than one close-related event while the application is under load. The
        window is withdrawn first so it disappears immediately, then the queued
        ``after`` callback is cancelled, dynamic state is released, Tk's main
        loop is stopped, and the widget hierarchy is destroyed.
        """
        if self._closing:
            return

        self._closing = True
        self.running = False

        # Hide the window immediately. This gives prompt visual feedback even
        # when the current scene contains many Canvas objects.
        try:
            self.root.withdraw()
        except tk.TclError:
            pass

        # Prevent the animation callback from running again after destruction.
        if self._after_id is not None:
            try:
                self.root.after_cancel(self._after_id)
            except tk.TclError:
                # The callback may already be executing or may have completed.
                pass
            finally:
                self._after_id = None

        # Release the largest Python-side collections before closing. This is
        # not required for correctness, but reduces shutdown work for long runs.
        self.balls.clear()
        self.impacts.clear()
        self.sparks.clear()
        self.burst_queue = 0

        # ``quit`` terminates ``mainloop``; ``destroy`` releases all Tk widgets
        # and the associated Tcl interpreter.
        try:
            self.root.quit()
        except tk.TclError:
            pass

        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def toggle_pause(self) -> None:
        """
        Toggle simulation advancement while leaving the current scene visible.

        Rendering continues while paused, but no balls or short-lived effects advance.
        """
        self.running = not self.running
        self.pause_button.configure(text="Pause" if self.running else "Resume")
        self.status_label.configure(
            text="RUNNING" if self.running else "PAUSED",
            bg=STATUS_RUNNING if self.running else STATUS_PAUSED,
        )

    def toggle_help(self) -> None:
        """
        Show or hide the in-canvas help panel.
        """
        self.show_help = not self.show_help

    def adjust_release_rate(self, amount: float) -> None:
        """
        Change the automatic release rate and clamp it to the supported interval.
        """
        self.release_rate.set(
            max(1.0, min(65.0, self.release_rate.get() + amount))
        )

    def reset(self) -> None:
        """
        Return the stochastic experiment to an empty initial state.

        Configuration values and display switches are deliberately retained.
        """
        self.balls.clear()
        self.impacts.clear()
        self.sparks.clear()
        self.bin_counts = [0 for _ in range(self.bins)]
        self.expected_counts = [0.0 for _ in range(self.bins)]
        self.total_released = 0
        self.total_settled = 0
        self.spawn_accumulator = 0.0
        self.burst_queue = 0

    def release_one(self) -> None:
        """
        Generate one ball immediately using the current geometry and probability.
        """
        self._spawn_ball(self._layout())

    def release_burst(self) -> None:
        """
        Queue up to 100 releases without exceeding the global total-ball limit.

        The queue is consumed over several frames rather than generated all at once.
        """
        available = max(0, self.MAX_TOTAL_BALLS - self.total_released)
        self.burst_queue += min(100, available)

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    def _layout(self) -> Layout:
        """
        Calculate all responsive board coordinates from the current Canvas dimensions.

        The returned immutable object is shared by update and drawing routines for the
        current frame. Minimum dimensions keep the geometry valid during early startup.
        """
        width = max(float(self.canvas.winfo_width()), 760.0)
        height = max(float(self.canvas.winfo_height()), 700.0)

        center_x = width * 0.5

        # Use almost the complete left canvas. Only a narrow outer margin is
        # retained so that the frame and its shadow remain visible.
        horizontal_margin = 9.0
        board_width = width - 2.0 * horizontal_margin
        board_left = horizontal_margin
        board_right = width - horizontal_margin
        board_top = 7.0
        board_bottom = height - 18.0

        frame_thickness = 20.0
        inner_left = board_left + frame_thickness
        inner_right = board_right - frame_thickness
        inner_top = board_top + frame_thickness
        inner_bottom = board_bottom - frame_thickness

        # Allow the peg lattice and receiving bins to expand with the enlarged
        # board rather than retaining the former narrow maximum spacing.
        peg_dx = min(
            66.0,
            (inner_right - inner_left) / (self.rows + 2.35),
        )
        usable_vertical = inner_bottom - inner_top
        peg_dy = min(
            49.0,
            (usable_vertical - 265.0) / max(self.rows, 1),
        )
        peg_dy = max(34.0, peg_dy)

        peg_radius = max(5.0, min(8.2, peg_dx * 0.14))
        nominal_ball_radius = max(4.5, min(7.2, peg_dx * 0.125))

        funnel_y = inner_top + 24.0
        first_peg_y = funnel_y + 66.0

        bin_top = min(
            height - 190.0,
            first_peg_y + self.rows * peg_dy + 23.0,
        )
        bin_bottom = inner_bottom - 8.0

        bin_left = center_x - self.bins * peg_dx / 2.0
        bin_right = center_x + self.bins * peg_dx / 2.0
        bin_width = (bin_right - bin_left) / self.bins

        return Layout(
            width=width,
            height=height,
            center_x=center_x,
            board_left=board_left,
            board_right=board_right,
            board_top=board_top,
            board_bottom=board_bottom,
            inner_left=inner_left,
            inner_right=inner_right,
            inner_top=inner_top,
            inner_bottom=inner_bottom,
            funnel_y=funnel_y,
            first_peg_y=first_peg_y,
            peg_dx=peg_dx,
            peg_dy=peg_dy,
            peg_radius=peg_radius,
            nominal_ball_radius=nominal_ball_radius,
            bin_left=bin_left,
            bin_right=bin_right,
            bin_top=bin_top,
            bin_bottom=bin_bottom,
            bin_width=bin_width,
            bins=self.bins,
        )

    def _peg_positions(self, layout: Layout) -> Iterable[tuple[float, float]]:
        """
        Yield peg-centre coordinates row by row for the triangular lattice.

        Row r contains r + 1 pegs and is centred about the board's vertical axis.
        """
        for row in range(self.rows):
            y = layout.first_peg_y + row * layout.peg_dy
            start_x = layout.center_x - row * layout.peg_dx / 2.0
            for column in range(row + 1):
                yield start_x + column * layout.peg_dx, y

    # ------------------------------------------------------------------
    # Exact probability model
    # ------------------------------------------------------------------

    def _spawn_ball(self, layout: Layout) -> None:
        """
        Create one ball if live-object and total-run safety limits permit.

        The exact Bernoulli path is generated first. Visual radius, colour, speed, and
        reflection phase are then assigned without altering the selected final bin.
        """
        if len(self.balls) >= self.MAX_LIVE_BALLS:
            return
        if self.total_released >= self.MAX_TOTAL_BALLS:
            return

        probability = max(0.0, min(1.0, self.right_probability.get()))
        path, impact_indices, bin_index = self._generate_path(
            layout,
            probability,
        )

        radius = (
            layout.nominal_ball_radius
            * max(0.60, min(1.50, self.ball_scale.get()))
        )

        ball = Ball(
            path=path,
            impact_indices=impact_indices,
            bin_index=bin_index,
            right_probability=probability,
            radius=radius,
            color=random.choice(BALL_COLORS),
            base_speed=random.uniform(195.0, 240.0),
            rotation_phase=random.random() * math.tau,
        )

        self.balls.append(ball)
        self.total_released += 1

    def _generate_path(
        self,
        layout: Layout,
        probability_right: float,
    ) -> tuple[list[tuple[float, float]], set[int], int]:
        """
        Generate the exact random decisions and the smooth visual path for one ball.

        At every row a single ``random.random()`` draw selects right with probability
        ``probability_right``. The final bin equals the number of right selections.
        Intermediate side nodes control appearance only; lattice endpoints preserve the
        correct combinatorial path.
        """
        points: list[tuple[float, float]] = []
        impact_indices: set[int] = set()

        x = layout.center_x
        y = layout.funnel_y + 7.0
        points.append((x, y))

        rights = 0
        half_step = layout.peg_dx * 0.5
        bounce = max(0.35, min(1.50, self.bounce_amplitude.get()))

        for row in range(self.rows):
            peg_y = layout.first_peg_y + row * layout.peg_dy

            points.append((x, peg_y - layout.peg_radius - 0.7))
            impact_indices.add(len(points) - 1)

            # This is the only stochastic branch for the current row.
            # It implements one independent Bernoulli(p) trial exactly.
            direction = 1 if random.random() < probability_right else -1
            if direction > 0:
                rights += 1

            lateral_fraction = 0.24 + 0.12 * bounce
            downward_fraction = 0.14 + 0.12 * bounce

            side_x = x + direction * layout.peg_dx * lateral_fraction
            side_y = peg_y + layout.peg_dy * downward_fraction

            next_x = x + direction * half_step
            next_y = peg_y + layout.peg_dy * 0.66

            points.append((side_x, side_y))
            points.append((next_x, next_y))
            x = next_x

        # A path containing exactly ``rights`` right decisions belongs in
        # bin ``rights``; no geometric approximation is used for bin selection.
        bin_index = rights
        bin_center_x = layout.bin_left + (bin_index + 0.5) * layout.bin_width

        points.append((x, layout.bin_top - 17.0))
        points.append((bin_center_x, layout.bin_top - 4.0))
        points.append((bin_center_x, layout.bin_bottom - 9.0))

        return points, impact_indices, bin_index

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def _update_simulation(self, dt: float, layout: Layout) -> None:
        """
        Advance automatic release scheduling, balls, impacts, and spark particles.

        Expired effects are removed by rebuilding compact active lists. This avoids
        retaining dead objects and keeps per-frame work bounded.
        """
        if not self.running:
            return

        self.spawn_accumulator += dt * self.release_rate.get()
        while self.spawn_accumulator >= 1.0:
            self._spawn_ball(layout)
            self.spawn_accumulator -= 1.0

        burst_now = min(9, self.burst_queue)
        for _ in range(burst_now):
            self._spawn_ball(layout)
        self.burst_queue -= burst_now

        active_balls: list[Ball] = []
        for ball in self.balls:
            self._advance_ball(ball, dt)
            if not ball.settled:
                active_balls.append(ball)
        self.balls = active_balls

        active_impacts: list[ImpactEffect] = []
        for impact in self.impacts:
            impact.age += dt
            if impact.age < impact.duration:
                active_impacts.append(impact)
        self.impacts = active_impacts

        active_sparks: list[Spark] = []
        for spark in self.sparks:
            spark.age += dt
            if spark.age < spark.life:
                spark.vy += 125.0 * dt
                spark.x += spark.vx * dt
                spark.y += spark.vy * dt
                active_sparks.append(spark)
        self.sparks = active_sparks

    def _advance_ball(self, ball: Ball, dt: float) -> None:
        """
        Move one ball through as many path segments as the current time step allows.

        Smoothstep interpolation provides zero slope at segment endpoints. Any unused
        part of ``dt`` carries into the next segment, which makes motion independent of
        minor frame-rate variation.
        """
        if ball.settled:
            return

        remaining_dt = dt
        speed_multiplier = max(0.25, min(1.50, self.fall_speed.get()))

        while remaining_dt > 1.0e-8 and not ball.settled:
            if ball.segment >= len(ball.path) - 1:
                self._settle_ball(ball)
                break

            x0, y0 = ball.path[ball.segment]
            x1, y1 = ball.path[ball.segment + 1]

            dx = x1 - x0
            dy = y1 - y0
            segment_length = math.hypot(dx, dy)

            if segment_length < 1.0e-9:
                ball.segment += 1
                ball.progress = 0.0
                continue

            speed = (
                ball.base_speed
                * speed_multiplier
                * (1.0 + 0.020 * ball.segment)
            )

            progress_delta = remaining_dt * speed / segment_length
            advance = min(progress_delta, 1.0 - ball.progress)
            ball.progress += advance

            # Cubic smoothstep: s(t) = 3t^2 - 2t^3. It satisfies
            # s(0)=0, s(1)=1, and has zero endpoint derivatives.
            t = ball.progress
            eased = 3.0 * t * t - 2.0 * t * t * t

            ball.x = x0 + dx * eased
            ball.y = y0 + dy * eased
            ball.rotation_phase += dt * speed * 0.020

            if self.trails_enabled.get():
                ball.trail.append((ball.x, ball.y))
            else:
                ball.trail.clear()

            consumed = advance * segment_length / max(speed, 1.0e-9)
            remaining_dt = max(0.0, remaining_dt - consumed)

            if ball.progress >= 0.999999:
                ball.segment += 1
                ball.progress = 0.0

                if (
                    ball.segment in ball.impact_indices
                    and self.effects_enabled.get()
                    and self.effect_intensity.get() > 0.0
                ):
                    impact_x, impact_y = ball.path[ball.segment]
                    strength = max(
                        0.0,
                        min(1.25, self.effect_intensity.get()),
                    )

                    self.impacts.append(
                        ImpactEffect(
                            x=impact_x,
                            y=impact_y,
                            color=ball.color,
                            strength=strength,
                        )
                    )

                    spark_count = 2 + round(3 * strength)
                    for spark_index in range(spark_count):
                        angle = (
                            -math.pi * 0.95
                            + spark_index * math.pi / max(1, spark_count - 1)
                            + random.uniform(-0.18, 0.18)
                        )
                        speed_spark = random.uniform(32.0, 72.0) * strength
                        self.sparks.append(
                            Spark(
                                x=impact_x,
                                y=impact_y,
                                vx=math.cos(angle) * speed_spark,
                                vy=math.sin(angle) * speed_spark,
                                life=random.uniform(0.16, 0.30),
                                size=random.uniform(1.0, 2.2),
                            )
                        )

                if ball.segment >= len(ball.path) - 1:
                    self._settle_ball(ball)

    def _settle_ball(self, ball: Ball) -> None:
        """
        Commit one ball to its receiving bin exactly once.

        Besides incrementing the observed integer count, add this ball's full binomial
        probability vector to ``expected_counts``. This is essential when p changes.
        """
        if ball.settled:
            return

        ball.settled = True
        self.bin_counts[ball.bin_index] += 1
        self.total_settled += 1

        # Add this ball's theoretical probability mass to every bin.
        # Storing per-ball expectations keeps the curve correct if the user
        # changes p while earlier balls are still part of the experiment.
        probabilities = self._binomial_probabilities(
            ball.right_probability
        )
        for index, probability in enumerate(probabilities):
            self.expected_counts[index] += probability

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def _binomial_probabilities(self, probability_right: float) -> list[float]:
        """
        Return P(K=k) for every receiving bin k under Binomial(rows, p).

        The input is clamped defensively to [0, 1]. ``math.comb`` evaluates the exact
        integer binomial coefficients before floating-point probability scaling.
        """
        # Enforce a valid Bernoulli probability even if this private
        # routine is called programmatically with an out-of-range value.
        p = max(0.0, min(1.0, probability_right))
        q = 1.0 - p

        # k ranges from zero right turns to n right turns, exactly matching
        # receiving-bin indices 0..n.
        return [
            math.comb(self.rows, k)
            * (p ** k)
            * (q ** (self.rows - k))
            for k in range(self.bins)
        ]

    def _observed_statistics(self) -> tuple[float, float]:
        """
        Calculate population mean and standard deviation from settled integer counts.

        The variance denominator is N, not N-1, because the displayed balls constitute
        the complete simulated population rather than a sample estimator.
        """
        if self.total_settled == 0:
            return 0.0, 0.0

        mean = (
            sum(index * count for index, count in enumerate(self.bin_counts))
            / self.total_settled
        )
        variance = (
            sum(
                count * (index - mean) ** 2
                for index, count in enumerate(self.bin_counts)
            )
            / self.total_settled
        )

        return mean, math.sqrt(max(0.0, variance))

    def _expected_statistics(self) -> tuple[float, float]:
        """
        Calculate mean and standard deviation from accumulated expected bin counts.

        Before the first ball settles, return the analytical Binomial(n, p) values for
        the currently configured probability.
        """
        total = sum(self.expected_counts)

        if total <= 0.0:
            p = self.right_probability.get()
            return (
                self.rows * p,
                math.sqrt(self.rows * p * (1.0 - p)),
            )

        mean = (
            sum(index * value for index, value in enumerate(self.expected_counts))
            / total
        )
        variance = (
            sum(
                value * (index - mean) ** 2
                for index, value in enumerate(self.expected_counts)
            )
            / total
        )

        return mean, math.sqrt(max(0.0, variance))

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def _draw(self, layout: Layout) -> None:
        """
        Redraw the complete Canvas scene in a deliberate back-to-front layer order.

        Canvas items are recreated each frame. For this bounded educational scene, the
        simple deterministic layer order is clearer than managing many persistent IDs.
        """
        self.canvas.delete("all")

        self._draw_wall(layout)
        self._draw_board_shadow(layout)
        self._draw_wooden_frame(layout)
        self._draw_felt(layout)
        self._draw_bins(layout)
        self._draw_pegs(layout)
        self._draw_scientific_annotations(layout)
        self._draw_impacts()
        self._draw_sparks()
        self._draw_live_balls()

        if self.glass_enabled.get():
            self._draw_glass(layout)

        self._draw_title_plate(layout)
        self._draw_header(layout)
        self._draw_statistics(layout)

        if self.show_help:
            self._draw_help(layout)

    def _draw_wall(self, layout: Layout) -> None:
        """
        Paint the outer blue gradient and side vignette behind the apparatus.
        """
        top = self._hex_to_rgb(WALL_TOP)
        bottom = self._hex_to_rgb(WALL_BOTTOM)

        strips = 38
        for index in range(strips):
            t = index / max(1, strips - 1)
            rgb = tuple(
                round(top[channel] * (1.0 - t) + bottom[channel] * t)
                for channel in range(3)
            )
            y0 = layout.height * index / strips
            y1 = layout.height * (index + 1) / strips + 1.0
            self.canvas.create_rectangle(
                0,
                y0,
                layout.width,
                y1,
                fill=self._rgb_to_hex(rgb),
                outline="",
            )

        # Soft vignette using progressively darker side bands.
        for index in range(8):
            inset = index * 8.0
            shade = self._blend(WALL_SHADOW, WALL_TOP, index / 8.0)
            self.canvas.create_line(
                inset,
                0,
                inset,
                layout.height,
                fill=shade,
                width=10,
            )
            self.canvas.create_line(
                layout.width - inset,
                0,
                layout.width - inset,
                layout.height,
                fill=shade,
                width=10,
            )

    def _draw_board_shadow(self, layout: Layout) -> None:
        """
        Draw several offset rectangles that approximate a soft frame shadow.
        """
        for offset, shade in (
            (18.0, BOARD_SHADOW_1),
            (12.0, BOARD_SHADOW_2),
            (7.0, BOARD_SHADOW_3),
        ):
            self.canvas.create_rectangle(
                layout.board_left + offset,
                layout.board_top + offset,
                layout.board_right + offset,
                layout.board_bottom + offset,
                fill=shade,
                outline="",
            )

    def _draw_wooden_frame(self, layout: Layout) -> None:
        """
        Render the layered blue frame, bevel highlights, texture, and corner fasteners.

        The historical method name is retained for compatibility with earlier versions,
        although the current frame is a blue technical-panel design rather than wood.
        """
        lighting = max(0.25, min(1.0, self.board_lighting.get()))

        self.canvas.create_rectangle(
            layout.board_left,
            layout.board_top,
            layout.board_right,
            layout.board_bottom,
            fill=MAHOGANY_DEEP,
            outline=FRAME_OUTLINE,
            width=4,
        )

        self.canvas.create_rectangle(
            layout.board_left + 5.0,
            layout.board_top + 5.0,
            layout.board_right - 5.0,
            layout.board_bottom - 5.0,
            fill=MAHOGANY_MID,
            outline=MAHOGANY_LIGHT,
            width=3,
        )

        self.canvas.create_rectangle(
            layout.board_left + 12.0,
            layout.board_top + 12.0,
            layout.board_right - 12.0,
            layout.board_bottom - 12.0,
            fill=MAHOGANY_DARK,
            outline=MAHOGANY_HIGHLIGHT,
            width=2,
        )

        # Bevel highlights.
        highlight = self._blend(
            MAHOGANY_MID,
            MAHOGANY_HIGHLIGHT,
            0.65 * lighting,
        )
        self.canvas.create_line(
            layout.board_left + 7.0,
            layout.board_top + 7.0,
            layout.board_right - 7.0,
            layout.board_top + 7.0,
            fill=highlight,
            width=3,
        )
        self.canvas.create_line(
            layout.board_left + 7.0,
            layout.board_top + 7.0,
            layout.board_left + 7.0,
            layout.board_bottom - 7.0,
            fill=highlight,
            width=3,
        )

        # Deterministic brushed-panel texture.
        span = layout.board_right - layout.board_left
        for index in range(20):
            base_y = layout.board_top + 18.0 + index * 32.0
            if base_y >= layout.board_bottom - 15.0:
                break

            points: list[float] = []
            samples = 28
            for sample in range(samples + 1):
                t = sample / samples
                x = layout.board_left + 14.0 + t * (span - 28.0)
                wave = (
                    2.2 * math.sin(t * math.tau * 2.0 + index * 0.72)
                    + 1.0 * math.sin(t * math.tau * 5.0 + index)
                )
                points.extend((x, base_y + wave))

            self.canvas.create_line(
                *points,
                fill=FRAME_TEXTURE,
                width=1,
                smooth=True,
                splinesteps=8,
            )

        # Metal corner screws.
        for x, y in (
            (layout.board_left + 18.0, layout.board_top + 18.0),
            (layout.board_right - 18.0, layout.board_top + 18.0),
            (layout.board_left + 18.0, layout.board_bottom - 18.0),
            (layout.board_right - 18.0, layout.board_bottom - 18.0),
        ):
            self._draw_brass_screw(x, y, 6.0)

    def _draw_felt(self, layout: Layout) -> None:
        """
        Render the dark inner board, subtle texture, funnel, and side guide rails.

        The historical method name is retained; the current visual surface is blue.
        """
        self.canvas.create_rectangle(
            layout.inner_left,
            layout.inner_top,
            layout.inner_right,
            layout.inner_bottom,
            fill=FELT_DEEP,
            outline=SURFACE_OUTLINE,
            width=2,
        )

        # Felt gradient.
        steps = 26
        top = self._hex_to_rgb(FELT_LIGHT)
        bottom = self._hex_to_rgb(FELT_DEEP)

        for index in range(steps):
            t = index / max(1, steps - 1)
            rgb = tuple(
                round(top[channel] * (1.0 - t) + bottom[channel] * t)
                for channel in range(3)
            )
            y0 = layout.inner_top + (
                layout.inner_bottom - layout.inner_top
            ) * index / steps
            y1 = layout.inner_top + (
                layout.inner_bottom - layout.inner_top
            ) * (index + 1) / steps + 1.0

            self.canvas.create_rectangle(
                layout.inner_left + 1.0,
                y0,
                layout.inner_right - 1.0,
                y1,
                fill=self._rgb_to_hex(rgb),
                outline="",
            )

        # Fine felt texture dots.
        for row in range(15):
            y = layout.inner_top + 12.0 + row * 34.0
            if y >= layout.inner_bottom:
                break
            for column in range(22):
                x = layout.inner_left + 14.0 + column * 34.0
                if x >= layout.inner_right:
                    break
                offset = 4.0 * math.sin(row * 1.2 + column * 0.7)
                self.canvas.create_oval(
                    x + offset,
                    y,
                    x + offset + 1.2,
                    y + 1.2,
                    fill=SURFACE_TEXTURE,
                    outline="",
                )

        # Funnel and upper metal guide.
        funnel_width = layout.peg_dx * 0.95
        self.canvas.create_polygon(
            layout.center_x - funnel_width,
            layout.funnel_y - 18.0,
            layout.center_x + funnel_width,
            layout.funnel_y - 18.0,
            layout.center_x + layout.nominal_ball_radius * 1.8,
            layout.funnel_y + 21.0,
            layout.center_x - layout.nominal_ball_radius * 1.8,
            layout.funnel_y + 21.0,
            fill=MAHOGANY_MID,
            outline=BRASS_MID,
            width=2,
        )

        self.canvas.create_line(
            layout.center_x - funnel_width + 4.0,
            layout.funnel_y - 13.0,
            layout.center_x + funnel_width - 4.0,
            layout.funnel_y - 13.0,
            fill=BRASS_LIGHT,
            width=2,
        )

        # Side guide rails.
        rail_left_top = layout.center_x - layout.peg_dx * 0.78
        rail_right_top = layout.center_x + layout.peg_dx * 0.78

        self.canvas.create_line(
            rail_left_top,
            layout.first_peg_y - 37.0,
            layout.bin_left - 9.0,
            layout.bin_top - 5.0,
            fill=BRASS_DARK,
            width=5,
        )
        self.canvas.create_line(
            rail_left_top,
            layout.first_peg_y - 37.0,
            layout.bin_left - 9.0,
            layout.bin_top - 5.0,
            fill=BRASS_LIGHT,
            width=1,
        )

        self.canvas.create_line(
            rail_right_top,
            layout.first_peg_y - 37.0,
            layout.bin_right + 9.0,
            layout.bin_top - 5.0,
            fill=BRASS_DARK,
            width=5,
        )
        self.canvas.create_line(
            rail_right_top,
            layout.first_peg_y - 37.0,
            layout.bin_right + 9.0,
            layout.bin_top - 5.0,
            fill=BRASS_LIGHT,
            width=1,
        )

    def _draw_bins(self, layout: Layout) -> None:
        """
        Render receiving compartments, count silhouettes, labels, piles, and theory.

        The gold curve uses ``expected_counts`` and therefore represents the exact
        accumulated expectation for the probabilities used during the run.
        """
        max_observed = max(max(self.bin_counts), 1)
        max_expected = max(max(self.expected_counts), 1.0)
        scale_max = max(max_observed, max_expected, 1.0)

        chart_height = layout.bin_bottom - layout.bin_top - 12.0
        baseline = layout.bin_bottom - 4.0

        self.canvas.create_rectangle(
            layout.bin_left,
            layout.bin_top,
            layout.bin_right,
            layout.bin_bottom,
            fill=FELT_DEEP,
            outline=BRASS_DARK,
            width=3,
        )

        # Subtle distribution silhouette behind the marble piles.
        for index, count in enumerate(self.bin_counts):
            x0 = layout.bin_left + index * layout.bin_width + 3.0
            x1 = layout.bin_left + (index + 1) * layout.bin_width - 3.0
            height = chart_height * count / scale_max
            y0 = baseline - height

            self.canvas.create_rectangle(
                x0,
                y0,
                x1,
                baseline,
                fill=HISTOGRAM_SHADOW,
                outline="",
            )
            self.canvas.create_rectangle(
                x0 + 1.0,
                y0,
                x1 - 1.0,
                min(baseline, y0 + max(2.0, height * 0.10)),
                fill=HISTOGRAM_FILL,
                outline="",
            )

        # Metal dividers.
        for index in range(self.bins + 1):
            x = layout.bin_left + index * layout.bin_width
            self.canvas.create_line(
                x,
                layout.bin_top,
                x,
                layout.bin_bottom,
                fill=BRASS_DARK,
                width=4,
            )
            self.canvas.create_line(
                x - 1.0,
                layout.bin_top,
                x - 1.0,
                layout.bin_bottom,
                fill=BRASS_LIGHT,
                width=1,
            )

        if self.piles_enabled.get():
            self._draw_settled_marble_piles(layout, scale_max)

        # Labels and exact counts.
        for index, count in enumerate(self.bin_counts):
            x = layout.bin_left + (index + 0.5) * layout.bin_width

            self.canvas.create_text(
                x,
                layout.bin_bottom + 12.0,
                text=str(index),
                fill=CREAM,
                font=("Consolas", 8),
            )

            if count > 0:
                self.canvas.create_text(
                    x,
                    layout.bin_top - 11.0,
                    text=str(count),
                    fill=BRASS_LIGHT,
                    font=("Consolas", 8, "bold"),
                )

        self.canvas.create_text(
            layout.bin_left,
            layout.bin_top - 25.0,
            anchor="w",
            text="RECEIVING BINS",
            fill=BRASS_LIGHT,
            font=("Segoe UI", 8, "bold"),
        )

        if self.theory_enabled.get() and self.total_settled > 0:
            points: list[float] = []

            for index, expected in enumerate(self.expected_counts):
                x = layout.bin_left + (index + 0.5) * layout.bin_width
                y = baseline - chart_height * expected / scale_max
                points.extend((x, y))

            if len(points) >= 4:
                self.canvas.create_line(
                    *points,
                    fill=THEORY_RED,
                    width=4,
                    smooth=True,
                    splinesteps=20,
                )
                self.canvas.create_line(
                    *points,
                    fill=THEORY_HIGHLIGHT,
                    width=1,
                    smooth=True,
                    splinesteps=20,
                )

                for point_index in range(0, len(points), 2):
                    x = points[point_index]
                    y = points[point_index + 1]
                    self.canvas.create_oval(
                        x - 3.0,
                        y - 3.0,
                        x + 3.0,
                        y + 3.0,
                        fill=THEORY_RED,
                        outline=CREAM,
                    )

    def _draw_settled_marble_piles(
        self,
        layout: Layout,
        scale_max: float,
    ) -> None:
        """
        Draw a bounded representative packing of settled balls inside each bin.

        For large counts, displayed marble quantity is normalized to available drawing
        capacity. Statistical totals and printed bin counts remain exact.
        """
        pile_radius = min(4.1, layout.bin_width / 8.5)
        horizontal_step = pile_radius * 2.05
        vertical_step = pile_radius * 1.78

        max_columns = max(
            2,
            min(
                7,
                int((layout.bin_width - 8.0) / horizontal_step),
            ),
        )
        max_rows = max(
            2,
            min(
                8,
                int(
                    (layout.bin_bottom - layout.bin_top - 12.0)
                    / vertical_step
                ),
            ),
        )
        capacity = max_columns * max_rows

        for bin_index, count in enumerate(self.bin_counts):
            if count <= 0:
                continue

            # Use a normalized number of displayed marbles so the pile height
            # preserves the observed histogram even after counts become large.
            visible = max(
                1,
                min(
                    capacity,
                    round(capacity * count / max(scale_max, 1.0)),
                ),
            )

            left = layout.bin_left + bin_index * layout.bin_width
            center_x = left + layout.bin_width / 2.0
            bottom_y = layout.bin_bottom - pile_radius - 5.0

            drawn = 0
            row = 0
            while drawn < visible and row < max_rows:
                row_count = min(max_columns, visible - drawn)
                row_width = (row_count - 1) * horizontal_step
                start_x = center_x - row_width / 2.0

                # Hexagonal packing offset.
                offset = pile_radius * 0.55 if row % 2 else 0.0

                for column in range(row_count):
                    if drawn >= visible:
                        break

                    x = start_x + column * horizontal_step + offset
                    max_x = left + layout.bin_width - pile_radius - 4.0
                    min_x = left + pile_radius + 4.0
                    x = max(min_x, min(max_x, x))
                    y = bottom_y - row * vertical_step

                    color = BALL_COLORS[
                        (bin_index * 3 + drawn * 5 + row) % len(BALL_COLORS)
                    ]
                    self._draw_small_marble(
                        x,
                        y,
                        pile_radius,
                        color,
                    )
                    drawn += 1

                row += 1

    def _draw_pegs(self, layout: Layout) -> None:
        """
        Draw every peg with a shadow, metal collar, highlight, and lower rim.
        """
        lighting = max(0.25, min(1.0, self.board_lighting.get()))

        for x, y in self._peg_positions(layout):
            radius = layout.peg_radius

            # Shadow.
            self.canvas.create_oval(
                x - radius * 1.20 + 2.4,
                y - radius * 1.20 + 3.1,
                x + radius * 1.20 + 2.4,
                y + radius * 1.20 + 3.1,
                fill=PEG_SHADOW,
                outline="",
            )

            # Outer metal collar.
            self.canvas.create_oval(
                x - radius * 1.42,
                y - radius * 1.42,
                x + radius * 1.42,
                y + radius * 1.42,
                fill=BRASS_DARK,
                outline=PEG_OUTLINE,
            )

            # Main metal surface.
            body = self._blend(
                BRASS_MID,
                BRASS_LIGHT,
                0.22 * lighting,
            )
            self.canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=body,
                outline=BRASS_LIGHT,
                width=1,
            )

            # Specular highlight.
            self.canvas.create_oval(
                x - radius * 0.52,
                y - radius * 0.60,
                x + radius * 0.05,
                y - radius * 0.05,
                fill=BRASS_GLOW,
                outline="",
            )

            # Dark lower rim.
            self.canvas.create_arc(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                start=195,
                extent=150,
                style="arc",
                outline=PEG_RIM,
                width=2,
            )

    def _draw_impacts(self) -> None:
        """
        Draw expanding collision rings for all currently active impact effects.
        """
        for impact in self.impacts:
            phase = impact.age / impact.duration
            remaining = max(0.0, 1.0 - phase)
            radius = 3.0 + 20.0 * phase * impact.strength

            ring = self._blend(
                impact.color,
                BRASS_GLOW,
                0.55 + 0.40 * remaining,
            )

            self.canvas.create_oval(
                impact.x - radius,
                impact.y - radius,
                impact.x + radius,
                impact.y + radius,
                outline=ring,
                width=max(1, round(3.0 * remaining * impact.strength)),
            )

            inner = max(2.0, radius * 0.42)
            self.canvas.create_oval(
                impact.x - inner,
                impact.y - inner,
                impact.x + inner,
                impact.y + inner,
                outline=self._blend(BRASS_MID, BRASS_GLOW, remaining),
                width=1,
            )

    def _draw_sparks(self) -> None:
        """
        Draw active short-lived collision particles with age-dependent size and colour.
        """
        for spark in self.sparks:
            remaining = max(0.0, 1.0 - spark.age / spark.life)
            radius = max(0.5, spark.size * remaining)

            self.canvas.create_oval(
                spark.x - radius,
                spark.y - radius,
                spark.x + radius,
                spark.y + radius,
                fill=self._blend(BRASS_MID, BRASS_GLOW, remaining),
                outline="",
            )

    def _draw_live_balls(self) -> None:
        """
        Draw trails first and then render each moving ball above its trail.
        """
        for ball in self.balls:
            if self.trails_enabled.get() and len(ball.trail) > 1:
                points = list(ball.trail)
                for index in range(1, len(points)):
                    x0, y0 = points[index - 1]
                    x1, y1 = points[index]
                    fraction = index / len(points)

                    self.canvas.create_line(
                        x0,
                        y0,
                        x1,
                        y1,
                        fill=self._blend(
                            FELT_DEEP,
                            ball.color,
                            fraction * 0.82,
                        ),
                        width=max(
                            1,
                            round(ball.radius * 0.30 * fraction),
                        ),
                    )

            self._draw_marble(
                ball.x,
                ball.y,
                ball.radius,
                ball.color,
                ball.rotation_phase,
            )

    def _draw_marble(
        self,
        x: float,
        y: float,
        radius: float,
        color: str,
        phase: float,
    ) -> None:
        """
        Render one moving gray/white ball using layered 2D shading.

        The rotating internal reflection is an aesthetic cue only and has no effect on
        the ball path or probability.
        """
        gloss = max(0.0, min(1.0, self.marble_gloss.get()))

        # Drop shadow.
        self.canvas.create_oval(
            x - radius * 1.05 + 2.6,
            y - radius * 0.90 + 3.3,
            x + radius * 1.05 + 2.6,
            y + radius * 1.18 + 3.3,
            fill=WALL_SHADOW,
            outline="",
        )

        # Dark rim.
        self.canvas.create_oval(
            x - radius * 1.10,
            y - radius * 1.10,
            x + radius * 1.10,
            y + radius * 1.10,
            fill=BALL_RIM,
            outline="",
        )

        # Main body.
        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill=color,
            outline=self._blend(color, CREAM, 0.35),
            width=1,
        )

        # Lower shading.
        self.canvas.create_arc(
            x - radius * 0.92,
            y - radius * 0.92,
            x + radius * 0.92,
            y + radius * 0.92,
            start=185,
            extent=175,
            style="pieslice",
            fill=self._blend(color, BALL_SHADE, 0.42),
            outline="",
        )

        # Restore central colour over part of the shade to create a curved band.
        self.canvas.create_oval(
            x - radius * 0.82,
            y - radius * 0.84,
            x + radius * 0.72,
            y + radius * 0.62,
            fill=self._blend(color, CREAM, 0.05),
            outline="",
        )

        # Moving internal reflection.
        streak_x = math.cos(phase) * radius * 0.18
        self.canvas.create_arc(
            x - radius * 0.64 + streak_x,
            y - radius * 0.72,
            x + radius * 0.55 + streak_x,
            y + radius * 0.52,
            start=85,
            extent=120,
            style="arc",
            outline=self._blend(color, BALL_HIGHLIGHT, 0.42 * gloss),
            width=max(1, round(radius * 0.18)),
        )

        # Primary specular highlight.
        highlight_radius = radius * (0.19 + 0.14 * gloss)
        self.canvas.create_oval(
            x - radius * 0.52 - highlight_radius,
            y - radius * 0.55 - highlight_radius,
            x - radius * 0.52 + highlight_radius,
            y - radius * 0.55 + highlight_radius,
            fill=self._blend(color, BALL_HIGHLIGHT, 0.72 + 0.22 * gloss),
            outline="",
        )

        # Tiny sharp glint.
        glint = max(0.7, radius * 0.10 * gloss)
        self.canvas.create_oval(
            x - radius * 0.66 - glint,
            y - radius * 0.69 - glint,
            x - radius * 0.66 + glint,
            y - radius * 0.69 + glint,
            fill=CREAM,
            outline="",
        )

    def _draw_small_marble(
        self,
        x: float,
        y: float,
        radius: float,
        color: str,
    ) -> None:
        # Simplified rendering for settled piles keeps animation responsive.
        """
        Render a simplified small ball for dense settled-bin piles.

        Fewer layers are used than for moving balls to preserve frame rate.
        """
        self.canvas.create_oval(
            x - radius + 1.2,
            y - radius + 1.8,
            x + radius + 1.2,
            y + radius + 1.8,
            fill=WALL_SHADOW,
            outline="",
        )
        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill=color,
            outline=self._blend(color, CREAM, 0.28),
            width=1,
        )
        highlight = radius * 0.25
        self.canvas.create_oval(
            x - radius * 0.42 - highlight,
            y - radius * 0.47 - highlight,
            x - radius * 0.42 + highlight,
            y - radius * 0.47 + highlight,
            fill=self._blend(color, CREAM, 0.70),
            outline="",
        )

    def _draw_glass(self, layout: Layout) -> None:
        # Thin perimeter lines suggest a glass front.
        """
        Draw only a fine perimeter to suggest a protective glass cover.

        Diagonal reflection strokes are intentionally avoided because opaque Tk Canvas
        lines can resemble unexplained blue marks rather than transparent reflections.
        """
        self.canvas.create_rectangle(
            layout.inner_left + 4.0,
            layout.inner_top + 4.0,
            layout.inner_right - 4.0,
            layout.inner_bottom - 4.0,
            outline=self._blend(GLASS_EDGE, FELT_LIGHT, 0.45),
            width=1,
        )

        # No diagonal reflection strokes are drawn here. On opaque Tk Canvas
        # surfaces they look like blue lines rather than transparent glass.
        # The fine perimeter is enough to suggest the protective glass front.

    def _draw_title_plate(self, layout: Layout) -> None:
        """
        Draw the integrated upper title plate and its two fasteners.
        """
        plate_width = min(330.0, layout.board_right - layout.board_left - 90.0)
        plate_height = 34.0
        x0 = layout.center_x - plate_width / 2.0
        x1 = layout.center_x + plate_width / 2.0
        y0 = layout.board_top + 8.0
        y1 = y0 + plate_height

        self.canvas.create_rectangle(
            x0 + 3.0,
            y0 + 4.0,
            x1 + 3.0,
            y1 + 4.0,
            fill=WALL_SHADOW,
            outline="",
        )
        self.canvas.create_rectangle(
            x0,
            y0,
            x1,
            y1,
            fill=BRASS_DARK,
            outline=PLATE_OUTLINE,
            width=2,
        )
        self.canvas.create_rectangle(
            x0 + 3.0,
            y0 + 3.0,
            x1 - 3.0,
            y1 - 3.0,
            fill=BRASS_MID,
            outline=BRASS_LIGHT,
            width=1,
        )

        self.canvas.create_text(
            layout.center_x,
            (y0 + y1) / 2.0,
            text="THE GALTON QUINCUNX",
            fill=PLATE_TEXT,
            font=("Georgia", 13, "bold"),
        )

        self._draw_brass_screw(x0 + 13.0, (y0 + y1) / 2.0, 4.2)
        self._draw_brass_screw(x1 - 13.0, (y0 + y1) / 2.0, 4.2)

    def _draw_brass_screw(self, x: float, y: float, radius: float) -> None:
        """
        Draw one circular metal fastener with a horizontal slot.
        """
        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill=BRASS_MID,
            outline=BRASS_LIGHT,
            width=1,
        )
        self.canvas.create_line(
            x - radius * 0.55,
            y,
            x + radius * 0.55,
            y,
            fill=BRASS_DARK,
            width=1,
        )

    def _draw_header(self, layout: Layout) -> None:
        # The main title is integrated into the board's upper plate. Keep only
        # a compact live-ball indicator inside the upper-right frame.
        """
        Draw the compact live-ball indicator inside the upper-right board frame.

        The main title is already integrated into the board plate.
        """
        self.canvas.create_text(
            layout.board_right - 24.0,
            layout.board_top + 22.0,
            anchor="ne",
            text=f"{len(self.balls):03d} live",
            fill=CREAM,
            font=("Consolas", 10, "bold"),
        )


    def _draw_scientific_annotations(self, layout: Layout) -> None:
        """
        Draw compact mathematical notes and numerical values on the board.

        The layout is inspired by educational Galton-board posters showing
        the relationship between Pascal's triangle, binomial coefficients and
        the normal approximation, but adapted so the animation remains clear.
        """
        n = self.rows
        p = max(0.0, min(1.0, self.right_probability.get()))
        mu = n * p
        sigma = math.sqrt(max(0.0, n * p * (1.0 - p)))

        left_x = layout.inner_left + 22.0
        right_x = layout.inner_right - 245.0
        top_y = layout.inner_top + 62.0

        # Left formula block.
        left_text = (
            "MEAN AND DISPERSION\n"
            f"mu = n p = {n} x {p:.3f} = {mu:.3f}\n"
            f"sigma = sqrt(n p (1-p)) = {sigma:.3f}\n"
            f"Var(X) = n p (1-p) = {sigma**2:.3f}"
        )
        self.canvas.create_text(
            left_x,
            top_y,
            anchor="nw",
            text=left_text,
            fill=BRASS_LIGHT,
            font=("Segoe UI", 8, "bold"),
            justify="left",
            width=200,
        )

        # Right formula block.
        right_text = (
            "BINOMIAL MODEL\n"
            "P(X = k) = C(n,k) p^k (1-p)^(n-k)\n"
            "(a + b)^n = sum C(n,k) a^(n-k) b^k\n"
            f"for this board: X ~ Binomial({n}, {p:.3f})"
        )
        self.canvas.create_text(
            right_x,
            top_y,
            anchor="nw",
            text=right_text,
            fill=BRASS_LIGHT,
            font=("Segoe UI", 8, "bold"),
            justify="left",
            width=220,
        )

        # Centre annotation above the peg field.
        self.canvas.create_text(
            layout.center_x,
            layout.inner_top + 74.0,
            text="PASCAL TRIANGLE / BINOMIAL COEFFICIENTS",
            fill=CREAM,
            font=("Segoe UI", 8, "bold"),
        )

        # Educational side labels: row number and row sum.
        left_rows_x = layout.center_x - (n * layout.peg_dx / 2.0) - 68.0
        right_rows_x = layout.center_x + (n * layout.peg_dx / 2.0) + 68.0

        self.canvas.create_text(
            left_rows_x,
            layout.first_peg_y - 22.0,
            text="row n",
            fill=BRASS_LIGHT,
            font=("Consolas", 8, "bold"),
        )
        self.canvas.create_text(
            right_rows_x,
            layout.first_peg_y - 22.0,
            text="sum = 2^n",
            fill=BRASS_LIGHT,
            font=("Consolas", 8, "bold"),
        )

        display_rows = min(n, 10)
        for row in range(display_rows + 1):
            y = layout.first_peg_y + row * layout.peg_dy
            self.canvas.create_text(
                left_rows_x,
                y,
                text=str(row),
                fill=BRASS_LIGHT,
                font=("Consolas", 8),
            )
            self.canvas.create_text(
                right_rows_x,
                y,
                text=str(2 ** row),
                fill=BRASS_LIGHT,
                font=("Consolas", 8),
            )

        # Show the current Pascal row and expected percentages above the bins.
        coefficients = [math.comb(n, k) for k in range(n + 1)]
        probabilities = self._binomial_probabilities(p)

        coeff_y = layout.bin_top - 58.0
        prob_y = layout.bin_top - 42.0
        label_y = layout.bin_top - 74.0

        self.canvas.create_text(
            layout.center_x,
            label_y,
            text=f"Row n = {n} : coefficients C({n}, k) and expected percentages",
            fill=BRASS_LIGHT,
            font=("Segoe UI", 8, "bold"),
        )

        for k in range(n + 1):
            x = layout.bin_left + (k + 0.5) * layout.bin_width

            self.canvas.create_text(
                x,
                coeff_y,
                text=str(coefficients[k]),
                fill=CREAM,
                font=("Consolas", 8, "bold"),
            )
            self.canvas.create_text(
                x,
                prob_y,
                text=f"{100.0 * probabilities[k]:.1f}%",
                fill=MUTED,
                font=("Consolas", 7),
            )

        # Compact normal-approximation formula near the bottom of the board.
        normal_text = (
            "Normal approximation:  f(x) = (1 / (sigma sqrt(2 pi))) "
            "exp[-0.5 ((x - mu) / sigma)^2]"
        )
        self.canvas.create_text(
            layout.center_x,
            layout.bin_bottom + 18.0,
            text=normal_text,
            fill=BRASS_LIGHT,
            font=("Segoe UI", 8),
        )

    def _draw_statistics(self, layout: Layout) -> None:
        """
        Update the side-panel statistics and the compact parameter line on the board.
        """
        observed_mean, observed_std = self._observed_statistics()
        expected_mean, expected_std = self._expected_statistics()

        self.stats_label.configure(
            text=(
                f"released  {self.total_released:>6}\n"
                f"settled   {self.total_settled:>6}\n"
                f"mean      {observed_mean:>5.2f}  exp {expected_mean:>5.2f}\n"
                f"std dev   {observed_std:>5.2f}  exp {expected_std:>5.2f}\n"
                f"p(right)  {self.right_probability.get():>5.3f}\n"
                f"fps       {self.smoothed_fps:>5.1f}"
            )
        )

        self.canvas.create_text(
            layout.board_left + 24.0,
            layout.board_bottom - 7.0,
            anchor="sw",
            text=(
                f"rows={self.rows}   "
                f"speed={self.fall_speed.get():.2f}×   "
                f"bounce={self.bounce_amplitude.get():.2f}×   "
                f"gloss={self.marble_gloss.get():.2f}"
            ),
            fill=MUTED,
            font=("Consolas", 8),
        )

    def _draw_help(self, layout: Layout) -> None:
        """
        Draw an opaque explanatory overlay containing controls and model information.
        """
        width = min(640.0, layout.width - 80.0)
        height = 360.0
        x0 = (layout.width - width) / 2.0
        y0 = (layout.height - height) / 2.0

        self.canvas.create_rectangle(
            x0 + 8.0,
            y0 + 9.0,
            x0 + width + 8.0,
            y0 + height + 9.0,
            fill=WALL_TOP,
            outline="",
        )
        self.canvas.create_rectangle(
            x0,
            y0,
            x0 + width,
            y0 + height,
            fill=PARCHMENT,
            outline=MAHOGANY_DEEP,
            width=3,
        )

        self.canvas.create_text(
            x0 + 26.0,
            y0 + 22.0,
            anchor="nw",
            text="Controls and visual settings",
            fill=INK,
            font=("Georgia", 16, "bold"),
        )

        body = (
            "Release rate controls how frequently balls enter the board.\n"
            "Fall speed changes animation timing without changing probability.\n"
            "Right probability sets p in the exact Binomial(rows, p) model.\n"
            "Bounce amplitude changes only the visual deflection around each peg.\n"
            "Ball size affects newly released balls.\n"
            "Impact intensity controls rings and metallic spark particles.\n"
            "Marble gloss controls specular highlights and internal reflections.\n"
            "Board lighting controls metal and glass highlights.\n\n"
            "Marble piles show the settled distribution as packed balls. The red "
            "curve is the exact accumulated theoretical expectation, including "
            "runs where p is changed during the simulation.\n\n"
            "Press H to close this panel."
        )

        self.canvas.create_text(
            x0 + 26.0,
            y0 + 64.0,
            anchor="nw",
            width=width - 52.0,
            text=body,
            fill=INK,
            font=("Segoe UI", 10),
            spacing3=6,
        )

    # ------------------------------------------------------------------
    # Animation loop
    # ------------------------------------------------------------------

    def _tick(self) -> None:
        """
        Execute one animation frame and schedule the next frame with ``root.after``.

        Frame time is capped at 0.033 s so returning from a pause, window drag, or system
        stall cannot cause a large jump. FPS is exponentially smoothed for readability.
        """
        # A pending callback can begin just before a close event is processed.
        # Exit without touching widgets when shutdown has already started.
        if self._closing:
            self._after_id = None
            return

        # This callback is now executing, so its previously stored identifier
        # no longer represents a future event.
        self._after_id = None

        # perf_counter() is monotonic and suitable for animation timing.
        # Clamp dt to about 30 FPS worth of motion after temporary stalls.
        now = time.perf_counter()
        dt = min(now - self.last_time, 0.033)
        self.last_time = now

        if dt > 1.0e-8:
            instantaneous_fps = 1.0 / dt
            self.smoothed_fps = (
                0.92 * self.smoothed_fps
                + 0.08 * instantaneous_fps
            )

        layout = self._layout()
        self._update_simulation(dt, layout)
        self._draw(layout)

        # Schedule another frame only while the application remains open.
        # Store the Tcl callback identifier for cancellation by ``close``.
        if not self._closing:
            try:
                self._after_id = self.root.after(
                    round(1000 / self.TARGET_FPS),
                    self._tick,
                )
            except tk.TclError:
                # Tk has already begun destroying the interpreter.
                self._after_id = None

    # ------------------------------------------------------------------
    # Colour helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _hex_to_rgb(value: str) -> tuple[int, int, int]:
        """
        Convert a ``#RRGGBB`` colour string to an integer RGB tuple.
        """
        value = value.lstrip("#")
        return tuple(
            int(value[index:index + 2], 16)
            for index in (0, 2, 4)
        )

    @staticmethod
    def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
        """
        Convert an integer RGB tuple to a lowercase ``#rrggbb`` colour string.
        """
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    @classmethod
    def _blend(cls, first: str, second: str, fraction: float) -> str:
        """
        Linearly interpolate between two RGB colours.

        ``fraction`` is clamped to [0, 1], making this helper safe for age-based visual
        effects that may slightly overshoot because of frame timing.
        """
        fraction = max(0.0, min(1.0, fraction))
        first_rgb = cls._hex_to_rgb(first)
        second_rgb = cls._hex_to_rgb(second)

        mixed = tuple(
            round(
                first_rgb[channel] * (1.0 - fraction)
                + second_rgb[channel] * fraction
            )
            for channel in range(3)
        )
        return cls._rgb_to_hex(mixed)


def main() -> None:
    """
    Create the Tk root window, request maximization, and enter Tk's event loop.

    Windows supports ``state("zoomed")``. A secondary ``-zoomed`` attempt and a
    silent fallback preserve startup on other Tk window managers.
    """
    root = tk.Tk()

    # Open maximized on Windows. The fallbacks preserve compatibility with
    # other Tk window managers without preventing the program from starting.
    try:
        root.state("zoomed")
    except tk.TclError:
        try:
            root.attributes("-zoomed", True)
        except tk.TclError:
            pass

    GaltonBoardApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
