from flask import Flask,render_template, request, jsonify
import pymysql
import json
from flask import Response
import time

app = Flask(__name__)

# 기존 hello() 함수 변경
@app.route('/test1')
def test1():
    return render_template('index.html')
@app.route('/test2')
def test2():
    return render_template('index2.html')
@app.route('/test3')
def test3():
    return render_template('index3.html')
@app.route('/map')
def map():
    return render_template('map_test.html')
@app.route('/map2')
def map2():
    return render_template('map2.html')
@app.route('/map3')
def map3():
    return render_template('map3.html')
@app.route('/map4')
def map4():
    return render_template('map4.html')
@app.route('/map5')
def map5():
    return render_template('map5.html')
@app.route('/map6')
def map6():
    return render_template('map6.html')
@app.route('/map_request')

def map_request():
    return render_template('map_request.html')
@app.route('/map_response')
def map_response():
    return render_template('map_response.html')


@app.route('/events')
def sse():
    def event_stream():
        last_id = None  # 마지막으로 가져온 데이터의 ID
        while True:
            cnx = pymysql.connect(
                host="localhost",
                user="root",
                password="2412",
                database="road"
            )
            cursor = cnx.cursor()

            # 마지막 ID 이후의 새로운 데이터를 가져오기
            if last_id:
                query = f"SELECT * from dataset_row WHERE idx > {last_id} ORDER BY idx ASC"
            else:
                query = "SELECT * from dataset_row ORDER BY idx ASC"
            
            cursor.execute(query)
            rows = cursor.fetchall()

            # 새로운 데이터가 있으면 클라이언트에 전송
            if rows:
                last_id = rows[-1][0]
                coordinates = [{"idx": row[0], "xy_date": row[1], "car_id": row[2], "x_point": row[3], "y_point": row[4]} for row in rows]
                data = {
                    "coordinates": coordinates,
                }
                yield f"data: {json.dumps(data)}\n\n"
            
            cursor.close()
            cnx.close()
            time.sleep(1)  # 1초 간격으로 데이터베이스 조회

    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/data_reset', methods=['POST'])
def data_reset():
    cnx = pymysql.connect(
        host="localhost",  # 예: "localhost"
        user="root",  # 예: "root"
        password="2412",  # 예: "yourpassword"
        database="road"  # 연결하려는 데이터베이스 이름. 예: "yourdatabase"
    )
    cursor = cnx.cursor()
    try:
        # 좌표를 데이터베이스에 저장
        query = "TRUNCATE TABLE dataset"
        cursor.execute(query)
        cnx.commit()
        return jsonify({"status": "success", "message": "Coordinate saved successfully"}), 200
    except Exception as e:
        print("General error:", e)
        return jsonify({"status": "error", "message": "General error: {}".format(e)}), 500
    finally:
        cursor.close()
        cnx.close()


@app.route('/save-coordinate', methods=['POST'])
def save_coordinate():
    car_id = request.form['car_id']
    x = request.form['x']
    y = request.form['y']

    cnx = pymysql.connect(
        host="localhost",  # 예: "localhost"
        user="root",  # 예: "root"
        password="2412",  # 예: "yourpassword"
        database="road"  # 연결하려는 데이터베이스 이름. 예: "yourdatabase"
    )
    cursor = cnx.cursor()
    try:
        # 좌표를 데이터베이스에 저장
        query = "INSERT INTO dataset (xy_date, car_id, x_point, y_point) VALUES (now(), %s, %s, %s)"
        cursor.execute(query, (car_id, x, y))
        cnx.commit()
        return jsonify({"status": "success", "message": "Coordinate saved successfully"}), 200
    except Exception as e:
        print("General error:", e)
        return jsonify({"status": "error", "message": "General error: {}".format(e)}), 500
    finally:
        cursor.close()
        cnx.close()
    # # MySQL 쿼리를 실행하여 road_data 테이블 업데이트
    # insert_query = "INSERT INTO dataset (x_point, y_point) VALUES (%s, %s)"
    # print((x, y))
    # cursor.execute(insert_query, (x, y))

    # # 변경사항을 커밋
    # cnx.commit()

    # # 커서와 연결을 닫음
    # cursor.close()
    # cnx.close()
  
@app.route('/events_foot')
def sse_foot():
    def event_stream_foot():
        last_id = None  # 마지막으로 가져온 데이터의 ID
        while True:
            cnx = pymysql.connect(
                host="localhost",
                user="root",
                password="2412",
                database="road"
            )
            cursor = cnx.cursor()

            # 마지막 ID 이후의 새로운 데이터를 가져오기
            if last_id:
                query = f"SELECT * from dataset WHERE idx > {last_id} AND footpoint IS NULL ORDER BY idx ASC"
            else:
                query = "SELECT * from dataset WHERE footpoint IS NULL ORDER BY idx ASC "
            #query = "SELECT * FROM dataset WHERE footpoint IS NULL ORDER BY idx ASC"
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # 새로운 데이터가 있으면 클라이언트에 전송
            if rows:
                last_id = rows[-1][0]
                coordinates = [{"idx": row[0], "xy_date": row[1], "car_id": row[2], "x_point": row[3], "y_point": row[4]} for row in rows]
                yield f"data: {json.dumps(coordinates)}\n\n"
            
            cursor.close()
            cnx.close()
            time.sleep(1)  # 1초 간격으로 데이터베이스 조회

    return Response(event_stream_foot(), mimetype="text/event-stream")
    

@app.route('/getfootPoint', methods=['POST'])
def getfootPoint():
    data = request.get_json()
    car_id = data.get('car_id')
    footPoint = data.get('footPoint')  # 이중 배열을 받아옵니다.
    ori_x = data.get('ori_x')  # 이중 배열을 받아옵니다.
    ori_y = data.get('ori_y')  # 이중 배열을 받아옵니다.
    #print(footPoint)
    cnx = pymysql.connect(
        host="localhost",  # 예: "localhost"
        user="root",  # 예: "root"
        password="2412",  # 예: "yourpassword"
        database="road"  # 연결하려는 데이터베이스 이름. 예: "yourdatabase"
    )
    cursor = cnx.cursor()

    try:    
        for points in footPoint: 
            query = "INSERT INTO dataset_row (xy_date, car_id, x_point, y_point) VALUES (now(), %s, %s, %s)"
            cursor.execute(query, (car_id, points[0], points[1]))
            cnx.commit()
            
        # 좌표를 데이터베이스에 저장
        query = "UPDATE dataset SET footpoint = 1 WHERE car_id = %s AND x_point = %s AND y_point = %s "
        cursor.execute(query, (car_id, ori_x, ori_y))
        cnx.commit()
        
        return jsonify({"status": "success", "message": "Coordinate saved successfully"}), 200
    except Exception as e:
        print("General error:", e)
        return jsonify({"status": "error", "message": "General error: {}".format(e)}), 500
    finally:
        cursor.close()
        cnx.close()
        
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4444, debug=True)