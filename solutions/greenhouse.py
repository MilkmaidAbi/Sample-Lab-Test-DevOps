import csv

VALID_ZONES = ["A", "B", "C"]


def load_readings(filename):
    readings = []
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            readings.append(row)
    return readings


def convert_to_fahrenheit(celsius):
    return float(celsius) * 9 / 5 + 32


def display_all_readings(readings):
    print("ID\tZone\tTemp(C)\tTemp(F)\tHumidity\tSoil".expandtabs(10))
    for r in readings:
        temp_f = round(convert_to_fahrenheit(r["temperature"]), 1)
        print((r["reading_id"] + "\t" + r["zone"] + "\t" + str(r["temperature"]) + "\t" + str(temp_f)
               + "\t" + str(r["humidity"]) + "\t" + str(r["soil_moisture"])).expandtabs(10))


def display_records(records):
    if len(records) == 0:
        print("No readings found")
        return
    display_all_readings(records)


def get_reading_by_id(readings, reading_id):
    for r in readings:
        if r["reading_id"] == reading_id:
            return r
    return None


# ---------------- REQ-01 ----------------
def get_readings_by_zone(readings, zone):
    result = []
    target = zone.strip().upper()
    for r in readings:
        if r["zone"].upper() == target:
            result.append(r)
    return result


# ---------------- REQ-02 ----------------
def calc_zone_statistics(readings, zone):
    zone_readings = get_readings_by_zone(readings, zone)
    if len(zone_readings) == 0:
        return None
    temps = []
    for r in zone_readings:
        temps.append(float(r["temperature"]))
    return {
        "count": len(temps),
        "min": min(temps),
        "max": max(temps),
        "average": round(sum(temps) / len(temps), 2),
    }


# ---------------- REQ-03 ----------------
def get_hottest_reading(readings):
    if len(readings) == 0:
        return None
    hottest = readings[0]
    for r in readings:
        if float(r["temperature"]) > float(hottest["temperature"]):
            hottest = r
    return hottest


# ---------------- REQ-04 ----------------
def classify_reading(reading):
    temp = float(reading["temperature"])
    soil = float(reading["soil_moisture"])
    if temp >= 35.0 or soil < 20:
        return "CRITICAL"
    elif temp >= 30.0 or soil < 35:
        return "WARNING"
    else:
        return "NORMAL"


def get_alert_summary(readings):
    summary = {"CRITICAL": 0, "WARNING": 0, "NORMAL": 0}
    for r in readings:
        level = classify_reading(r)
        summary[level] = summary[level] + 1
    return summary


# ---------------- REQ-05 ----------------
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_next_reading_id(readings):
    highest = 0
    for r in readings:
        number = int(r["reading_id"][1:])      # "R012" -> 12
        if number > highest:
            highest = number
    return "R" + str(highest + 1).zfill(3)


def add_reading(readings, zone, temperature, humidity, soil_moisture):
    zone = str(zone).strip().upper()
    temperature = str(temperature).strip()
    humidity = str(humidity).strip()
    soil_moisture = str(soil_moisture).strip()

    if zone not in VALID_ZONES:
        return 1
    if not (is_number(temperature) and is_number(humidity) and is_number(soil_moisture)):
        return 2
    if not (0 <= float(humidity) <= 100) or not (0 <= float(soil_moisture) <= 100):
        return 3

    readings.append({
        "reading_id": get_next_reading_id(readings),
        "zone": zone,
        "temperature": temperature,
        "humidity": humidity,
        "soil_moisture": soil_moisture,
    })
    return 0


# ---------------- menu (REQ-06) ----------------
def display_main_menu(readings):
    print("=" * 45)
    print("----- Smart Greenhouse Monitor -----")
    print("=" * 45)
    print("Select option")
    print("1 - Display all readings")
    print("2 - Display zone statistics")
    print("3 - Display hottest reading")
    print("4 - Display alert summary")
    print("5 - Add new reading")
    print("6 - Display readings by zone")
    print("7 - Find reading by ID")
    print("Q - Quit")
    print("=" * 45)
    option = input("Enter selection => ").strip()

    if option == "1":
        display_all_readings(readings)

    elif option == "2":
        zone = input("Zone = ")
        stats = calc_zone_statistics(readings, zone)
        if stats is None:
            print("No readings found")
        else:
            print("Count = " + str(stats["count"]))
            print("Min = " + str(stats["min"]))
            print("Max = " + str(stats["max"]))
            print("Average = " + str(stats["average"]))

    elif option == "3":
        hottest = get_hottest_reading(readings)
        if hottest is None:
            print("No readings found")
        else:
            display_records([hottest])

    elif option == "4":
        summary = get_alert_summary(readings)
        for level in ["CRITICAL", "WARNING", "NORMAL"]:
            print(level + " = " + str(summary[level]))

    elif option == "5":
        zone = input("Zone = ")
        temperature = input("Temperature = ")
        humidity = input("Humidity = ")
        soil_moisture = input("Soil moisture = ")
        code = add_reading(readings, zone, temperature, humidity, soil_moisture)
        if code == 0:
            print("Reading added: " + readings[-1]["reading_id"])
        elif code == 1:
            print("Error: invalid zone")
        elif code == 2:
            print("Error: values must be numeric")
        elif code == 3:
            print("Error: humidity and soil moisture must be 0-100")

    elif option == "6":
        zone = input("Zone = ")
        display_records(get_readings_by_zone(readings, zone))

    elif option == "7":
        reading_id = input("Reading ID = ")
        reading = get_reading_by_id(readings, reading_id)
        if reading is None:
            print("No readings found")
        else:
            display_records([reading])

    elif option.upper() == "Q":
        quit()

    else:
        print("Invalid option")


def main():
    readings = load_readings("readings.csv")
    while True:
        display_main_menu(readings)


if __name__ == "__main__":
    main()
