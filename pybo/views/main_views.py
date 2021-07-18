# # --------------------------------- [edit] ---------------------------------- #
# from flask import Blueprint, url_for
# from werkzeug.utils import redirect
# # --------------------------------------------------------------------------- #
#
# bp = Blueprint('main', __name__, url_prefix='/')
# #블루프린트 객체명=Blueprint('이름',모듈명,url_prefix='/접두어')
# """@bp.route에서 bp는 Blueprint 클래스로 생성한 객체를 의미한다.
#  코드에서 보듯 Blueprint 클래스로 객체를 생성할 때는 이름, 모듈명, URL 프리픽스(url_prefix)값을 전달해야 한다.
#  URL 프리픽스는 특정 파일(main_views.py)에 있는 함수의 애너테이션 URL 앞에 기본으로 붙일 접두어 URL을 의미한다.
#   예를 들어 main_views.py 파일의 URL 프리픽스에 url_prefix='/' 대신 url_prefix='/main'이라고 입력했다면
#   hello_pybo 함수를 호출하는 URL은 localhost:5000/이 아니라 localhost:5000/main/이 된다.
# """
#
#
# @bp.route('/hello')  #url을  /hello로 등록
# def hello_pybo():
#     return 'Hello, Pybo!'
#
#
# # --------------------------------- [edit] ---------------------------------- #
# @bp.route('/')
# def index():
#     return redirect(url_for('question._list'))
# """detail 함수는 제거하고 index 함수는 question._list에 해당하는 URL로 리다이렉트할 수 있도록 코드를 수정했다.
#     redirect 함수는 입력받은 URL로 리다이렉트해 주고, url_for 함수는 라우트가 설정된 함수명으로 URL을 역으로 찾아준다.
#
#     url_for 함수에 전달된 question._list는 question, _list 순서로 해석되어 함수명을 찾아준다.
#     question은 등록된 블루프린트 이름, _list는 블루프린트에 등록된 함수명이라고 생각하면 된다.
#     현재 _list 함수에 등록된 라우트는 @bp.route('/list/')이므로
#      url_for('question._list')는 bp의 접두어인 /question/과 /list/가 더해진 /question/list/ URL을 반환한다.
#      이제 localhost:5000에 접속하면 리다이렉트 기능 덕분에 localhost:5000/question/list/ 페이지가 호출될 것이다. 확인해 보자."""
#
#
#
# # --------------------------------------------------------------------------- #
from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    return redirect(url_for('question._list'))