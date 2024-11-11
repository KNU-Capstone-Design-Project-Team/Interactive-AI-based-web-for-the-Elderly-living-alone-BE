# app.py
from app import create_app
from flask_cors import CORS

app = create_app()
app.logger.debug("Flask app created")
CORS(app)  # 모든 출처에서의 접근을 허용

if __name__ == "__main__":
    app.run(port=5000, debug=True, threaded=True)
