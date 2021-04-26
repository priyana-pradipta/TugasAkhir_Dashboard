# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from app import db, login_manager
from app.home import blueprint
from app.home.main import get_records, validate_date, render_data, zipFiles, fetch_table_data, get_recents
from flask import Flask,render_template, redirect, url_for, request, Response, make_response, current_app, jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if template == 'tables-data.html':
            return redirect(url_for('home_blueprint.tables_data'))
        elif template == 'download_csv':
            return redirect(url_for('home_blueprint.download_csv'))
        elif template == 'index2.html':
            return redirect(url_for('home_blueprint.home_index'))
        else :
            if (not template.endswith( '.html' )) and (not template == 'tables-data' or 'download_csv' or 'index2'):
                template += '.html'

            # Detect the current page
            segment = get_segment( request )

            # Serve the file (if exists) from app/templates/FILE.html
            return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  

@blueprint.route("/tables_data", methods=['GET'])
@login_required
def tables_data():
    temperatures, humidities, errors, temps_chart, hums_chart, from_date_str, to_date_str = get_records()
    return render_template(	"tables-data.html", 	temp=temperatures,
                            hum=humidities,
                            err=errors,
                            from_date=from_date_str,
                            to_date=to_date_str,
                            temp_chart=temps_chart,
                            hum_chart=hums_chart,
                            )


@blueprint.route("/download_csv", methods=['GET'])
@login_required
def download_csv():
    render_data()
    condz = request.args.get('cond')
    if condz == 'byDate' :
        table_temp = fetch_table_data('temp','byDate')
        table_hum = fetch_table_data('hum','byDate')
        table_err = fetch_table_data('err','byDate')
    else :
        table_temp = fetch_table_data('temp','byRecent')
        table_hum = fetch_table_data('hum','byRecent')
        table_err = fetch_table_data('err','byRecent')        
    file_List = [table_temp, table_hum, table_err]
    zipped_file = zipFiles(file_List)
    response = make_response(zipped_file)
    response.headers["Content-Type"] = "application/octet-stream"
    response.headers["Content-Disposition"] = "attachment; filename=Record.zip"
    return response


@blueprint.route("/home_index", methods=['GET'])
@login_required
def home_index():
    recents_tables, temps_chart, hums_chart, uptimes_chart, times, recents_hum, recents_temp, count_total_data, count_error_data, count_upload_data = get_recents()
    count_error_rate = (float(count_error_data) / float(count_total_data)) * 100
    datasplit_time = times.split(' ')
    recents_time1 = datasplit_time[0]
    recents_time2 = datasplit_time[1]
    upload_rate = (float(count_upload_data) / float(count_total_data)) * 100
    return render_template(	"index2.html", 	recent_table=recents_tables,
                            temp_chart=temps_chart,
                            hum_chart=hums_chart,
                            uptime_chart=uptimes_chart,
                            recent_time1=recents_time1,
                            recent_time2=recents_time2,
                            recent_hum=recents_hum,
                            recent_temp=recents_temp,
                            total_data= count_total_data,
                            error_data= count_error_data,
                            error_rate= count_error_rate,
                            upload_data= upload_rate
                            )



