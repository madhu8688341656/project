
from flask import *
import mysql.connector
'''from werkzeug import secure_filename'''
'''from flask_ngrok import run_with_ngrok'''
import os
import csv

app=Flask(__name__)
'''run_with_ngrok(app)'''
app.secret_key="dnt tell"


myconn = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="placements"
)


@app.route("/")#index page or first page
@app.route("/update",methods=['GET','POST'])
def update():
	if not session.get('loggedin'):
		return render_template("login.html")
	if request.method=="POST":
		Company_name=request.form['Company_name']
		Drive_type=request.form['Drive_type']
		Eligible_gender=request.form.getlist('Eligible_gender')
		Eligible_gender=",".join(Eligible_gender)
		Branch=request.form.getlist('Branch')
		Branch=",".join(Branch)
		Eligibility=request.form['Eligibility']
		Backlogs=request.form['Backlogs']
		Reg_link=request.form['Reg_link']
		Rounds=request.form['Rounds']
		Package=request.form['Package']
		Location=request.form['Location']
		comment=request.form['comment']
		'''print(Companyname,Drive_type,Gender,Branch,Eligibility,Backlogs,Reg_link,Rounds,Package,Location,Comment)
		return "hii"'''
		mycur=myconn.cursor()
		mycur.execute("""insert into campus_details(Company_name,Drive_type,Eligible_gender,
			Branch,Eligibility,Backlogs,Reg_link,Rounds,
			Package,Location,comment)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
			(Company_name,Drive_type,Eligible_gender,Branch,Eligibility,Backlogs,
			Reg_link,Rounds,Package,Location,comment))
		myconn.commit()
		flash("Inserted succesfully")
		 

	else:
			flash("Already Inserted")

	return render_template("update.html")



@app.route("/modify",methods=['GET','POST'])
def modify():
	if not session.get('loggedin'):
		return render_template("login.html")
	if request.method=="POST":
		id=request.form['id']
		Company_name=request.form['Company_name']
		Drive_type=request.form['Drive_type']
		Eligible_gender=request.form.getlist('Eligible_gender')
		Eligible_gender=",".join(Eligible_gender)
		Branch=request.form.getlist('Branch')
		Branch=",".join(Branch)
		Eligibility=request.form['Eligibility']
		Backlogs=request.form['Backlogs']
		Reg_link=request.form['Reg_link']
		Rounds=request.form['Rounds']
		Package=request.form['Package']
		Location=request.form['Location']
		comment=request.form['comment']
		mycur=myconn.cursor()
		mycur.execute("""update campus_details set Company_name=%s,Drive_type=%s,Eligible_gender=%s,
			Branch=%s,Eligibility=%s,Backlogs=%s,Reg_link=%s,Rounds=%s,
			Package=%s,Location=%s,comment=%s where sno=%s""",
			(Company_name,Drive_type,Eligible_gender,Branch,Eligibility,Backlogs,
			Reg_link,Rounds,Package,Location,comment,id))
		myconn.commit()
		return redirect(url_for('viewcoming'))



@app.route("/edit",methods=['GET','POST'])
def edit():
	if not session.get('loggedin'):
		return render_template("login.html")
	if request.method == "POST":
		id=request.form['edit']
		cur=myconn.cursor()
		cur.execute("select * from campus_details where sno=%s"%(id))
		data=cur.fetchall()
		Eligible_gender=data[0][3].split(',')
		Branch=data[0][4].split(',')

     
		return render_template("edit.html",data=data,Branch=Branch,Eligible_gender=Eligible_gender)







		
@app.route("/login",methods=['GET','POST'])
def login():
	if request.method=="POST":
		uname=request.form['uname']
		pwd=request.form['pwd']
		cur=myconn.cursor()
		cur.execute("""select * from admins where 
			username=%s and password=%s""",(uname,pwd))
		data=cur.fetchall()
		if data:
			session['loggedin']=True
			session['user']=uname
			flash("Login Successfully")
			return render_template("layout.html")

		else:
			flash("Incorrect Username or Password")
	return render_template("login.html")



@app.route("/layout")
def layout():
	return render_template("layout.html")

@app.route("/files")
def files():
	if not session.get('loggedin'):
		return render_template("login.html")
	return render_template("files.html")



@app.route("/logout")
def logout():
	session['loggedin']=False
	return render_template("home.html")

@app.route("/view",methods=['GET','POST'])
def view():
	cur=myconn.cursor()
	cur.execute("select * from campus_details where status=1 ORDER BY sno DESC" )
	data=cur.fetchall()
	return render_template("view.html",data=data)


@app.route("/viewall",methods=['GET','POST'])
def viewall():
	cur=myconn.cursor()
	cur.execute("select * from campus_details  ORDER BY sno DESC" )
	data=cur.fetchall()
	return render_template("viewall.html",data=data)
	

@app.route("/viewcoming",methods=['GET','POST'])
def viewcoming():
	if not session.get('loggedin'):
		return render_template("login.html")
	if request.method=="POST":
		Placed=request.form['Placed_count']
		id=request.form['over']
		mycur=myconn.cursor()
		mycur.execute("""update campus_details set Placed=%s,status=0 where sno=%s  """ ,(Placed,id))
		myconn.commit()
		mycur.execute("select * from campus_details where status=1 ORDER BY sno DESC")
		data=mycur.fetchall()
		return render_template("viewcoming.html",data=data)
	else:

		cur=myconn.cursor()
		cur.execute("select * from campus_details where status=1 ORDER BY sno DESC")
		data=cur.fetchall()
		return render_template("viewcoming.html",data=data)


@app.route("/viewcompleted",methods=['GET','POST'])
def viewcompleted():
	if not session.get('loggedin'):
		return render_template("login.html")
	cur=myconn.cursor()
	cur.execute("select * from campus_details where status=0 ORDER BY sno DESC")
	data=cur.fetchall()
	return render_template("viewcompleted.html",data=data)




'''@app.route("/edit",methods=['GET','POST'])
def edit():
	if not session.get('loggedin'):
		return render_template("login.html")
	return render_template("edit.html")'''


@app.route("/delete",methods=['GET','POST'])
def delete():
	if not session.get('loggedin'):
		return render_template("login.html")
	if request.method == "POST":
		id=request.form['delete']
		cur=myconn.cursor()
		cur.execute("delete from campus_details where sno=%s"%(id))
		myconn.commit()
		flash("Deleted Successfully")
		return redirect(url_for('viewcoming'))
	

@app.route("/over",methods=['GET','POST'])
def over():
	if not session.get('loggedin'):
		return render_template("login.html")
	if request.method == "POST":
		id=request.form['over']
		cur=myconn.cursor()
		cur.execute("update campus_details set status=0 where sno=%s"%(id))
		myconn.commit()
		flash("Deleted Successfully")
		return redirect(url_for('viewcoming'))





@app.route("/contact")
def contact():
	return render_template("contact.html")


@app.route("/home")
def home():

	return render_template("home.html")








if __name__=="__main__":
	app.run(debug=True)


	
    