from cooling_tower.fan.selection import select_fan_and_motor
from cooling_tower.fills.properties import net_open_area


def test_xf75_open_area_example():
    assert abs(net_open_area(21.948, 0.91) - 19.97268) < 1e-6


def test_fan_motor_example():
    result = select_fan_and_motor(
        71.75,
        119.9,
        fan_efficiency=0.78,
        motor_efficiency=0.92,
        service_factor=1.15,
    )
    assert 10.9 < result.fan_shaft_power_kw < 11.2
    assert result.selected_motor_kw == 15.0
