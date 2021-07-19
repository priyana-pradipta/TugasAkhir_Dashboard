
from app import db, login_manager
from flask import Flask,render_template, redirect, url_for, request, Response, make_response, current_app
import time, os, copy, datetime, sys, csv, zipfile
from io import BytesIO, StringIO

def get_records():

    from_date_str = request.args.get('from', time.strftime(
        "%Y-%m-%d 00:00"))  # Get the from date value from the URL
    to_date_str = request.args.get('to', time.strftime(
        "%Y-%m-%d %H:%M"))  # Get the to date value from the URL

    # Validate date before sending it to the DB
    if not validate_date(from_date_str):
        from_date_str = time.strftime("%Y-%m-%d 00:00")
    if not validate_date(to_date_str):
        # Validate date before sending it to the DB
        to_date_str = time.strftime("%Y-%m-%d %H:%M")

    temperatures = db.get_engine(bind='sensor').execute("SELECT rDatetime, temp FROM sensors WHERE rDateTime BETWEEN (?) AND (?) AND temp IS NOT NULL",
                                                       (from_date_str, to_date_str))
    temps_chart = db.get_engine(bind='sensor').execute("SELECT rDatetime, COALESCE(NULLIF(temp,''), 'null') FROM sensors WHERE rDateTime BETWEEN (?) AND (?)",
                                                       (from_date_str, to_date_str))
    humidities = db.get_engine(bind='sensor').execute("SELECT rDatetime, hum FROM sensors WHERE rDateTime BETWEEN (?) AND (?) AND hum IS NOT NULL",
                                                     (from_date_str, to_date_str))
    hums_chart = db.get_engine(bind='sensor').execute("SELECT rDatetime, COALESCE(NULLIF(hum,''), 'null') FROM sensors WHERE rDateTime BETWEEN (?) AND (?)",
                                                     (from_date_str, to_date_str))
    errors = db.get_engine(bind='sensor').execute("SELECT rDatetime, err FROM sensors WHERE rDateTime BETWEEN (?) AND (?) AND err IS NOT NULL",
                                                 (from_date_str, to_date_str))
    error_dict = list()
    for row in errors :
        if row[1] == -6 :
            status = "Waktu Timed Out"
        elif (row[1] == -7) or (row[1] == -701) :
            status = "CRC Error"
        elif row[1] == -16 :
            status = "Kesalahan SPI"
        elif row[1] == -2 :
            status = "Setup/Wiring Gagal"
        elif row[1] == -8 or row[1] == -12 or row[1] == -13 or row[1] == -17 or row[1] == -18 or row[1] == -101 or row[1] == -102 or row[1] == -103 or row[1] == -104 :
            status = "Konfigurasi Salah"
        else :
            status = ""
        
        data = (row[0], row[1], status)
        error_dict.append(data)

    return [temperatures, humidities, error_dict, temps_chart, hums_chart, from_date_str, to_date_str]

