from cooling_tower.airside.louver import size_louver
from cooling_tower.fan.sound import estimate_cooling_tower_sound

def test_louver():
    x=size_louver(71.75,1.113,free_area_fraction=0.55,target_passage_velocity_m_s=2.5,loss_coefficient=2.0)
    assert abs(x.required_net_free_area_m2-28.7)<0.1
    assert abs(x.recommended_gross_louver_area_m2-52.18)<0.2
    assert 6.9 < x.pressure_drop_pa < 7.1

def test_sound():
    x=estimate_cooling_tower_sound(11.02,71.75,2.5,distance_m=10)
    assert x.combined_lwa_db > 95
    assert x.estimated_lpa_db < x.combined_lwa_db
