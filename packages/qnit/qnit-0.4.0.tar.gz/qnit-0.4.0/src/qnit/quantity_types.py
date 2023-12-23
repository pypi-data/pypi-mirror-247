"""
Module with predefined quantity types
"""

import dataclasses

from dataclasses import dataclass
from typing import Type, Generic, Optional

from . import unit_collections, unit_types, errors
from .unit_types import UnitsT


@dataclass(frozen=True)
class QuantityType(Generic[UnitsT]):
    """
    Class for meta information of a quantity.
    Implemented as dataclass for simple definition of child-classes.
    """

    # Type of the units e.g., unit_types.EnergyUnit
    units_type: Type[UnitsT]
    # The internal units e.g., unit_collection.Energy.J
    internal_units: UnitsT
    # Collection of available units e.g., unit_collections.Energy()
    available_units: unit_collections.UnitCollection
    # Default display units e.g., unit_collection.Energy.MWh
    default_display_units: Optional[UnitsT] = None

    def __post_init__(self):
        """
        Check the compatibility of the given units
        """
        # Check if type of internal units matches the declared unit type
        if not isinstance(self.internal_units, self.units_type):
            msg = (
                f"Type of internal_units ({type(self.internal_units)}) "
                f"does not match the specified unit type ({self.units_type})"
            )
            raise errors.QuantityUnitsError(msg)

        # Check if type of display units matches the declared unit type
        if self.default_display_units is not None:
            if not isinstance(self.default_display_units, self.units_type):
                msg = (
                    "Type of default_display_units "
                    f"({type(self.default_display_units)}) "
                    f"does not match the specified unit type ({self.units_type})"
                )
                raise errors.QuantityUnitsError(msg)

        # Check if type of all fields of the units collection
        # match the declared unit type
        for units_field in dataclasses.fields(self.available_units):
            field_object = getattr(self.available_units, units_field.name)
            if not isinstance(field_object, self.units_type):
                msg = (
                    f"The type ({type(field_object)}) "
                    f" of the field '{units_field.name}' (and maybe others)"
                    f" from the available_units ({self.available_units})"
                    f" do not match the specified unit type ({self.units_type})"
                )
                raise errors.QuantityUnitsError(msg)


Acceleration = QuantityType(
    units_type=unit_types.AccelerationUnit,
    internal_units=unit_collections.Acceleration.m_per_s2,
    default_display_units=unit_collections.Acceleration.m_per_s2,
    available_units=unit_collections.Acceleration(),
)


Angle = QuantityType(
    units_type=unit_types.AngleUnit,
    internal_units=unit_collections.Angle.rad,
    default_display_units=unit_collections.Angle.deg,
    available_units=unit_collections.Angle(),
)


Area = QuantityType(
    units_type=unit_types.AreaUnit,
    internal_units=unit_collections.Area.m2,
    default_display_units=unit_collections.Area.m2,
    available_units=unit_collections.Area(),
)


Currency = QuantityType(
    units_type=unit_types.CurrencyUnit,
    internal_units=unit_collections.Currency.EUR,
    default_display_units=unit_collections.Currency.EUR,
    available_units=unit_collections.Currency(),
)


Current = QuantityType(
    units_type=unit_types.CurrentUnit,
    internal_units=unit_collections.Current.A,
    default_display_units=unit_collections.Current.A,
    available_units=unit_collections.Current(),
)


Density = QuantityType(
    units_type=unit_types.DensityUnit,
    internal_units=unit_collections.Density.kg_per_m3,
    default_display_units=unit_collections.Density.kg_per_m3,
    available_units=unit_collections.Density(),
)


DurationShare = QuantityType(
    units_type=unit_types.NoUnit,
    internal_units=unit_collections.DurationShare.h_per_a,
    default_display_units=unit_collections.DurationShare.h_per_a,
    available_units=unit_collections.DurationShare(),
)


DynamicViscosity = QuantityType(
    units_type=unit_types.DynamicViscosityUnit,
    internal_units=unit_collections.DynamicViscosity.Pa_s,
    default_display_units=unit_collections.DynamicViscosity.Pa_s,
    available_units=unit_collections.DynamicViscosity(),
)


