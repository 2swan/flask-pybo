import functools

from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)
'''
라우트 URL인 /login/에 매핑되는 login 함수를 생성했다. login 함수는 signup 함수와 비슷한 패턴이다.
 POST 방식 요청에는 로그인을 수행하고, GET 방식 요청에는 로그인 템플릿을 렌더링한다.
 데이터베이스에 저장된 비밀번호는 암호화되었으므로 입력된 비밀번호와 바로 비교할 수 없다. 
 POST 방식 요청으로 로그인 작업을 수행하는 과정을 알아보자. 우선 폼 입력으로 받은 username으로 데이터베이스에 해당 사용자가 있는지를 검사한다.
  만약 사용자가 없으면 ‘존재하지 않는 사용자입니다.’라는 오류를 발생시킨다. 사용자가 존재한다면 폼 입력으로 받은 password와 check_password_hash 함수를 사용하여 데이터베이스의 비밀번호와 일치하는지를 비교한다.
 입력된 비밀번호는 반드시 check_password_hash 함수로 똑같이 암호화하여 비교해야 한다.
 사용자도 존재하고 비밀번호도 올바르다면 플라스크 세션(session)에 키와 키값을 저장한다. 
 키에는 'user_id'라는 문자열을 저장하고 키값은 데이터베이스에서 조회된 사용자의 id값을 저장한다.
 
 세션 개념을 잠시 살펴보자. 세션은 request와 마찬가지로 플라스크가 자동으로 생성하여 제공하는 변수이다. 쉽게 말해 세션은 플라스크 서버를 구동하는 동안에는 영구히 참조할 수 있는 값이다.
  session 변수에 user의 id값을 저장했으므로 다양한 URL 요청에 이 세션값을 사용할 수 있다. 예를들어 현재 웹 브라우저를 요청한 주체가 로그인한 사용자인지 아닌지를 판 별할 수 있다.
  
  request는 요청, 응답이라는 과정에서만 사용할 수 있는 값인 반면, 세션은 플라스크 서버를 구동하는 동안에는 영구히 사용할 수 있는 값이므로 사용자 id를 저장하거나 활용하는 데 적합하다.
   단, 세션은 시간제한이 있어서 일정 시간 접속하지 않으면 자동으로 삭제된다.

'''

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

'''
여기서는 @bp.before_app_request 애너테이션을 사용했다. 이 애너테이션이 적용된 함수는 라우트 함수보다 먼저 실행된다.
 즉, 앞으로 load_logged_in_user 함수는 모든 라우트 함수보다 먼저 실행될 것이다.
 @bp.before_app_request 애너테이션은 플라스크에서 기본으로 제공한다.
 load_logged_in_user 함수에서 사용한 g는 플라스크가 제공하는 컨텍스트 변수이다. 이 변수는 request 변수와 마찬가지로 [요청 → 응답] 과정에서 유효하다. 코드에서 보듯 session 변수에 user_id값이 있으면 데이터베이스에서 이를 조회하여 g.user에 저장한다.

이렇게 하면 이후 사용자 로그인 검사를 할 때 session을 조사할 필요가 없다. g.user에 값이 있는지만 알아내면 된다. 
g.user에는 User 객체가 저장되어 있으므로 여러 가지 사용자 정보(username, email 등)를 추가로 얻어내는 이점이 있다.
 '''


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


'''코드에서 보듯 데코레이터 함수는 기존 함수를 감싸는 방법으로 간단히 만들 수 있다. 
이제 다른 함수에 @login_required 애너테이션을 지정하면 login_required 데코레이터 함수가 먼저 실행된다. login_required 함수는 g.user가 있는지를 조사하여 없으면 로그인 URL로 리다이렉트 하고 g.user가 있으면 원래 함수를 그대로 실행할 것이다.'''