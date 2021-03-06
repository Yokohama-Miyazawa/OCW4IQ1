from django.shortcuts import render
from django.http.response import HttpResponse
import pymysql
import ast


def db_connect():
    return pymysql.connect(host='localhost',
                                 user='chakku',
                                 password='chakku',
                                 # db='test',
                                 db='test_ocw',
                                 charset='utf8',
                                 # Selectの結果をdictionary形式で受け取る
                                 cursorclass=pymysql.cursors.DictCursor)

# Create your views here.
def test_response(request):
    return HttpResponse("OCW4IQ1")

def toppage(request):
    d = {'default_input_value' : '授業名'}
    return render(request,'OCW/topPage.html',d)

def search_and_result(request):
    # テーブルヘッダ
    result_head = {'quarter': 'クォーター', 'lecname': '講義名', 'teacher': '教員名'}

    # リクエストから取れる情報
    lecname = request.GET.get("lectureName")    # 講義名


    # リクエストに応じてDBから情報を取得
    # TODO

    #content = [('1Q', '講義名1', '教員名3','lecture'), ('2Q', '講義名2', '教員名2','lecture'), ('1Q', '講義名3', '教員名3','lecture')]
    content = []
    result_content = []

    #SQL kakeru baai
    with db_connect().cursor() as cursor:
        sql = "SELECT Quarter,LectureName,Professor,LectureCode FROM lecture WHERE LectureName like '%{}%'".format(lecname)
        cursor.execute(sql)
        dbdata = cursor.fetchall()
        for row in dbdata:
            content.append((row["Quarter"],row["LectureName"],row["Professor"],row["LectureCode"]))

    for item in content:
        result_content.append({'quarter': item[0], 'lecname': item[1], 'teacher': item[2] , 'code': item[3]})

    d = {
        'result_head': result_head,
        'result_content': result_content,
        'lectureName' : lecname,
    }
    return render(request, 'OCW/searchAndResult.html', d)


def lecture(request):
    # クエリから得られる情報
    code = request.GET.get("code")    # 講義名

    # 情報からのデータ構築
    d = {}
    with db_connect().cursor() as cursor:
        sql = "SELECT * FROM lecture WHERE LectureCode like '{}'".format(code)
        cursor.execute(sql)
        dbdata = cursor.fetchall()
        d = dbdata[0]

    d["LecturePlan"] = [{"term":p[0],"plan":p[1],"task":p[2]} \
        for p in ast.literal_eval(d["LecturePlan"].replace("\'","\\\'")
                                                    .replace("\\\\'","\'")
                                                    .replace("\r","\\r")
                                                    .replace("\n","\\n"))]

    return render(request,'OCW/lecture.html',d)


def department_page(request):
    request_param = request.GET.get('dep')
    result_head = {'series': '番台', 'lecname': '講義名', 'opening_department': '開講元', 'teacher': '教員名' , 'dateroom':'曜日・時間(講義室)'}

    def param2name(param):
        if param == "rigakuin":
            return "理学院"
        elif param == "kougakuin":
            return "工学院"
        elif param == "bussitsu":
            return "物質理工学院"
        elif param == "jouhou":
            return "情報理工学院"
        elif param == "seimei":
            return "生命理工学院"
        elif param == "kankyo":
            return "環境・社会理工学院"
        elif param == "sonota":
            return "その他"

    gakuin_name = param2name(request_param)

    with db_connect().cursor() as cursor:
        sql = "SELECT LectureName,Department,Professor,LectureCode,DateRoom FROM lecture WHERE Gakuin like '%s'" % gakuin_name
        cursor.execute(sql)
        dbdata = cursor.fetchall()
        content = ((row["LectureName"],row["Department"],row["Professor"],row["LectureCode"],row["DateRoom"]) for row in dbdata)

    result_content = list(
            {
                'lecname': item[0],
                'opening_department': item[1],
                'teacher': item[2],
                'code': item[3],
                'series': '%s00' % item[3][-3:-2:],
                'dateroom': item[4]
                } for item in content)
    series_list = sorted({row['series'] for row in result_content})
    opening_department_list = sorted({row['opening_department'] for row in result_content})

    d = {
        'result_head' : result_head,
        'result_content' : result_content,
        'series_list' : series_list,
        'opening_department_list' : opening_department_list,
        'gakuin_name' : gakuin_name,
        }
    return render(request,'OCW/department.html',d)


def base_layout(request):
    template = 'OCW/base.html'
    return render(request, template)
