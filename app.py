from flask import Flask, request, redirect, session, render_template
from db import engine, Base, SessionLocal
from ai import analyze_resume
import models
import PyPDF2
import docx
import json

app = Flask(__name__)
app.secret_key = "bhopal_dev_secret_key"

Base.metadata.create_all(bind=engine)

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        db = SessionLocal()
        email = request.form.get("email") 
        password = request.form.get("password")
        
        if not email or not password:
            return "Email and Password are required!"

        existing_user = db.query(models.User).filter_by(email=email).first()
        if existing_user:
            db.close()
            return "User already exists. <a href='/login'>Login here</a>"

        new_user = models.User(email=email, password=password)
        db.add(new_user)
        db.commit()
        db.close()
        return redirect("/login")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = SessionLocal()
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.query(models.User).filter_by(email=email, password=password).first()
        db.close()

        if user:
            session["user"] = user.email
            session["user_id"] = user.id
            return redirect("/dashboard")
        return "Invalid credentials. <a href='/login'>Try again</a>"
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    result = None
    if request.method == "POST":
        user_goal = request.form.get("role")
        resume_text = request.form.get("resume")
        file = request.files.get("file")
        if file and file.filename != "":
            if file.filename.endswith(".pdf"):
                pdf_reader = PyPDF2.PdfReader(file)
                resume_text = "".join([p.extract_text() or "" for p in pdf_reader.pages])
            elif file.filename.endswith(".docx"):
                doc = docx.Document(file)
                resume_text = "\n".join([p.text for p in doc.paragraphs])

        if resume_text:
            result = analyze_resume(resume_text, user_goal)
            if result and "error" not in result:
                db = SessionLocal()
                report = models.Reports(
                    User_id=session["user_id"],
                    resume_text=resume_text[:500],
                    result=json.dumps(result)
                )
                db.add(report)
                db.commit()
                db.close()

    return render_template("dashboard.html", user=session["user"], result=result)

@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")
    db = SessionLocal()
    reports = db.query(models.Reports).filter_by(User_id=session["user_id"]).all()
    db.close()

    parsed_reports = []
    for r in reports:
        try:
            parsed_result = json.loads(r.result)
        except:
            parsed_result = {}
        parsed_reports.append({"resume": r.resume_text, "result": parsed_result})
    return render_template("history.html", reports=parsed_reports)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)