Energy = QuantityType(
    units_type=unit_types.EnergyUnit,
    internal_units=unit_collections.Energy.J,
    default_display_units=unit_collections.Energy.MWh,
    available_units=unit_collections.Energy(),
)


EnergyCosts = QuantityType(
    units_type=unit_types.EnergyCostsUnit,
    internal_units=unit_collections.EnergyCosts.EUR_per_MWh,
    default_display_units=unit_collections.EnergyCosts.EUR_per_MWh,
    available_units=unit_collections.EnergyCosts(),
)


EnergyInDuration = QuantityType(
    units_type=unit_types.PowerUnit,
    internal_units=unit_collections.EnergyInDuration.MWh_per_a,
    default_display_units=unit_collections.EnergyInDuration.MWh_per_a,
    available_units=unit_collections.EnergyInDuration(),
)


Frequency = QuantityType(
    units_type=unit_types.FrequencyUnit,
    internal_units=unit_collections.Frequency.Hz,
    default_display_units=unit_collections.Frequency.Hz,
    available_units=unit_collections.Frequency(),
)


GeothermalProdIndex = QuantityType(
    units_type=unit_types.GeothermalProdIndexUnit,
    internal_units=unit_collections.GeothermalProdIndex.m3_per_s_Pa,
    default_display_units=unit_collections.GeothermalProdIndex.m3_per_s_Pa,
    available_units=unit_collections.GeothermalProdIndex(),
)


HeatCapacityRate = QuantityType(
    units_type=unit_types.HeatCapacityRateUnit,
    internal_units=unit_collections.HeatCapacityRate.W_per_K,
    default_display_units=unit_collections.HeatCapacityRate.W_per_K,
    available_units=unit_collections.HeatCapacityRate(),
)


HeatTransferCoefficient = QuantityType(
    units_type=unit_types.HeatTransferCoefficientUnit,
    internal_units=unit_collections.HeatTransferCoefficient.W_per_m2_K,
    default_display_units=unit_collections.HeatTransferCoefficient.W_per_m2_K,
    available_units=unit_collections.HeatTransferCoefficient(),
)


HourlyCosts = QuantityType(
    units_type=unit_types.HourlyCostsUnit,
    internal_units=unit_collections.HourlyCosts.EUR_per_h,
    default_display_units=unit_collections.HourlyCosts.EUR_per_h,
    available_units=unit_collections.HourlyCosts(),
)


Irradiance = QuantityType(
    units_type=unit_types.HeatTransferCoefficientUnit,
    internal_units=(
        unit_collections.QuadraticHeatTransferCoefficient.W_per_m2_K2
    ),
    default_display_units=(
        unit_collections.QuadraticHeatTransferCoefficient.W_per_m2_K2
    ),
    available_units=unit_collections.QuadraticHeatTransferCoefficient(),
)


KinematicViscosity = QuantityType(
    units_type=unit_types.KinematicViscosityUnit,
    internal_units=unit_collections.KinematicViscosity.m2_per_s,
    default_display_units=unit_collections.KinematicViscosity.m2_per_s,
    available_units=unit_collections.KinematicViscosity(),
)


Length = QuantityType(
    units_type=unit_types.LengthUnit,
    internal_units=unit_collections.Length.m,
    default_display_units=unit_collections.Length.m,
    available_units=unit_collections.Length(),
)


LinearPressure = QuantityType(
    units_type=unit_types.PressureUnit,
    internal_units=unit_collections.LinearPressure.Pa_s_per_l,
    default_display_units=unit_collections.LinearPressure.Pa_s_per_l,
    available_units=unit_collections.LinearPressure(),
)


Mass = QuantityType(
    units_type=unit_types.MassUnit,
    internal_units=unit_collections.Mass.kg,
    default_display_units=unit_collections.Mass.kg,
    available_units=unit_collections.Mass(),
)


