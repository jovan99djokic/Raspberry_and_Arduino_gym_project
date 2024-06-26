from flask import Flask, render_template, request, redirect, flash
from markupsafe import Markup
from db.db_function import*
from utils.file import*
from datetime import date, datetime, timedelta

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

todayDate = date.today()
noAccount = True

@app.route("/", methods=['GET', 'POST'])
def login():
   createDB()
   administrator = getAdministartor()
   
   if administrator == []:
      noAccount = True
   else:
      noAccount = False

   if request.method == "POST":
      username = request.form.get("username")
      password = request.form.get("password")
      repeatPassword = request.form.get("repeatPassword")

      if noAccount:
         if password == repeatPassword:
            newAdministrator = (username, password)
            insertAdministrator(newAdministrator)
            return render_template("login.html")
         else:
            message = Markup("<h3>Lozinke se ne poklapaju. Probajte ponovo.</h3>")
            flash(message)
      else:
         newAdministrator = getAdministartorByUsername(username)
         
         if password == newAdministrator[0][1]:
            return render_template("index.html")
         else:
            message = Markup("<h3>Pogrešna lozinka. Probajte ponovo.</h3>")
            flash(message)
      
   return render_template("login.html", noAccount = noAccount)

@app.route("/index")
def home():   
   return render_template("index.html")

@app.route("/users", methods=['GET', 'POST'])
def users():
   if request.method == "POST":
      if request.form['submit'] == 'delete':  
         deleteFile(app, request.form.get("filename"))
         deleteMembershipByUserId(request.form.get("id"))
         deleteUser(request.form.get("id"))
        
         emptyChip = (todayDate, -1, request.form.get("chipId"))
         updateChip(emptyChip)
         
      if request.form['submit'] == 'search':
         searchText = request.form.get("searchText")
         users = searchUsers(searchText)
   
   users = getUsersWithGroupsName()
   return render_template("users.html", users = users)

@app.route("/add_user", methods=['GET', 'POST'])
def addUser():
   groups = getGroups()
   chips = getEmptyChips()

   if request.method == "POST":
         firstname = request.form.get("firstname")
         lastname = request.form.get("lastname")
         personalId = request.form.get("personalId")
         groupId = request.form.get("group")
         idCard = request.form.get("idCard")
         userPicture = upload_file(app, 'userPicture')

         newUser = (firstname, lastname, personalId, groupId, idCard, userPicture)
         userId = insertUser(newUser)

         newChip = (todayDate, userId, idCard)
         updateChip(newChip)
   return render_template("add_user.html", groups = groups, chips = chips)

@app.route("/change_user", methods=['GET', 'POST'])
def changeUser():
   user = request.args.getlist('user')
   chips = getEmptyChips()

   if request.method == "POST":
      userId = request.form.get('userId')
      firstname = request.form.get("firstname")
      lastname = request.form.get("lastname")
      personalId = request.form.get("personalId")
      groupId = request.form.get("group")
      idCard = request.form.get("idCard")
      userFile = request.form.get("userFile")
      userPicture = upload_file(app, 'userPicture')

      if userPicture == 'None':
         userPicture = userFile

      oldIdCard = request.form.get('oldIdCard')

      if oldIdCard != idCard:
         oldChip = (todayDate, -1, oldIdCard)
         updateChip(oldChip)
      
      newUser = (firstname, lastname, personalId, groupId, idCard, userPicture, userId)
      newChip = (todayDate, userId, idCard)

      updateUser(newUser)
      updateChip(newChip)
      return redirect(request.form.get('next'))
   else:
      groups = getGroups()

   return render_template("change_user.html", groups = groups, user = user, chips = chips)

@app.route("/groups", methods=['GET', 'POST'])
def groups():
   if request.method == "POST":
      deleteGroup(request.form.get("id"))

   groups = getGroups()
   return render_template("groups.html", groups = groups)

@app.route("/add_group", methods=['GET', 'POST'])
def addGroup():
   if request.method == "POST":
      groupName = request.form.get("groupName")
      startTime = request.form.get("startTime")
      numberOfMonths = request.form.get("numberOfMonths")

      newGroup = (groupName, startTime, numberOfMonths)
      insertGroup(newGroup)
   
   return render_template("add_group.html")

