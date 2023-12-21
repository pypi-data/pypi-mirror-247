import numpy as np
import torch


class Polygon:
    """Class for computing properties of a polygon given its vertices as 2D coordinates.

    Attributes:
        vertices (torch.Tensor): A tensor of shape (N, 2), where N is the number of vertices in the polygon.
             Each row contains the x, y coordinate a pair of one vertex.
        _Signed_areas (torch.Tensor or None): Cached signed areas of each triangle formed by consecutive vertices.
                          If not computed yet, it will be calculated on demand when accessing `area`.
        _Length (float or None): Cached total edge length of the polygon. If not computed yet, it will be calculated
                           on demand when accessing `length`.

    """

    def __init__(self, vertices: torch.Tensor):
        """Initializes the Polygon object with the given 2D coordinates.

        Args:
            vertices (torch.Tensor): A tensor of shape (N, 2), where N is the number of vertices in the polygon.
                Each row contains the x, y coordinate a pair of one vertex.

        Raises:
            TypeError: If `vertices` is not a tensor.
            ValueError: If `vertices` has more than two dimensions or does not have exactly two columns per row.

        """
        if torch.is_tensor(obj=vertices):
            self.vertices = vertices
        elif isinstance(vertices, (list, np.ndarray)):
            self.vertices = torch.tensor(data=vertices, dtype=torch.float32)
        else:
            raise TypeError(
                "Coordinates must be provided as a Python list, PyTorch Tensor, or numpy array."
            )

        if len(vertices.shape) > 2:
            raise ValueError("Coordinates cannot have more than two dimensions")

        if vertices.shape[-1] != 2:
            raise ValueError(
                "Each row of coordinates should contain exactly two elements representing x and y"
            )

        self._validate_vertices(vertices=self.vertices)
        self._signed_areas = None
        self._length = None

    @staticmethod
    def _validate_vertices(vertices):
        """Validates that the input coordinates are appropriate for this class."""
        if vertices.shape[1] != 2:
            raise ValueError(
                "Expected 2D coordinates. Coordinate arrays should have shape (N, 2)"
            )

    def _calculate_signed_areas(self):
        """Computes the signed area of each triangle formed by consecutive vertices."""
        self._signed_areas = (
                torch.det(
                    input=torch.stack(
                        tensors=[
                            self.vertices[1:] - self.vertices[0],
                            self.vertices[:-1] - self.vertices[0],
                        ],
                        dim=2,
                    )
                )
                / 2
        )

    def _calculate_length(self):
        """Calculates the total edge length of the polygon."""
        diff_x = torch.roll(self.vertices[:, 0], shifts=-1) - self.vertices[:, 0]
        diff_y = torch.roll(self.vertices[:, 1], shifts=-1) - self.vertices[:, 1]
        self._length = torch.sqrt(diff_x ** 2 + diff_y ** 2).sum()

    @property
    def area(self):
        """Total area of the polygon.
        Returns:
            float: The total area of the polygon.

        """
        if self._signed_areas is None:
            self._calculate_signed_areas()
        return self._signed_areas.sum()

    @property
    def length(self):
        """Total edge length of the polygon.
        Returns:
            float: The length (perimeter) of the polygon.

        """
        if self._length is None:
            self._calculate_length()
        return self._length
