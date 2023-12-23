import dataclasses
import importlib.resources
import typing
import warnings
from typing import Generic, Optional, Union, TypeVar

import numpy as np
import numpy.typing as npt
import pint
import pint.facets
import pint_pandas

from . import errors
from .data_types import (
    Magnitude,
    PintQuantity as PintQuantityType,
)
from .quantity_types import QuantityType
from .unit_types import UnitsT


# Global Pint UnitRegistry, settings and classes
UNITS_DEFINITIONS_FILE = importlib.resources.files(__package__).joinpath(
    "pint_units.txt"
)
ureg = pint.UnitRegistry(
    default_as_delta=True,
    autoconvert_offset_to_baseunit=True,
    auto_reduce_dimensions=True,
    system="SI",
    cache_folder=":auto:",
)
with importlib.resources.as_file(UNITS_DEFINITIONS_FILE) as def_path:
    ureg.load_definitions(def_path)
pint_pandas.PintType.ureg = ureg  # Use global UnitsRegistry for new instances
ureg.default_format = "~"  # Short, not pretty (e.g. '1.5e-3 m ** 2')
PintQuantity = ureg.Quantity


class Quantity(Generic[UnitsT]):
    """
    A units and type-aware physical quantity
    """

    CAST_TYPE = float

    @classmethod
    def as_dataclass_field(
        cls,
        quantity_type: QuantityType,
        description: str = "",
        magnitude: Optional[Magnitude] = None,
        units: Optional[UnitsT] = None,
    ):
        """
        Return a dataclasses field with a default.
        Use this instead of passing objects of this class or initializing it in field defaults directly.
        If the normal constructor (__init__) is used for a default value inside a dataclass,
        the identical object is referred in all instances of the dataclass.
        For parameter descriptions, see Quantity.__init__.
        :return: The dataclass field
        """
        return dataclasses.field(
            default_factory=lambda: cls(
                quantity_type=quantity_type,
                description=description,
                magnitude=magnitude,
                units=units,
            )
        )

    def __init__(
        self,
        quantity_type: QuantityType[UnitsT],
        description: str = "",
        magnitude: Optional[Magnitude] = None,
        units: Optional[UnitsT] = None,
    ):
        """
        :param quantity_type: Type of the quantity e.g., 'Power'.
        :param description: Description of the quantity.
        :param magnitude: Preset magnitude of the quantity.
            Must be given together with units.
        :param units: Preset units of the quantity.
            Must be given together with magnitude.
        """
        self._quantity: Optional[PintQuantityType] = None
        self.quantityType: QuantityType = quantity_type
        self.description: str = description

        # Try initializing the value with given defaults
        if (magnitude is not None) or (units is not None):
            if (magnitude is not None) and (units is not None):
                self.set(magnitude=magnitude, units=units)
            else:
                msg = (
                    f"To set a default value for Quantity, you must give"
                    f" BOTH value and units."
                )
                warnings.warn(msg)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"quantity_type={self.quantityType}, "
            f"description={self.description}, "
        )

    @property
    def pint_quantity(self) -> PintQuantityType:
        """
        Getter for the quantity
        :return: The quantity
        """
        if self._quantity is None:
            msg = (
                f"Value of this quantity is accessed before it "
                f"was set."
            )
            raise errors.QuantityValueError(msg)
        return self._quantity

    @pint_quantity.setter
    def pint_quantity(self, quantity_: PintQuantityType):
        """
        Set the quantity.
        Check for units compatibility.
        :param quantity_: The quantity to set
        """
        # Check if the quantity's magnitude can be casted to float
        if np.isscalar(quantity_.magnitude):
            d_type = type(quantity_.magnitude)
        else:
            d_type = quantity_.magnitude.dtype
        if np.can_cast(d_type, self.CAST_TYPE) is False:
            msg = (
                f"Data type of the quantity magnitude ({repr(quantity_)},"
                f" {d_type}) is not numerical."
            )
            raise errors.QuantityValueError(msg)

        try:
            # Convert to internal unit
            self._quantity = quantity_.to(self.quantityType.internal_units)
        except pint.errors.DimensionalityError as err:
            msg = (
                f"Unit of the given quantity ('{err.units1}' {err.dim1}) "
                "does not fit to the predefined quantity unit "
                f"('{err.units2}' {err.dim2})."
            )
            raise errors.QuantityUnitsError(msg)

    def set(self, magnitude: Magnitude, units: UnitsT):
        """
        Set a quantity value by declaring magnitude and units
        :param magnitude: Magnitude of the quantity
        :param units: Units of the quantity
        """
        try:
            self.pint_quantity = PintQuantity(magnitude, units)
        except TypeError as e:
            raise errors.QuantityValueError(e)

    @property
    def magnitude_is_scalar(self) -> bool:
        """
        True, if the underlying pint Quantity's magnitude is scalar.
        False, if either the latter is not scalar or the Quantity is None.
        """
        if self.pint_quantity is not None:
            return np.isscalar(self.pint_quantity.m)
        else:
            return False

    def magnitude(self, units: UnitsT) -> Magnitude:
        """
        Return the magnitude of the quantity in given units
        :param units: Units in which the magnitude should be returned.
            If None, the default unit will be used.
        :return: Magnitude of the quantity
        """
        if self.pint_quantity is not None:
            try:
                magnitude = self.pint_quantity.m_as(units=units)
            except pint.errors.DimensionalityError as err:
                msg = (
                    f"Demanded unit ('{err.units2}'{err.dim2}) "
                    "does not fit to the predefined quantity units "
                    f"('{err.units1}'{err.dim1})."
                )
                raise errors.QuantityUnitsError(msg)
        else:
            magnitude = self.pint_quantity
        return magnitude

    @property
    def internal_magnitude(self) -> Magnitude:
        """
        Return the magnitude of the quantity as internal units.
        """
        return self.magnitude(units=self.quantityType.internal_units)

    @property
    def display_magnitude(self) -> Magnitude:
        """
        Return the magnitude of the quantity as default display units.
        If the quantity type does not define default display units,
        the magnitude is returned as internal units.
        """
        if self.quantityType.default_display_units is None:
            display_magnitude = self.internal_magnitude
        else:
            display_magnitude = self.magnitude(
                units=self.quantityType.default_display_units
            )
        return display_magnitude


