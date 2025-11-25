from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# Allow your tiiny.host site to call this API.
# In production, replace "*" with your actual tiiny.host URL for better security.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # e.g. ["https://your-site.tiiny.site"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GRID_ROWS = 4
GRID_COLS = 3

# Block definitions: each side is [color1, color2]
BLOCKS = [
    {
        "id": 1,
        "sides": [
            ["red", "red"],
            ["blue", "yellow"],
            ["green", "purple"],
            ["yellow", "green"],
        ],
    },
    {
        "id": 2,
        "sides": [
            ["yellow", "yellow"],
            ["green", "red"],
            ["blue", "purple"],
            ["red", "blue"],
        ],
    },
    {
        "id": 3,
        "sides": [
            ["green", "green"],
            ["yellow", "purple"],
            ["blue", "yellow"],
            ["purple", "red"],
        ],
    },
    {
        "id": 4,
        "sides": [
            ["blue", "blue"],
            ["green", "purple"],
            ["red", "yellow"],
            ["purple", "red"],
        ],
    },
    {
        "id": 5,
        "sides": [
            ["purple", "purple"],
            ["green", "blue"],
            ["yellow", "green"],
            ["red", "blue"],
        ],
    },
]


def create_empty_grid():
    return [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]


def try_place_block(grid, block):
    max_attempts = 200
    total_cells = GRID_ROWS * GRID_COLS

    for _ in range(max_attempts):
        # Pick random side
        side = random.choice(block["sides"])

        # Orientation: horizontal or vertical
        horizontal = random.random() < 0.5

        # Flip via 180° rotation
        flipped = random.random() < 0.5
        first_color = side[1] if flipped else side[0]
        second_color = side[0] if flipped else side[1]

        # Random starting cell
        cell_index = random.randrange(total_cells)
        row = cell_index // GRID_COLS
        col = cell_index % GRID_COLS

        row2, col2 = row, col
        if horizontal:
            col2 = col + 1
        else:
            row2 = row + 1

        # Bounds check
        if row2 >= GRID_ROWS or col2 >= GRID_COLS:
            continue

        # Occupancy check
        if grid[row][col] is not None or grid[row2][col2] is not None:
            continue

        # Place block
        grid[row][col] = first_color
        grid[row2][col2] = second_color
        return True

    return False


def generate_pattern_grid():
    while True:
        grid = create_empty_grid()
        success = True

        for block in BLOCKS:
            if not try_place_block(grid, block):
                success = False
                break

        if success:
            return grid


from fastapi import Request

@app.api_route("/generate-card", methods=["GET", "HEAD", "POST"])
async def generate_card(request: Request):
    """
    Returns a JSON grid:
    {
      "grid": [
        ["blue", "red", null],
        ...
      ]
    }

    Supports GET, HEAD, and POST so uptime monitors do not get 405 errors.
    """
    grid = generate_pattern_grid()
    return {"grid": grid}

