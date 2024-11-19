from megaverse_api import MegaverseAPI
import time


class MegaverseController:
    """Controller to manage the Megaverse grid and tasks."""

    GRID_SIZE = 11
    X_SIZE = 7
    OFFSET = (GRID_SIZE - X_SIZE) // 2

    @staticmethod
    def clear_grid():
        """Clears all Polyanets from the grid."""
        print("Clearing grid...")
        for row in range(MegaverseController.GRID_SIZE):
            for column in range(MegaverseController.GRID_SIZE):
                success = MegaverseAPI.delete_polyanet(row, column)
                if success:
                    print(f"Deleted Polyanet at ({row}, {column}).")
                else:
                    print(f"Failed to delete Polyanet at ({row}, {column}).")

    @staticmethod
    def draw_x():
        """Draws a centered 7x7 'X' pattern on the grid with Polyanets."""
        print("Drawing centered 'X'...")
        for row in range(MegaverseController.OFFSET, MegaverseController.OFFSET + MegaverseController.X_SIZE):
            for column in range(MegaverseController.OFFSET, MegaverseController.OFFSET + MegaverseController.X_SIZE):
                # Draw on diagonals of the 7x7 sub-grid
                if row - MegaverseController.OFFSET == column - MegaverseController.OFFSET or \
                        row - MegaverseController.OFFSET + column - MegaverseController.OFFSET == MegaverseController.X_SIZE - 1:
                    success = MegaverseAPI.create_polyanet(row, column)
                    if success:
                        print(f"Created Polyanet at ({row}, {column}).")
                    else:
                        print(f"Failed to create Polyanet at ({row}, {column}).")

    @staticmethod
    def build_logo():
        """Build the Crossmint logo using the API response."""
        print("Fetching the goal map...")
        goal_map = MegaverseAPI.get_goal_map()  # Fetch the response from the /goal API

        if not goal_map or "goal" not in goal_map:
            print("Failed to retrieve the goal map.")
            return

        print("Building the logo...")
        for row_index, row in enumerate(goal_map["goal"]):
            for col_index, cell in enumerate(row):
                if cell == "POLYANET":
                    # Place a Polyanet
                    MegaverseController._place_object(MegaverseAPI.create_polyanet, row_index, col_index)
                elif "SOLOON" in cell:
                    # Handle Soloons: Extract color from the cell
                    color = cell.split("_")[0].lower()  # Color comes first
                    MegaverseController._place_object(
                        lambda r, c: MegaverseAPI.create_soloon(r, c, color),
                        row_index,
                        col_index
                    )
                elif "COMETH" in cell:
                    # Handle Comeths: Extract direction from the cell
                    direction = cell.split("_")[0].lower()  # Direction comes first
                    MegaverseController._place_object(
                        lambda r, c: MegaverseAPI.create_cometh(r, c, direction),
                        row_index,
                        col_index
                    )

        print("Logo built successfully!")

    @staticmethod
    def _place_object(create_function, row, column):
        """Place an object and handle rate limits."""
        success = create_function(row, column)
        if not success:
            print(f"Rate limit hit. Retrying for ({row}, {column})...")
            time.sleep(1)  # Wait before retrying
            create_function(row, column)
        else:
            time.sleep(0.1)  # Small delay to prevent hitting rate limits