def validate_date(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False

def render_data():
    return redirect(url_for('home_blueprint.tables_data'))

def zipFiles(files):
    zipped_file = BytesIO()
    with zipfile.ZipFile(zipped_file, 'w') as f:
    	for i, file in enumerate(files):
            if i == 0:
                #f.writestr(zipfile.Zipinfo("Temp.csv"), file.getvalue())
                f.writestr('{}.csv'.format('Temp'), file.getvalue())
            if i == 1:
                f.writestr('{}.csv'.format('Hum'), file.getvalue())
            if i == 2:
                f.writestr('{}.csv'.format('Err'), file.getvalue())
    return zipped_file.getvalue()

def fetch_table_data(aspect,condition):

    from_date_str = request.args.get('from', time.strftime(
        "%Y-%m-%d 00:00"))  
    to_date_str = request.args.get('to', time.strftime(
        "%Y-%m-%d %H:%M"))  

    if not validate_date(from_date_str):
        from_date_str = time.strftime("%Y-%m-%d 00:00")
    if not validate_date(to_date_str):
        to_date_str = time.strftime("%Y-%m-%d %H:%M")

    target = aspect.decode("utf-8") 

    if condition == b'byDate' :
        result = db.get_engine(bind='sensor').execute('SELECT rDatetime, {} FROM sensors WHERE rDateTime BETWEEN ? AND ?'.format(target),(from_date_str, to_date_str))
        col_title = db.get_engine(bind='sensor').execute('SELECT rDatetime, {} FROM sensors WHERE rDateTime BETWEEN ? AND ?'.format(target), (from_date_str, to_date_str)).keys()
    elif condition == b'byRecent' :
        result = db.get_engine(bind='sensor').execute('SELECT rDatetime, {} FROM (SELECT * FROM sensors ORDER BY rDatetime DESC LIMIT 10) ORDER BY rDatetime ASC'.format(target))
        col_title = db.get_engine(bind='sensor').execute('SELECT rDatetime, {} FROM (SELECT * FROM sensors ORDER BY rDatetime DESC LIMIT 10) ORDER BY rDatetime ASC'.format(target)).keys()

    dump_file = StringIO()
    writer = csv.writer(dump_file, delimiter=",")
    writer.writerow(col_title)
    writer.writerows(result)

    return dump_file

def get_recents():
    temps_chart = db.get_engine(bind='sensor').execute("SELECT rDatetime, COALESCE(NULLIF(temp,''), 'null') FROM sensors ORDER BY rDatetime DESC LIMIT 10")
    hums_chart = db.get_engine(bind='sensor').execute("SELECT rDatetime, COALESCE(NULLIF(hum,''), 'null') FROM sensors ORDER BY rDatetime DESC LIMIT 10")
    uptimes_chart = db.get_engine(bind='sensor').execute("SELECT *,  max(t.PeriodCount) over (order by t.rDatetime) from (SELECT rDatetime, case when hum is not null then row_number() over (partition by temp is not null order by rDatetime) end as PeriodCount FROM sensors ORDER BY rDatetime ASC) t")

    
    recent_time = db.get_engine(bind='sensor').execute("SELECT rDatetime, COALESCE(NULLIF(hum,''), 'No Data'), COALESCE(NULLIF(temp,''), 'No Data') FROM sensors ORDER BY rDatetime DESC LIMIT 1")
    for row in recent_time :
        time = (row[0])
        show_recent_hum = (row[1])
        show_recent_temp = (row[2])

    totals_data = db.get_engine(bind='sensor').execute("SELECT COUNT(*) FROM sensors")
    for row in totals_data :
        count_total_data =  (row[0])

    errors_data = db.get_engine(bind='sensor').execute("SELECT COUNT(*) FROM Sensors WHERE err IS NOT NULL")
    for row in errors_data :
        count_error_data = (row[0])

    uploads_data = db.get_engine(bind='sensor').execute("SELECT COUNT(*) FROM Sensors WHERE uploaded IN ('1')")
    for row in uploads_data :
        count_upload_data = (row[0]) 

    recent_tables = db.get_engine(bind='sensor').execute("SELECT rDatetime, COALESCE(NULLIF(hum,''), ''), COALESCE(NULLIF(temp,''), ''), COALESCE(NULLIF(err,''), '') FROM sensors ORDER BY rDatetime DESC LIMIT 10")
    recent_dict = list()
    for row in recent_tables :
        if row[3] == -6 :
            status = "Timed Out"
        elif row[3] == -7 :
            status = "CRC Mismatch"
        elif row[3] == -16 :
            status = "Kesalahan SPI"
        elif row[3] == -2 :
            status = "Setup/Wiring Gagal"
        elif row[3] == -8 or row[1] == -12 or row[1] == -13 or row[1] == -17 or row[1] == -18 or row[1] == -101 or row[1] == -102 or row[1] == -103 or row[1] == -104 :
            status = "Konfigurasi Salah"
        else :
            status = ""
        
        data = (row[0], row[1], row[2], row[3], status)
        recent_dict.append(data)

    
    return [recent_dict, temps_chart, hums_chart, uptimes_chart, time, show_recent_hum, show_recent_temp, count_total_data, count_error_data, count_upload_data]