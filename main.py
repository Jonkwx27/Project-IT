from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__,template_folder='templates')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/user-login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("user_login.html")
    
@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run(debug=True)