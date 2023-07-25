import osmnx as ox
import geopandas as gpd
import random
from shapely.geometry import Point, LineString
import pymysql

def generate_random_point_on_road(gdf):
    # 랜덤한 도로 선택
    random_road = gdf.sample(1).iloc[0]

    # 도로의 라인 객체를 얻음
    road_line = random_road['geometry']

    # 라인 위의 랜덤한 위치를 선택
    random_position_along_line = random.random()

    # 라인 위의 랜덤한 점을 계산
    random_point = road_line.interpolate(random_position_along_line, normalized=True)

    return random_point

while True:
    # 서울 중심을 기준으로 도로 네트워크 데이터를 다운로드
    G = ox.graph_from_point((37.5665, 126.9780), dist=200, network_type='drive')

    # 도로 네트워크를 GeoDataFrame으로 변환
    gdf = ox.graph_to_gdfs(G, nodes=False)

    # 도로 위의 랜덤한 점을 생성
    random_point_on_road = generate_random_point_on_road(gdf)

    # MySQL 연결 설정
    cnx = pymysql.connect(
    host="localhost",  # 예: "localhost"
    user="root",  # 예: "root"
    password="2412",  # 예: "yourpassword"
    database="road"  # 연결하려는 데이터베이스 이름. 예: "yourdatabase"
    )

    # 커서 생성
    cursor = cnx.cursor()

    # 랜덤한 점의 x, y 좌표를 가져옴
    x, y = random_point_on_road.x, random_point_on_road.y

    # MySQL 쿼리를 실행하여 road_data 테이블 업데이트
    update_query = "UPDATE road_data SET y_point = %s, x_point = %s WHERE idx = 1"
    print((x, y))
    cursor.execute(update_query, (x, y))

    # 변경사항을 커밋
    cnx.commit()

    # # 커서와 연결을 닫음
    cursor.close()
    cnx.close()