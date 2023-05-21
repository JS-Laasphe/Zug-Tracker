# Filtern der vom Tracker erfassten Daten
# Es soll der gewünschte Zug (z.B. RB xxxxx) aus der vom Tracker erstellten csv-Datei gesucht und in eine neue Datei
# gepackt werden. Wurde ein Zug an einem Tag mehrfach erfasst, soll der Zug mit der größten Verspätung genommen werden.
# Wurde der Zug bei einer der Mehrfacherfassungen in den Ausfall gesetzt, ist dieser aufzulisten.

import csv

input_file = "unfiltered.csv"


def filter_csv(input_file):
    train_numbers = input("Geben Sie die zu filternden Zahlen ein (durch Leerzeichen getrennt): ").split()
    filtered_data = []

    output_file_name = '-'.join(train_numbers) + ".csv"

    with open(input_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)

        for row in reader:
            name, direction, datetime, delay, canceled = row
            day = datetime.split()[0]

            # Überprüfen, ob die gewünschten Zahlen in der Zugnummer enthalten sind
            if any(number in name for number in train_numbers):
                if canceled == "True":
                    filtered_data.append(row)
                else:
                    if any(day_data[0] == day for day_data in filtered_data):
                        for day_data in filtered_data:
                            if day_data[0] == day:
                                prev_canceled = day_data[4]
                                if prev_canceled == "True":
                                    continue
                                prev_delay = day_data[3]
                                if delay > prev_delay:
                                    filtered_data.remove(day_data)
                                    filtered_data.append(row)
                                    break
                    else:
                        filtered_data.append(row)

    if not filtered_data:
        print("Keine Daten für die angegebenen Zugnummern gefunden.")
        return

    header = ["Name", "Herkunft", "Ankunft", "Verspätung", "Ausgefallen"]

    with open(output_file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(header)

        for row in filtered_data:
            writer.writerow(row)

    print(f"Die gefilterten Daten wurden in der Datei {output_file_name} gespeichert.")


filter_csv(input_file)

input("Enter drücken!")
