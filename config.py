# --------------------------------- [edit] ---------------------------------- #
import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"
# SECRET_KEY 환경 변수를 추가
'''
사실 SECRET_KEY = "dev"는 위험한 설정이다. 실제 서비스를 운영할 때에는 "dev"처럼 유추하기 쉬운 문자열을 입력하면 안 된다. 물론 현재는 개발환경이므로 괜찮다. 서비스 운영 환경에서 SECRET_KEY를 설정하는 방법은 4장에서 알아본다.
'''
# --------------------------------------------------------------------------- #
"""SQLALCHEMY_DATABASE_URI는 데이터베이스 접속 주소이고 SQLALCHEMY_TRACK_MODIFICATIONS는 SQLAlchemy의 이벤트를 처리하는 옵션이다.
 이 옵션은 파이보에 필요하지 않으므로 False로 비활성화했다. 아무튼 지금 설정한 내용은 pybo.db라는 데이터베이스 파일을 프로젝트의 루트 디렉터리에 저장하려는 것이다.

"""