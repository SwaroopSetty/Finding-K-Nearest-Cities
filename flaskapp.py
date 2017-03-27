from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
import memcache
import time

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Locations'
app.config['MYSQL_DATABASE_HOST'] = 'cloudcomputing.cljvknvits4o.us-west-2.rds.amazonaws.com'
mysql.init_app(app)

# Memcahe configurations
mc = memcache.Client(['cloudcomputing.acbbep.cfg.usw2.cache.amazonaws.com:11211'], debug=0)

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/Locations',methods=['POST','GET'])
def Locations():
    _cityName = request.form['inputName']
    _region = request.form['inputRegion']
    _distance = request.form['inputDistance']
    print _cityName
    print _region
    print _distance
    # validate the received values
    if _cityName and _region and _distance:

        # All Good, let's check in memcache
        key = _cityName+_region+_distance
        print key
        start_time = time.time()
        obj = mc.get(key)
        # If not in memcache lets query
        if not obj:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('geodist',(_cityName, _region, _distance))
            data = cursor.fetchall()
            end_time = time.time()
            total_time = str(end_time - start_time)
            if len(data) > 0:
                mc.set(key, data)
                list = "<tr><td><h3>City</h3></td> <td><h3>State</h3></td> <td><h3>Longitude</h3></td> <td><h3>Latitude</h3></td> <td><h3>Distance</h3></td></tr>"
                for row in data :
                    print row[0],row[1],row[2]
                    list= list+ "<tr><td>"+row[0]+"</td><td>"+str(row[1])+"</td><td>"+str(row[2])+"</td><td>"+str(row[3])+"</td><td>"+str(row[4])+"</td></tr>"
                return '''<!DOCTYPE html>
                <html>
                    <head>
                        <title>Python Flask Application</title>
                        <meta charset="utf-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
                    </head>
                    <body>
                        <table class="table table-bordered">''' + list + '''</table>
                        <br>
                        <h3> SQL Query time </h3>
                        ''' + total_time + '''
                    </body>
                </html>'''
            else:
                return json.dumps({'error':str(data[0])})
        else:
            print 'data found in memcache'
            end_time = time.time()
            total_time = str(end_time - start_time)
            list = "<tr><td><h3>City</h3></td> <td><h3>State</h3></td> <td><h3>Longitude</h3></td> <td><h3>Latitude</h3></td> <td><h3>Distance</h3></td></tr>"
            for row in obj :
                list= list+ "<tr><td>"+row[0]+"</td><td>"+str(row[1])+"</td><td>"+str(row[2])+"</td><td>"+str(row[3])+"</td><td>"+str(row[4])+"</td></tr>"
            return '''<!DOCTYPE html>
             <html>
                 <head>
                     <title>Python Flask Application</title>
                     <meta charset="utf-8">
                     <meta http-equiv="X-UA-Compatible" content="IE=edge">
                     <meta name="viewport" content="width=device-width, initial-scale=1">
                     <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
                 </head>
                 <body>
                     <table class="table table-bordered">''' + list + '''</table>
                     <br>
                     <h3> Memcached Query time </h3>
                     ''' + total_time + '''
                 </body>
             </html>'''
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


@app.route('/LocationsN',methods=['POST','GET'])
def LocationsN():
    print 'Inside N'
    _cityName = request.form['inputName']
    _region = request.form['inputRegion']
    _N = int(request.form['inputN'])
    _distance = 0
    print _N
    # validate the received values
    if _cityName and _region and _N:
        print 'Inside if'
        # All Good, let's check in memcache
        key = _cityName+_region+str(_N)+"_NVal"
        print key
        start_time = time.time()
        obj = mc.get(key)
        # If not in memcache lets query
        if not obj:
            conn = mysql.connect()
            while True:
                count = 0
                _distance = _distance + 10
                cursor = conn.cursor()
                cursor.callproc('geodist1',(_cityName, _region,_distance,_N))
                data = cursor.fetchall()
                if len(data) > 0:
                    for row in data :
                        count = count + 1
                if count >= _N:
                    break

            mc.set(key, data)
            end_time = time.time()
            total_time = str(end_time - start_time)
            list = "<tr><td><h3>City</h3></td> <td><h3>State</h3></td> <td><h3>Longitude</h3></td> <td><h3>Latitude</h3></td> <td><h3>Distance</h3></td></tr>"
            for row in data :
                list= list+ "<tr><td>"+row[0]+"</td><td>"+str(row[1])+"</td><td>"+str(row[2])+"</td><td>"+str(row[3])+"</td><td>"+str(row[4])+"</td></tr>"
            return '''<!DOCTYPE html>
                <html>
                    <head>
                        <title>Python Flask Application</title>
                        <meta charset="utf-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
                    </head>
                    <body>
                        <table class="table table-bordered">''' + list + '''</table>
                        <br>
                        <h3> SQL Query time </h3>
                        ''' + total_time + '''
                    </body>
                </html>'''
        else:
            end_time = time.time()
            total_time = str(end_time - start_time)
            list = "<tr><td><h3>City</h3></td> <td><h3>State</h3></td> <td><h3>Longitude</h3></td> <td><h3>Latitude</h3></td> <td><h3>Distance</h3></td></tr>"
            for row in obj :
                list= list+ "<tr><td>"+row[0]+"</td><td>"+str(row[1])+"</td><td>"+str(row[2])+"</td><td>"+str(row[3])+"</td><td>"+str(row[4])+"</td></tr>"
            return '''<!DOCTYPE html>
             <html>
                 <head>
                     <title>Python Flask Application</title>
                     <meta charset="utf-8">
                     <meta http-equiv="X-UA-Compatible" content="IE=edge">
                     <meta name="viewport" content="width=device-width, initial-scale=1">
                     <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
                 </head>
                 <body>
                     <table class="table table-bordered">''' + list + '''</table>
                     <br>
                     <h3> Memcached Query time </h3>
                     ''' + total_time + '''
                 </body>
             </html>'''
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


if __name__ == "__main__":
    app.run(debug=True)