ParamDataT = TypeVar("ParamDataT", bound=Union[int, float, bool, str, bytes, np.generic])


class Parameter(Generic[ParamDataT, UnitsT]):
    """
    A parameter with either a unit-naive basic value or a unit-aware quantity value
    """

    @classmethod
    def as_dataclass_field(
        cls,
        data_type: type[ParamDataT],
        quantity_type: Optional[QuantityType[UnitsT]] = None,
        description: str = "",
        value: Union[ParamDataT, npt.NDArray, Quantity[UnitsT], None] = None,
        value_comment: str = ""
    ):
        """
        Return a dataclasses field with a default.
        Use this instead of passing objects of this class or initializing it in field defaults directly.
        If the normal constructor (__init__) is used for a default value inside a dataclass,
        the identical object is referred in all instances of the dataclass.
        For parameter descriptions, see Parameter.__init__.
        :return: The dataclass field
        """
        return dataclasses.field(
            default_factory=lambda: cls(
                data_type=data_type,
                quantity_type=quantity_type,
                description=description,
                value=value,
                value_comment=value_comment,
            )
        )

    def __init__(
        self,
        data_type: type[ParamDataT],
        quantity_type: Optional[QuantityType[UnitsT]] = None,
        description: str = "",
        value: Union[ParamDataT, npt.NDArray, Quantity[UnitsT], None] = None,
        value_comment: str = ""
    ):
        """
        :param data_type: Data type of the parameter
        :param quantity_type: Type of the parameter's quantity e.g., 'Power'.
            A given quantity type's data type will override the given data type.
        :param description: Description of the parameter
        :param value: Preset value for the parameter
        :param value_comment: Comment for the given parameter value
            (e.g. a reference)
        """
        self.dataType: type[ParamDataT] = data_type
        self.quantityType: Optional[QuantityType] = quantity_type
        self.description: str = description

        # The value of a units-aware parameter
        self._quantity: Optional[Quantity[UnitsT]]
        if quantity_type is None:
            self._quantity = None
        else:
            self._quantity = Quantity(quantity_type=quantity_type)

        # The value of a units-naive parameter
        self._naive_value: Optional[ParamDataT] = None

        if value is not None:
            self.value = value
            self.valueComment: str = value_comment

    @property
    def is_units_naive(self) -> bool:
        return self.quantityType is None

    @property
    def is_units_aware(self) -> bool:
        return not self.is_units_naive

    @property
    def value(self) -> Union[ParamDataT, npt.NDArray, Quantity[UnitsT], None]:
        """
        Return the parameter value, i.e.
        a units-naive value in case of a units-naive parameter or
        a pint quantity in case of a units-aware parameter
        :return: The parameter value
        """
        if self.is_units_aware:
            return self.quantity
        else:
            return self._naive_value

    @value.setter
    def value(self, value_: Union[ParamDataT, npt.NDArray, Quantity[UnitsT], None]):
        """
        Set the parameter value, i.e.
        a units-naive value in case of a units-naive parameter or
        a pint quantity in case of a units-aware parameter
        :param value_: The parameter value
        """
        if self.is_units_naive:
            # Allow setting to None
            if value_ is None:
                self._naive_value = value_
            else:
                if not isinstance(value_, self.dataType):
                    msg = (
                        f"Cannot set {repr(value_)} as parameter value"
                        f" as it is not an instance of {self.dataType}."
                    )
                    raise errors.ParameterValueError(msg)
                self._naive_value = value_
        else:
            if not isinstance(value_, Quantity):
                msg = (
                    f"Cannot set {repr(value_)} as value for units-aware"
                    " parameter. Please give a Quantity as value."
                )
                raise errors.ParameterValueError(msg)
            self.quantity = value_

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"data_type={self.dataType}, "
            f"quantity_type={self.quantityType}, "
            f"description={self.description}"
            f")"
        )

    def _raise_on_units_naive_quantity(self):
        """
        Raise an exception if a quantity of a units-naive parameter
        is being accessed
        """
        if self.is_units_naive:
            err_msg = (
                "Cannot access quantity of units-naive parameter."
                " Please use Parameter.value."
            )
            raise errors.ParameterValueError(err_msg)

    @property
    def quantity(self) -> Quantity[UnitsT]:
        """
        Return the quantity value (if the parameter is units-aware)
        :return: The quantity
        """
        self._raise_on_units_naive_quantity()
        assert self._quantity is not None
        return self._quantity

    @quantity.setter
    def quantity(self, quantity_: Quantity[UnitsT]):
        """
        Set the quantity value (if the parameter is units-aware)
        """
        self._raise_on_units_naive_quantity()
        self._quantity = quantity_

    @property
    def pint_quantity(self) -> Optional[PintQuantityType]:
        """
        Return the underlying pint quantity value (if the parameter is units-aware)
        :return: The pint quantity
        """
        return self.quantity.pint_quantity

    @pint_quantity.setter
    def pint_quantity(self, quantity_: PintQuantityType):
        """
        Set the underlying pint quantity value (if the parameter is units-aware)
        """
        self.quantity.pint_quantity = quantity_

    def _raise_on_units_naive_quantity_set(self):
        """
        Raise an exception if a quantity of a units-naive parameter
        is trying to be set
        """
        if self.is_units_naive:
            err_msg = (
                "Cannot set magnitude and units of units-naive parameter."
                " Please use Parameter.value.setter."
            )
            raise errors.ParameterValueError(err_msg)

    def set_magnitude_units(
        self,
        magnitude: Union[ParamDataT, npt.NDArray],
        units: UnitsT,
        value_comment: Optional[str] = None,
    ):
        """
        Set the parameter's quantity value by declaring magnitude and units
        :param magnitude: Magnitude to be set
        :param units: Units for the magnitude
        :param value_comment: Comment for the quantity value (e.g. a reference)
        """
        self._raise_on_units_naive_quantity_set()
        magnitude_ = typing.cast(Magnitude, magnitude)
        self.quantity.set(magnitude=magnitude_, units=units)
        if value_comment is not None:
            self.valueComment = value_comment

    def _raise_on_units_naive_magnitude(self):
        """
        Raise an exception if a magnitude property of a units-naive parameter
        is being accessed
        """
        if self.is_units_naive:
            err_msg = (
                "Cannot get magnitude of units-naive parameter."
                " Please use Parameter.value."
            )
            raise errors.ParameterValueError(err_msg)

    def magnitude(self, units: UnitsT) -> ParamDataT:
        """
        Return the magnitude of a units-aware parameter,
        converted to given units.
        :param units: Units in which the quantity magnitude should be returned
        :return: Magnitude of the parameter
        """
        self._raise_on_units_naive_magnitude()
        magnitude = self.quantity.magnitude(units=units)
        return typing.cast(ParamDataT, magnitude)

    @property
    def internal_magnitude(self) -> ParamDataT:
        """
        Return the magnitude of a units-aware parameter,
        converted to internal units.
        """
        self._raise_on_units_naive_magnitude()
        magnitude = self.quantity.internal_magnitude
        return typing.cast(ParamDataT, magnitude)

    @property
    def display_magnitude(self) -> ParamDataT:
        """
        Return the magnitude of a units-aware parameter,
        converted to display units.
        """
        self._raise_on_units_naive_magnitude()
        magnitude = self.quantity.display_magnitude
        return typing.cast(ParamDataT, magnitude)
