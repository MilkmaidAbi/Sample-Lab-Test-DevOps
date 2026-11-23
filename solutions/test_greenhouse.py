import pytest
import greenhouse


def make_readings():
    # Own data in the same shape as readings.csv (all values are strings)
    return [
        {"reading_id": "R001", "zone": "A", "temperature": "28.5", "humidity": "65", "soil_moisture": "40"},
        {"reading_id": "R002", "zone": "B", "temperature": "31.0", "humidity": "58", "soil_moisture": "33"},
        {"reading_id": "R003", "zone": "A", "temperature": "9.5", "humidity": "80", "soil_moisture": "55"},
        {"reading_id": "R004", "zone": "C", "temperature": "35.2", "humidity": "45", "soil_moisture": "18"},
        {"reading_id": "R005", "zone": "C", "temperature": "35.2", "humidity": "50", "soil_moisture": "60"},
    ]


def make_reading(temperature, soil_moisture):
    return {"reading_id": "R999", "zone": "A", "temperature": temperature,
            "humidity": "50", "soil_moisture": soil_moisture}


# ---------- given test (fails until the Fahrenheit defect is fixed) ----------
def test_convert_to_fahrenheit():
    assert greenhouse.convert_to_fahrenheit(0) == 32
    assert greenhouse.convert_to_fahrenheit(100) == 212
    assert greenhouse.convert_to_fahrenheit(-40) == -40
    assert greenhouse.convert_to_fahrenheit("37.0") == pytest.approx(98.6)


# ---------- defect test: get_reading_by_id ----------
def test_get_reading_by_id():
    data = make_readings()
    assert greenhouse.get_reading_by_id(data, "R001") == data[0]
    assert greenhouse.get_reading_by_id(data, "R004") == data[3]     # fails on the given code
    assert greenhouse.get_reading_by_id(data, "R999") is None
    assert greenhouse.get_reading_by_id([], "R001") is None


# ---------- REQ-01 ----------
def test_get_readings_by_zone():
    data = make_readings()
    assert greenhouse.get_readings_by_zone(data, "A") == [data[0], data[2]]
    assert greenhouse.get_readings_by_zone(data, "a") == [data[0], data[2]]
    assert greenhouse.get_readings_by_zone(data, "  c ") == [data[3], data[4]]
    assert greenhouse.get_readings_by_zone(data, "D") == []
    assert greenhouse.get_readings_by_zone([], "A") == []


# ---------- REQ-02 ----------
def test_calc_zone_statistics():
    data = make_readings()
    stats = greenhouse.calc_zone_statistics(data, "a")
    assert stats["count"] == 2
    assert stats["min"] == pytest.approx(9.5)        # string min would give "28.5"
    assert stats["max"] == pytest.approx(28.5)       # string max would give "9.5"
    assert stats["average"] == pytest.approx(19.0)
    three = [{"zone": "B", "temperature": "10"}, {"zone": "B", "temperature": "10"},
             {"zone": "B", "temperature": "11"}]
    assert greenhouse.calc_zone_statistics(three, "B")["average"] == 10.33   # rounded to 2 d.p.
    assert greenhouse.calc_zone_statistics(data, "D") is None
    assert greenhouse.calc_zone_statistics([], "A") is None


# ---------- REQ-03 ----------
def test_get_hottest_reading():
    data = make_readings()
    hottest = greenhouse.get_hottest_reading(data)
    assert hottest == data[3]                        # tie 35.2 -> FIRST one (R004, not R005)
    assert hottest["reading_id"] == "R004"
    assert greenhouse.get_hottest_reading(data[:3]) == data[1]   # "9.5" must not win
    assert greenhouse.get_hottest_reading([]) is None


# ---------- REQ-04 ----------
def test_classify_reading():
    assert greenhouse.classify_reading(make_reading("35.0", "50")) == "CRITICAL"   # temp boundary
    assert greenhouse.classify_reading(make_reading("34.9", "50")) == "WARNING"
    assert greenhouse.classify_reading(make_reading("30.0", "50")) == "WARNING"    # temp boundary
    assert greenhouse.classify_reading(make_reading("29.9", "50")) == "NORMAL"
    assert greenhouse.classify_reading(make_reading("25", "19.9")) == "CRITICAL"   # soil boundary
    assert greenhouse.classify_reading(make_reading("25", "20")) == "WARNING"
    assert greenhouse.classify_reading(make_reading("25", "34.9")) == "WARNING"
    assert greenhouse.classify_reading(make_reading("25", "35")) == "NORMAL"       # soil boundary
    assert greenhouse.classify_reading(make_reading("31", "10")) == "CRITICAL"     # CRITICAL wins


def test_get_alert_summary():
    assert greenhouse.get_alert_summary(make_readings()) == {"CRITICAL": 2, "WARNING": 1, "NORMAL": 2}
    assert greenhouse.get_alert_summary([]) == {"CRITICAL": 0, "WARNING": 0, "NORMAL": 0}


# ---------- REQ-05 ----------
def test_add_reading():
    data = make_readings()
    assert greenhouse.add_reading(data, " b ", "26.5", "60", "45") == 0
    assert len(data) == 6
    new = data[-1]
    assert new["reading_id"] == "R006"
    assert new["zone"] == "B"
    assert new["temperature"] == "26.5"
    assert greenhouse.get_readings_by_zone(data, "B")[-1] == new


def test_add_reading_next_id_uses_highest():
    data = [{"reading_id": "R001", "zone": "A", "temperature": "1", "humidity": "1", "soil_moisture": "1"},
            {"reading_id": "R010", "zone": "A", "temperature": "1", "humidity": "1", "soil_moisture": "1"}]
    assert greenhouse.add_reading(data, "A", "20", "50", "50") == 0
    assert data[-1]["reading_id"] == "R011"          # highest + 1, not count + 1
    empty = []
    assert greenhouse.add_reading(empty, "C", "20", "50", "50") == 0
    assert empty[0]["reading_id"] == "R001"


def test_add_reading_invalid():
    data = make_readings()
    assert greenhouse.add_reading(data, "D", "20", "50", "50") == 1
    assert greenhouse.add_reading(data, "", "20", "50", "50") == 1
    assert greenhouse.add_reading(data, "A", "hot", "50", "50") == 2
    assert greenhouse.add_reading(data, "A", "20", "", "50") == 2
    assert greenhouse.add_reading(data, "A", "20", "101", "50") == 3
    assert greenhouse.add_reading(data, "A", "20", "50", "-1") == 3
    assert greenhouse.add_reading(data, "D", "hot", "500", "50") == 1   # zone checked first
    assert greenhouse.add_reading(data, "A", "hot", "500", "50") == 2   # then numeric
    assert len(data) == 5                                                # nothing was added


def test_add_reading_boundaries():
    data = make_readings()
    assert greenhouse.add_reading(data, "A", "-5", "0", "100") == 0      # 0 and 100 are allowed
    assert greenhouse.add_reading(data, "A", "20", "100.1", "50") == 3
