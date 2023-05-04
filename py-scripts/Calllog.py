import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")

mydb = client["call_logs"]

mycol = mydb["logs"]

with open('call_log.txt', 'r') as file:
    log_date, log_os, log_remote_ip, log_remote_port = "", "", "", ""
    call_logs = []

    for line in file:
        if "Date:" in line:
            log_date = line.replace("Date:", "").strip()
        elif "OS:" in line:
            log_os = line.replace("OS:", "").strip()
        elif "Remote IP:" in line:
            log_remote_ip = line.replace("Remote IP:", "").strip()
        elif "Remote Port:" in line:
            log_remote_port = line.replace("Remote Port:", "").strip()

        elif "Number" in line:
            number = line.replace("Number:", "").strip()
            name = file.readline().replace("Name:", "").strip()
            call_date = file.readline().replace("Date:", "").strip()
            call_type = file.readline().replace("Type:", "").strip()
            call_duration = file.readline().replace("Duration:", "").strip()

            call_logs.append({
                "number": number,
                "name": name,
                "date": call_date,
                "type": call_type,
                "duration": call_duration
            })

    log_details = {
        "date": log_date,
        "os": log_os,
        "remote_ip": log_remote_ip,
        "remote_port": log_remote_port,
        "call_logs": call_logs
    }

    mycol.insert_one(log_details)

print("Data inserted")
