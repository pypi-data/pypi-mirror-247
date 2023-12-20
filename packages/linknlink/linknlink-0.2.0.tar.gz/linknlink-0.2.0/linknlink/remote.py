"""Support for universal remotes."""
import struct

from . import exceptions as e
from .device import Device

class ehub(Device):
    """Controls a LinknLink ehub."""

    TYPE = "EHUB"
    
    # sensor function
    def _send(self, command: int, data: bytes = b"") -> bytes:
        """Send a packet to the device."""
        packet = struct.pack("<HI", len(data) + 4, command) + data
        resp = self.send_packet(0x6A, packet)
        e.check_error(resp[0x22:0x24])
        payload = self.decrypt(resp[0x38:])
        p_len = struct.unpack("<H", payload[:0x2])[0]
        return payload[0x6 : p_len + 2]
    
    def check_sensors(self) -> dict:
        """Return the state of the sensors."""
        resp = self._send(0x24)
        return {
            "envtemp": resp[0x0] + resp[0x1] / 100.0,
            "envhumid": resp[0x2] + resp[0x3] / 100.0,
            "pir_detected": "on" if resp[0x6] else "off",
        }

    def check_temperature(self) -> float:
        """Return the temperature."""
        return self.check_sensors()["temperature"]

    def check_humidity(self) -> float:
        """Return the humidity."""
        return self.check_sensors()["humidity"]
    
    def check_pir(self) -> str:
        """Return the pirDetected."""
        return self.check_sensors()["pir_detected"]

    # remote function
    def sweep_frequency(self) -> None:
        """Sweep frequency."""
        self._send(0x19)

    def check_frequency(self) -> bool:
        """Return True if the frequency was identified successfully."""
        resp = self._send(0x1A)
        return resp[0] == 1

    def find_rf_packet(self) -> None:
        """Enter radiofrequency learning mode."""
        self._send(0x1B)

    def cancel_sweep_frequency(self) -> None:
        """Cancel sweep frequency."""
        self._send(0x1E)

    def update(self) -> None:
        """Update device name and lock status."""
        resp = self._send(0x1)
        self.name = resp[0x48:].split(b"\x00")[0].decode()
        self.is_locked = bool(resp[0x87])

    def send_data(self, data: bytes) -> None:
        """Send a code to the device."""
        self._send(0x2, data)

    def enter_learning(self) -> None:
        """Enter infrared learning mode."""
        self._send(0x3)

    def check_data(self) -> bytes:
        """Return the last captured code."""
        return self._send(0x4)