NoUnit = QuantityType(
    units_type=unit_types.NoUnit,
    internal_units=unit_collections.NoUnit.No,
    default_display_units=unit_collections.NoUnit.No,
    available_units=unit_collections.NoUnit(),
)


Power = QuantityType(
    units_type=unit_types.PowerUnit,
    internal_units=unit_collections.Power.W,
    default_display_units=unit_collections.Power.kW,
    available_units=unit_collections.Power(),
)


PowerAreaRatio = QuantityType(
    units_type=unit_types.PowerAreaRatioUnit,
    internal_units=unit_collections.PowerAreaRatio.W_per_m2,
    default_display_units=unit_collections.PowerAreaRatio.W_per_m2,
    available_units=unit_collections.PowerAreaRatio(),
)


Pressure = QuantityType(
    units_type=unit_types.PressureUnit,
    internal_units=unit_collections.Pressure.Pa,
    default_display_units=unit_collections.Pressure.bar,
    available_units=unit_collections.Pressure(),
)


QuadraticPressure = QuantityType(
    units_type=unit_types.PressureUnit,
    internal_units=unit_collections.QuadraticPressure.Pa_s2_per_l2,
    default_display_units=unit_collections.QuadraticPressure.Pa_s2_per_l2,
    available_units=unit_collections.QuadraticPressure(),
)


ShareInPeriod = QuantityType(
    units_type=unit_types.FrequencyUnit,
    internal_units=unit_collections.ShareInPeriod.share_per_a,
    default_display_units=unit_collections.ShareInPeriod.share_per_a,
    available_units=unit_collections.ShareInPeriod(),
)


SpecificHeatCapacity = QuantityType(
    units_type=unit_types.SpecificHeatCapacityUnit,
    internal_units=unit_collections.SpecificHeatCapacity.J_per_kg_K,
    default_display_units=unit_collections.SpecificHeatCapacity.J_per_kg_K,
    available_units=unit_collections.SpecificHeatCapacity(),
)


Temperature = QuantityType(
    units_type=unit_types.TemperatureUnit,
    internal_units=unit_collections.Temperature.K,
    default_display_units=unit_collections.Temperature.deg_C,
    available_units=unit_collections.Temperature(),
)


TemperatureCorrection = QuantityType(
    units_type=unit_types.TemperatureCorrectionUnit,
    internal_units=unit_collections.TemperatureCorrection.inverse_K,
    default_display_units=unit_collections.TemperatureCorrection.inverse_K,
    available_units=unit_collections.TemperatureCorrection(),
)


TemperatureDifference = QuantityType(
    units_type=unit_types.TemperatureDifferenceUnit,
    internal_units=unit_collections.TemperatureDifference.delta_deg_C,
    default_display_units=unit_collections.TemperatureDifference.delta_deg_C,
    available_units=unit_collections.TemperatureDifference(),
)


ThermalConductivity = QuantityType(
    units_type=unit_types.ThermalConductivityUnit,
    internal_units=unit_collections.ThermalConductivity.W_per_m_K,
    default_display_units=unit_collections.ThermalConductivity.W_per_m_K,
    available_units=unit_collections.ThermalConductivity(),
)


Time = QuantityType(
    units_type=unit_types.TimeUnit,
    internal_units=unit_collections.Time.s,
    default_display_units=unit_collections.Time.h,
    available_units=unit_collections.Time(),
)


Velocity = QuantityType(
    units_type=unit_types.VelocityUnit,
    internal_units=unit_collections.Velocity.m_per_s,
    default_display_units=unit_collections.Velocity.m_per_s,
    available_units=unit_collections.Velocity(),
)


Volume = QuantityType(
    units_type=unit_types.VolumeUnit,
    internal_units=unit_collections.Volume.m3,
    default_display_units=unit_collections.Volume.m3,
    available_units=unit_collections.Volume(),
)


VolumeFlow = QuantityType(
    units_type=unit_types.VolumeFlowUnit,
    internal_units=unit_collections.VolumeFlow.m3_per_h,
    default_display_units=unit_collections.VolumeFlow.l_per_min,
    available_units=unit_collections.VolumeFlow(),
)
