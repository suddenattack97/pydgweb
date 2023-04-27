from flask import Flask,render_template

app = Flask(__name__)

# 기존 hello() 함수 변경
@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4444, debug=True)