@app.route("/change_group", methods=['GET', 'POST'])
def changeGroup():
   group = request.args.getlist('group')

   if request.method == "POST":
      groupId = request.form.get('groupId')
      groupName = request.form.get("groupName")
      startTime = request.form.get("startTime")
      numberOfMonths = request.form.get("numberOfMonths")
     
      newGroup = (groupName, startTime, numberOfMonths, groupId)
      updateGroup(newGroup)
      return redirect(request.form.get('next'))
   
   return render_template("change_group.html", group = group)

@app.route("/reports")
def reports():
   reports = getReportsWithUsers()
   return render_template("reports.html", reports = reports)

@app.route("/add_membership", methods=['GET', 'POST'])
def addMembership():
   user = request.args.getlist('user')
   
   if request.method == "POST":
      payDate = request.form.get("startDate")
      numberOfMonths = request.form.get("numberOfMonths")
      amount = request.form.get("amount")
      userId = request.form.get("userId")

      startDate = datetime.strptime(payDate, '%Y-%m-%d')
      lastPayDateMembershipOfUser = getLastPayDateMembershipByUserId(userId)

      if lastPayDateMembershipOfUser != []: 
         lastSaveDate = datetime.strptime(lastPayDateMembershipOfUser[0][1], '%Y-%m-%d')
         endDate = lastSaveDate + timedelta(days = int(lastPayDateMembershipOfUser[0][2]))
      else:
         endDate = startDate

      if startDate > endDate:
         payDate = startDate.strftime("%Y-%m-%d")
      else:
         payDate = endDate.strftime("%Y-%m-%d")

      newMembership = (payDate, numberOfMonths, userId, amount)
      insertMembership(newMembership)
      return redirect(request.form.get('next'))      
   
   return render_template("add_membership.html", user = user, todayDate = todayDate)

@app.route("/change_membership", methods=['GET', 'POST'])
def changeMembership():
   membership = request.args.getlist('membership')
   checkEndOfMembership(membership[3])

   if request.method == "POST":
      membershipId = request.form.get('membershipId')
      pay_date = request.form.get("startDate")
      numberOfMonths = request.form.get("numberOfMonths")
      amount = request.form.get("amount")

      newMembership = (pay_date, numberOfMonths, amount, membershipId)
      updateMembership(newMembership)
      return redirect(request.form.get('next'))
   
   return render_template("change_membership.html", membership = membership)

@app.route("/memberships", methods=['GET', 'POST'])
def memberships():
   if request.method == "POST":
      deleteMembership(request.form.get("id"))

   memberships = getMembershipsWithUser()
   return render_template("memberships.html", memberships = memberships)

@app.route("/memberships_by_user_id", methods=['GET', 'POST'])
def membershipsByUserId():
   if request.method == "POST":
      deleteMembership(request.form.get("id"))

   userId = request.args.get('userId')
   memberships = getMembershipByUserId(userId)
   endDates = []

   for membership in memberships:
      startDate = datetime.strptime(membership[1], '%Y-%m-%d')
      endDate = startDate + timedelta(days = int(membership[2]))
      endDates.append(endDate.strftime("%Y-%m-%d"))
   
   return render_template("memberships_by_user_id.html", memberships = memberships, endDates = endDates)

@app.route("/chips", methods=['GET', 'POST'])
def chips():
   if request.method == "POST":
      deleteChip(request.form.get("id"))

   chips = getChipsWithUsers()

   return render_template("chips.html", chips = chips)

@app.route("/add_chips", methods=['GET', 'POST'])
def addChips():
   chipId = ""   

   if request.method == "POST":
      if request.form['submit'] == 'readChip':
         chipId = readFile()
      if request.form['submit'] == 'insertChip':
         chipId = request.form.get("chipId")
         newChip = (int(chipId), todayDate, -1)
         chipId = ""
         insertChip(newChip)

   return render_template("add_chips.html", chipId = chipId)

if __name__ == '__main__':
   app.debug = True
   app.run()
   
def checkEndOfMembership(userId):
   print(userId)
   membership = getMembershipByUserId(userId)
   print(membership)