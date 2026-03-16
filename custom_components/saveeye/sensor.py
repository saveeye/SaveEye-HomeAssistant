from __future__ import annotations

from collections.abc import Callable
from typing import Any, Dict, Optional, Union

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfElectricCurrent, UnitOfElectricPotential, UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo

from .const import DATA_KEY_COORDINATOR, DOMAIN
from . import SaveEyeCoordinator


class SaveEyeSensorDescription:
    def __init__(
        self,
        key: str,
        name: str,
        json_path: tuple[Union[str, int], ...],
        device_class: Optional[SensorDeviceClass],
        state_class: Optional[SensorStateClass],
        unit: Optional[str],
        device_identifier_suffix: str,
        value_transform: Optional[Callable[[Any], Optional[float | int | str]]] = None,
    ) -> None:
        self.key = key
        self.name = name
        self.json_path = json_path
        self.device_class = device_class
        self.state_class = state_class
        self.unit = unit
        self.device_identifier_suffix = device_identifier_suffix
        self.value_transform = value_transform


SENSORS: list[SaveEyeSensorDescription] = [
    # Core identifiers and metadata
    SaveEyeSensorDescription(
        key="deviceSerialNumber",
        name="Device Serial Number",
        json_path=("saveeyeDeviceSerialNumber",),
        device_class=SensorDeviceClass.ENUM,
        state_class=None,
        unit=None,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="meterType",
        name="Meter Type",
        json_path=("meterType",),
        device_class=SensorDeviceClass.ENUM,
        state_class=None,
        unit=None,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="meterSerialNumber",
        name="Meter Serial Number",
        json_path=("meterSerialNumber",),
        device_class=SensorDeviceClass.ENUM,
        state_class=None,
        unit=None,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="deviceTime",
        name="Device Time",
        json_path=("timestamp",),
        device_class=None,
        state_class=None,
        unit=None,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="wifiRssi",
        name="WiFi Signal Strength",
        json_path=("wifiRssi",),
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        unit="dBm",
        device_identifier_suffix="general",
    ),
    # Cumulative active energy consumption/production
    SaveEyeSensorDescription(
        key="activeTotalConsumption_total",
        name="Active Cumulative Energy Consumption (All lines)",
        json_path=("activeTotalConsumption", "total"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeTotalConsumption_L1",
        name="Active Cumulative Energy Consumption L1",
        json_path=("activeTotalConsumption", "L1"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeTotalConsumption_L2",
        name="Active Cumulative Energy Consumption L2",
        json_path=("activeTotalConsumption", "L2"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeTotalConsumption_L3",
        name="Active Cumulative Energy Consumption L3",
        json_path=("activeTotalConsumption", "L3"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeTotalProduction_total",
        name="Active Cumulative Energy Production (All lines)",
        json_path=("activeTotalProduction", "total"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeTotalProduction_L1",
        name="Active Cumulative Energy Production L1",
        json_path=("activeTotalProduction", "L1"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeTotalProduction_L2",
        name="Active Cumulative Energy Production L2",
        json_path=("activeTotalProduction", "L2"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeTotalProduction_L3",
        name="Active Cumulative Energy Production L3",
        json_path=("activeTotalProduction", "L3"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    # Cumulative reactive energy consumption/production
    SaveEyeSensorDescription(
        key="reactiveTotalConsumption_total",
        name="Reactive Cumulative Energy Consumption (All lines)",
        json_path=("reactiveTotalConsumption", "total"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveTotalConsumption_L1",
        name="Reactive Cumulative Energy Consumption L1",
        json_path=("reactiveTotalConsumption", "L1"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveTotalConsumption_L2",
        name="Reactive Cumulative Energy Consumption L2",
        json_path=("reactiveTotalConsumption", "L2"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveTotalConsumption_L3",
        name="Reactive Cumulative Energy Consumption L3",
        json_path=("reactiveTotalConsumption", "L3"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveTotalProduction_total",
        name="Reactive Cumulative Energy Production (All lines)",
        json_path=("reactiveTotalProduction", "total"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveTotalProduction_L1",
        name="Reactive Cumulative Energy Production L1",
        json_path=("reactiveTotalProduction", "L1"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveTotalProduction_L2",
        name="Reactive Cumulative Energy Production L2",
        json_path=("reactiveTotalProduction", "L2"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveTotalProduction_L3",
        name="Reactive Cumulative Energy Production L3",
        json_path=("reactiveTotalProduction", "L3"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.WATT_HOUR,
        device_identifier_suffix="general",
    ),
    # Active power consumption/production
    SaveEyeSensorDescription(
        key="activeActualConsumption_total",
        name="Active Consumption (All lines)",
        json_path=("activeActualConsumption", "total"),
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfPower.WATT,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeActualConsumption_L1",
        name="Active Consumption L1",
        json_path=("activeActualConsumption", "L1"),
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfPower.WATT,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeActualConsumption_L2",
        name="Active Consumption L2",
        json_path=("activeActualConsumption", "L2"),
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfPower.WATT,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeActualConsumption_L3",
        name="Active Consumption L3",
        json_path=("activeActualConsumption", "L3"),
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfPower.WATT,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeActualProduction_total",
        name="Active Production (All lines)",
        json_path=("activeActualProduction", "total"),
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfPower.WATT,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeActualProduction_L1",
        name="Active Production L1",
        json_path=("activeActualProduction", "L1"),
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfPower.WATT,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeActualProduction_L2",
        name="Active Production L2",
        json_path=("activeActualProduction", "L2"),
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfPower.WATT,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="activeActualProduction_L3",
        name="Active Production L3",
        json_path=("activeActualProduction", "L3"),
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfPower.WATT,
        device_identifier_suffix="general",
    ),
    # Reactive power consumption/production
    SaveEyeSensorDescription(
        key="reactiveActualConsumption_total",
        name="Reactive Consumption (All lines)",
        json_path=("reactiveActualConsumption", "total"),
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit="var",
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveActualConsumption_L1",
        name="Reactive Consumption L1",
        json_path=("reactiveActualConsumption", "L1"),
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit="var",
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveActualConsumption_L2",
        name="Reactive Consumption L2",
        json_path=("reactiveActualConsumption", "L2"),
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit="var",
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveActualConsumption_L3",
        name="Reactive Consumption L3",
        json_path=("reactiveActualConsumption", "L3"),
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit="var",
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveActualProduction_total",
        name="Reactive Production (All lines)",
        json_path=("reactiveActualProduction", "total"),
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit="var",
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveActualProduction_L1",
        name="Reactive Production L1",
        json_path=("reactiveActualProduction", "L1"),
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit="var",
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveActualProduction_L2",
        name="Reactive Production L2",
        json_path=("reactiveActualProduction", "L2"),
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit="var",
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="reactiveActualProduction_L3",
        name="Reactive Production L3",
        json_path=("reactiveActualProduction", "L3"),
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit="var",
        device_identifier_suffix="general",
    ),
    # RMS Voltage
    SaveEyeSensorDescription(
        key="rmsVoltage_L1",
        name="L1 Voltage",
        json_path=("rmsVoltage", "L1"),
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfElectricPotential.VOLT,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="rmsVoltage_L2",
        name="L2 Voltage",
        json_path=("rmsVoltage", "L2"),
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfElectricPotential.VOLT,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="rmsVoltage_L3",
        name="L3 Voltage",
        json_path=("rmsVoltage", "L3"),
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfElectricPotential.VOLT,
        device_identifier_suffix="general",
    ),
    # RMS Current
    SaveEyeSensorDescription(
        key="rmsCurrent_L1",
        name="L1 Current",
        json_path=("rmsCurrent", "L1"),
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfElectricCurrent.MILLIAMPERE,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="rmsCurrent_L2",
        name="L2 Current",
        json_path=("rmsCurrent", "L2"),
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfElectricCurrent.MILLIAMPERE,
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="rmsCurrent_L3",
        name="L3 Current",
        json_path=("rmsCurrent", "L3"),
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfElectricCurrent.MILLIAMPERE,
        device_identifier_suffix="general",
    ),
    # Power factor
    SaveEyeSensorDescription(
        key="powerFactor_total",
        name="Total Power Factor",
        json_path=("powerFactor", "total"),
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        unit="%",
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="powerFactor_L1",
        name="L1 Power Factor",
        json_path=("powerFactor", "L1"),
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        unit="%",
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="powerFactor_L2",
        name="L2 Power Factor",
        json_path=("powerFactor", "L2"),
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        unit="%",
        device_identifier_suffix="general",
    ),
    SaveEyeSensorDescription(
        key="powerFactor_L3",
        name="L3 Power Factor",
        json_path=("powerFactor", "L3"),
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        unit="%",
        device_identifier_suffix="general",
    ),
    # Extender metrics
    SaveEyeSensorDescription(
        key="extender_deviceSerialNumber",
        name="Extender Serial Number",
        json_path=("extendersData", 0, "extenderDeviceId"),
        device_class=SensorDeviceClass.ENUM,
        state_class=None,
        unit=None,
        device_identifier_suffix="remote",
    ),
    SaveEyeSensorDescription(
        key="extender_rssi",
        name="Extender 1 Signal Strength",
        json_path=("extendersData", 0, "extenderRssi"),
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        unit="dBm",
        device_identifier_suffix="remote",
    ),
    SaveEyeSensorDescription(
        key="extender_totalConsumption_kwh",
        name="Extender 1 Active Cumulative Energy Consumption",
        json_path=("extendersData", 0, "activeTotalConsumption"),
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.MEASUREMENT,
        unit="kWh",
        device_identifier_suffix="remote",
        value_transform=lambda value: float(value) / 1000.0 if value is not None else None,
    ),
    SaveEyeSensorDescription(
        key="extender_totalpower",
        name="Extender 1 Active Consumption",
        json_path=("extendersData", 0, "activeActualConsumption"),
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfPower.WATT,
        device_identifier_suffix="remote",
    ),
    SaveEyeSensorDescription(
        key="extender_last_seen",
        name="Extender Last Seen",
        json_path=("extendersData", 0, "extenderTimestamp"),
        device_class=None,
        state_class=None,
        unit=None,
        device_identifier_suffix="remote",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SaveEye MQTT sensors based on a config entry.

    Entities are created dynamically based on the telemetry payload.
    Only sensors for properties that actually exist on the device are added.
    """
    stored = hass.data[DOMAIN][entry.entry_id]
    coordinator: SaveEyeCoordinator = stored[DATA_KEY_COORDINATOR]

    created_keys: set[str] = set()

    def extract_value(payload: Dict[str, Any], description: SaveEyeSensorDescription) -> Optional[float | int | str]:
        current: Any = payload
        for path_part in description.json_path:
            if isinstance(path_part, int):
                if not isinstance(current, list) or path_part < 0 or path_part >= len(current):
                    return None
                current = current[path_part]
            else:
                if not isinstance(current, dict) or path_part not in current:
                    return None
                current = current.get(path_part)

        transform: Optional[Callable[[Any], Optional[float | int | str]]] = description.value_transform
        if transform is not None:
            try:
                return transform(current)
            except (TypeError, ValueError):
                return None

        if current is None:
            return None

        if not isinstance(current, (float, int, str)):
            return None

        return current

    def handle_new_data() -> None:
        devices: Dict[str, Dict[str, Any]] = coordinator.devices
        if not devices:
            return

        _serial, payload = next(iter(devices.items()))

        new_entities: list[SaveEyeSensor] = []

        for description in SENSORS:
            if description.key in created_keys:
                continue

            value = extract_value(payload, description)
            if value is None:
                continue

            created_keys.add(description.key)
            new_entities.append(SaveEyeSensor(coordinator, description))

        if new_entities:
            async_add_entities(new_entities)

    # Register listener so that as soon as telemetry arrives, we create entities
    coordinator.async_add_listener(handle_new_data)

    # Also attempt to create entities immediately in case data already exists
    handle_new_data()


class SaveEyeSensor(SensorEntity):
    """Representation of a SaveEye sensor."""

    _attr_should_poll = False

    def __init__(self, coordinator: SaveEyeCoordinator, description: SaveEyeSensorDescription) -> None:
        self._coordinator = coordinator
        self._description = description
        self._device_serial: Optional[str] = None
        self._attr_unique_id = f"saveeye_{description.key}"
        self._attr_name = description.name
        self._attr_device_class = description.device_class
        self._attr_state_class = description.state_class
        self._attr_native_unit_of_measurement = description.unit

    @property
    def device_info(self) -> DeviceInfo:
        serial: str = self._device_serial or "unknown"
        identifiers = {(DOMAIN, f"{serial}_{self._description.device_identifier_suffix}")}
        return DeviceInfo(
            identifiers=identifiers,
            manufacturer="SaveEye ApS",
            name="SaveEye Device",
            model="V1",
        )

    @property
    def native_value(self) -> Optional[float | int | str]:
        """Return the sensor value from latest coordinator data."""
        devices: Dict[str, Dict[str, Any]] = self._coordinator.devices
        if not devices:
            return None

        # Use first device in mapping for now (single-topic, single-device assumption).
        serial, payload = next(iter(devices.items()))
        self._device_serial = serial

        current: Any = payload
        for path_part in self._description.json_path:
            if isinstance(path_part, int):
                if not isinstance(current, list) or path_part < 0 or path_part >= len(current):
                    return None
                current = current[path_part]
            else:
                if not isinstance(current, dict) or path_part not in current:
                    return None
                current = current.get(path_part)

        transform = self._description.value_transform
        if transform is not None:
            try:
                return transform(current)
            except (TypeError, ValueError):
                return None

        return current

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self._coordinator.async_add_listener(self._handle_coordinator_update))

    async def async_will_remove_from_hass(self) -> None:
        # Listener removal is handled by async_on_remove registrations.
        return

    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()
