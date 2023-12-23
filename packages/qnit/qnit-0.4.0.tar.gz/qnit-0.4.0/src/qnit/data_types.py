from typing import Union

import numpy as np
import numpy.typing as npt
import pint.facets

# Type aliases
# We explicitly narrow down pint's internal Scalar and Magnitude types
# to be typing-compatible with numpy
ScalarMagnitude = Union[float, int, np.number]
ArrayMagnitude = npt.NDArray[np.number]
Magnitude = Union[ScalarMagnitude, ArrayMagnitude]
PintQuantity = pint.facets.plain.quantity.PlainQuantity
