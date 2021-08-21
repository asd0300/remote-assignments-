from flask import Flask, request, render_template, redirect, url_for
import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='a7788123',
                             database='assignment',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
@app.route('/')
def aa():
    return redirect((url_for('a')))
@app.route('/home') 
def a():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST']) #GET 接收form 的submit, POST 則傳送資料至mysql
def register():
    if request.method == 'POST' :  #表示form 這邊有自料被送出
        userDetails = request.form #設userDetails變數
        email = userDetails['email']#因在index.html 有對tag 設參數值可方便定義收到的email
        password = userDetails['password']
        
        with connection.cursor() as cursor:
            # Create a new record
            query = 'SELECT * FROM user WHERE email = %s'
            cursor.execute(query, email)
            data = cursor.fetchone()
            connection.commit()
            error = None
            if data:
                error = "A person with this email already exists, please try another email name"
                return render_template('member.html', wlcome=error)
            else:
                sql = "INSERT INTO `user` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, (email, password))
                connection.commit()
                error = "Register Success!"
                return render_template('member.html', wlcome=error)
    return render_template('index.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == "POST" and request.form["action"] =="SignIn":
        error= None
        email = request.form['email']
        password = request.form['password']
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `email`, `password` FROM `user` WHERE `email`=%s AND `password`=%s"
            cursor.execute(sql, (email,password))
            result = cursor.fetchone()
            if result:
                error = "Check ok, account login"
                return render_template('member.html', wlcome=error)
            else:
                error = "!! something wrong,Please double confirm email/password"
                return render_template('member.html', wlcome=error)
    error = ""
    return render_template('index.html', error=error)
  

if __name__ == '__main__':
    app.run(debug = True,host='localhost', port=3000)


