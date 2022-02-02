from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import sqlite3
import random
from datetime import *

connection = sqlite3.connect("QuizApp.db")
cursor = connection.cursor()
class quizApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top",fill="both",expand="True")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (loginwindow, homepage, signuppage, quizquestions, resultpage, historypage, leaderboardpage):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(loginwindow)
        self.title("Quiz Application")
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
        
class loginwindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        f2 = Frame(self)
        global usernameEntry,nameEntry,usernameEntry1,gender1,gender2,gender3,passwordEntry1,passwordEntry
        usernameLabel = Label(f2, text="Username:",font=("Georgia",20))
        passwordLabel = Label(f2, text="Password:",font=("Georgia",20))
        usernameEntry = Entry(f2, font=("Modern No.20",15))
        passwordEntry = Entry(f2, show="*", font=("Modern No.20",15))
        def checkUser():
                cursor.execute("Select 1 from User where username=? and password=?",(usernameEntry.get(),passwordEntry.get()))
                if cursor.fetchone():
                    controller.show_frame(homepage)
                else:
                    tkinter.messagebox.showinfo("Error.","Incorrect username or password.")
        loginButton = Button(self, text="LOGIN", command=checkUser,width=40,height=1,bg="khaki1",font=("Georgia",15),relief=GROOVE)
        def emptyEntry1():
            controller.show_frame(signuppage)
            nameEntry.delete(0,END)
            usernameEntry1.delete(0,END)
            passwordEntry1.delete(0,END)
            gender1.deselect()
            gender2.deselect()
            gender3.deselect()
            usernameEntry.delete(0,END)
            passwordEntry.delete(0,END)
        signupButton = Button(self, text="Don't have an account? Click here to sign up.", command=emptyEntry1,fg="blue",relief=RIDGE,bd=0)
        self.img1 = PhotoImage(file="questionmark.png")
        quizclipartLabel = Label(self, image=self.img1)
        quizclipartLabel.pack()
        f2.pack()
        usernameLabel.grid(row=0)
        usernameEntry.grid(row=0,column=1,ipady=7,ipadx=15,pady=5)
        passwordLabel.grid(row=1)
        passwordEntry.grid(row=1,column=1,ipady=7,ipadx=15,pady=5)
        loginButton.pack()
        signupButton.pack()
        
class homepage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        f1 = Frame(self)
        bottomFrame = Frame(self)
        categoryLabel = Label(self, text = "Select Category:",font=("Georgia",25),pady=10)
        global categoryVar,r1,r2,r3,r4,r5,r6
        categoryVar = StringVar()
        r1 = Radiobutton(f1,text = "Brain Teasers",bg="lightpink1",width=25,height=3,font=("Georgia",15),variable=categoryVar,value="Brain Teasers",tristatevalue=0)
        r2 = Radiobutton(f1,text = "Animals",bg="khaki1",width=25,height=3,font=("Georgia",15),variable=categoryVar,value="Animals",tristatevalue=0)
        r3 = Radiobutton(f1,text = "Celebrities",bg="lightpink1",width=25,height=3,font=("Georgia",15),variable=categoryVar,value="Celebrities",tristatevalue=0)
        r4 = Radiobutton(f1,text = "General Knowledge",bg="khaki1",width=25,height=3,font=("Georgia",15),variable=categoryVar,value="General Knowledge",tristatevalue=0)
        r5 = Radiobutton(f1,text = "Geography",bg="lightpink1",width=25,height=3,font=("Georgia",15),variable=categoryVar,value="Geography",tristatevalue=0)
        r6 = Radiobutton(f1,text = "For Kids",bg="khaki1",width=25,height=3,font=("Georgia",15),variable=categoryVar,value="For Kids",tristatevalue=0)
        doneButton = Button(f1, text="GO TO QUIZ",command=lambda:controller.show_frame(quizquestions),width=20,height=2,bg="skyblue1",font=("Georgia",15))
        leaderboardButton1 = Button(bottomFrame, text="Leaderboard",command=lambda:controller.show_frame(leaderboardpage),width=20,height=2,bg="mediumpurple2")
        historyButton = Button(bottomFrame, text = "History",command=lambda: controller.show_frame(historypage),width=20,height=2,bg="mediumpurple2")
        def emptyEntry2():
            controller.show_frame(loginwindow)
            usernameEntry.delete(0,END)
            passwordEntry.delete(0,END)
        signoutButton = Button(bottomFrame, text = "Sign Out", command=emptyEntry2 ,width=20,height=2,bg="mediumpurple2")
        instructions = "INSTRUCTIONS:\nYou will be given two minutes. \nSolve as many multiple choice questions as you can.\nYou will get two chances to eliminate an option."
        instructionsLabel = Label(f1, text=instructions,font=("helvetica",13),pady=20)
        categoryLabel.pack()
        f1.pack()
        r1.grid(row=0)
        r2.grid(row=1)
        r3.grid(row=2)
        r4.grid(row=0,column=1)
        r5.grid(row=1,column=1)
        r6.grid(row=2,column=1)
        instructionsLabel.grid(row=3,columnspan=2)
        doneButton.grid(row=4,columnspan=2)
        bottomFrame.pack()
        leaderboardButton1.grid(row=0)
        historyButton.grid(row=0,column=1)
        signoutButton.grid(row=0,column=2)
        
class signuppage(Frame):
    def create_userTable():
        cursor.execute("Create table if not exists User(name TEXT check(length(name)>0), username TEXT primary key check(length(username)>0), gender TEXT check(length(gender)>0), password TEXT check(length(password)>0))")
        connection.commit()
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        global nameEntry,usernameEntry1,gender1,gender2,gender3,passwordEntry1,usernameEntry,passwordEntry
        f3 = Frame(self)
        enterdetailsLabel = Label(f3, text="Enter Your Details:",font=("helvetica",25),pady=10)
        nameLabel = Label(f3, text="Enter your name:",font=("helvetica",13))
        nameEntry = Entry(f3)
        usernameLabel1 = Label(f3, text = "Username:",font=("helvetica",13))
        usernameEntry1 = Entry(f3)
        gendervar = StringVar()
        genderLabel = Label(f3,text="Gender:",font=("helvetica",13))
        gender1 = Radiobutton(f3, text = "Male", variable=gendervar, value="Male",font=("helvetica",13),tristatevalue=0)
        gender2 = Radiobutton(f3, text = "Female", variable=gendervar, value="Female",font=("helvetica",13),tristatevalue=0)
        gender3 = Radiobutton(f3, text = "Others", variable=gendervar, value="Others",font=("helvetica",13),tristatevalue=0)
        passwordLabel1 = Label(f3, text = "Password:",font=("helvetica",13))
        passwordEntry1 = Entry(f3)
        def userData_entries():
            try:
                cursor.execute("Insert into User values(?,?,?,?)",(nameEntry.get(),usernameEntry1.get(),gendervar.get(),passwordEntry1.get()))
            except Exception:
                tkinter.messagebox.showinfo("Error.","Please try entering details again.")
            else:
                connection.commit()
                controller.show_frame(loginwindow)
        signupButton1 = Button(f3, text = "SIGN UP", command=userData_entries,font=("helvetica",13))
        alreadyButton = Button(f3, text = "Already have an account. Login.", command=lambda: controller.show_frame(loginwindow),font=("helvetica",13))
        f3.pack()
        enterdetailsLabel.grid(row=0,columnspan=2)
        nameLabel.grid(row=1)
        nameEntry.grid(row=1,column=1)
        usernameLabel1.grid(row=2)
        usernameEntry1.grid(row=2,column=1)
        genderLabel.grid(row=4)
        gender1.grid(row=4,column=1)
        gender2.grid(row=5,column=1)
        gender3.grid(row=6,column=1)
        passwordLabel1.grid(row=7)
        passwordEntry1.grid(row=7,column=1)
        signupButton1.grid(row=8,columnspan=2)
        alreadyButton.grid(row=9,columnspan=2)
        
class quizquestions(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller
        global startButton,timerLabel,timerVar,counter
        startImg = PhotoImage(file="startquiz.png")
        startButton = Button(self,command=self.selectFile,image=startImg,bd=0)
        startButton.image = startImg
        startButton.grid()
    def selectFile(self):
        global options,questions,correctLetter,qIndex,oIndex,score,categoryVar,startButton,checkRandom
        global count,total,timerLabel,timerVar,counter,lifelineCount,categoryName,quiznameLabel
        startButton.grid_forget()
        categoryName = categoryVar.get()
        if categoryName=="Celebrities":
            quizFile = open("celebrities.txt","r",encoding="utf8")
        elif categoryName=="Animals":
            quizFile = open("animals.txt","r",encoding="utf8")
        elif categoryName=="General Knowledge":
            quizFile = open("general.txt","r",encoding="latin-1")
        elif categoryName=="For Kids":
            quizFile = open("forkids.txt","r",encoding="utf8")
        elif categoryName=="Geography":
            quizFile = open("geography.txt","r",encoding="utf8")
        else:
            quizFile = open("brainteasers.txt","r",encoding="utf8")
            categoryName="Brain Teasers"
        line = quizFile.readline()[3:]
        options=[]
        questions=[]
        correctLetter =[]
        while(line != ""):
            questions.append(line)
            correctLetter.append(quizFile.readline()[2:])
            for i in range (4):
                options.append(quizFile.readline()[2:])
            line=quizFile.readline()
            line=quizFile.readline()[3:]
        quizFile.close()
        checkRandom = []
        qIndex = random.randint(0,144)
        oIndex = qIndex*4
        checkRandom.append(qIndex)
        score = 0
        count = 1
        lifelineCount = 2
        timerVar = StringVar()
        counter = 121
        timerVar.set(counter)
        quiznameLabel = Label(self, text=categoryName,font=("Georgia",20),fg="black")
        quiznameLabel.grid(row=0,columnspan=2)
        timerLabel = Label(self, textvariable=timerVar,font=("helvetica",15),fg="white",width=5,bg="mediumpurple1")
        timerLabel.grid(row=0,column=2)
        def countdown(i,label):
            global j,categoryName
            j = i
            if j > 0:
                j -= 1
                label.set(j)
                self.after(1000, lambda: countdown(j, label))
            else:
                historypage.historyData_entries(self,usernameEntry.get(),categoryName,score,count-1,datetime.now())
                self.controller.show_frame(resultpage)
                resultpage.showResult(self)
        countdown(counter,timerVar)
        self.viewQuestions()
    def viewQuestions(self):
        global questionLabel,option1,option2,option3,option4,optionVar,nextButton,total,lifelineButton,lifelineCount,endButton
        optionVar=StringVar()
        questionLabel=Label(self,text=questions[qIndex],bg="skyblue1",width=70,height=7,wraplength=600,justify=CENTER,font=("Georgia",12),bd=2)
        option1=Radiobutton(self,text=options[oIndex],variable=optionVar,value=options[oIndex],tristatevalue=0,bg="khaki1",width=75,height=2,justify=CENTER,wraplength=400)
        option2=Radiobutton(self,text=options[oIndex+1],variable=optionVar,value=options[oIndex+1],tristatevalue=0,bg="mediumpurple1",width=75,justify=CENTER,wraplength=400,height=2)
        option3=Radiobutton(self,text=options[oIndex+2],variable=optionVar,value=options[oIndex+2],tristatevalue=0,bg="khaki1",width=75,justify=CENTER,wraplength=400,height=2)
        option4=Radiobutton(self,text=options[oIndex+3],variable=optionVar,value=options[oIndex+3],tristatevalue=0,bg="mediumpurple1",width=75,justify=CENTER,wraplength=400,height=2)
        lifelineButton = Button(self,command=self.lifeline50,text="Eliminate Option",bg="skyblue1",width=15,height=2,font=("Georgia",12))
        nextButton=Button(self,command=self.check,text="Next",bg="skyblue1",width=16,height=2,font=("Georgia",12))
        endButton = Button(self,command=lambda:(self.controller.show_frame(resultpage),resultpage.showResult(self)),text="END",bg="skyblue1",width=17,height=2,font=("Georgia",12))
        questionLabel.grid(row=1,columnspan=3)
        option1.grid(row=2,columnspan=3)
        option2.grid(row=3,columnspan=3)
        option3.grid(row=4,columnspan=3)
        option4.grid(row=5,columnspan=3)
        lifelineButton.grid(row=7)
        if lifelineCount == 0:
            lifelineButton["state"] = DISABLED
        nextButton.grid(row=7,column=1)
        endButton.grid(row=7,column=2)
    def lifeline50(self):
        global option1,option2,option3,option4,options,oIndex,correctLetter,qIndex,lifelineCount
        tempVar=0
        for i in range(0,4):
            if options[oIndex+i]==correctLetter[qIndex]:
                tempVar = i+1
        temp = random.randint(1,4)
        while temp==tempVar:
            temp = random.randint(1,4)
        if temp==1:
            option1.configure(bg="red")
        elif temp==2:
            option2.configure(bg="red")
        elif temp==3:
            option3.configure(bg="red")
        else:
            option4.configure(bg="red")
        lifelineCount -= 1
        lifelineButton["state"] = DISABLED
    def check(self):
        global qIndex,oIndex,score,checkRandom,count,usernameEntry,total,lifelineButton,endButton
        if optionVar.get()==correctLetter[qIndex]:
            score += 1
        count += 1
        questionLabel.grid_forget()
        option1.grid_forget()
        option2.grid_forget()
        option3.grid_forget()
        option4.grid_forget()
        nextButton.grid_forget()
        lifelineButton.grid_forget()
        endButton.grid_forget()
        while qIndex in checkRandom:
            qIndex = random.randint(0,144)
        checkRandom.append(qIndex)
        oIndex = qIndex*4
        self.viewQuestions()
    
class resultpage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        global scoreLabel1,homeImg,r1,r2,r3,r4,r5,r6
        def emptyEntry3():
            controller.show_frame(homepage)
            r1.deselect()
            r2.deselect()
            r3.deselect()
            r4.deselect()
            r5.deselect()
            r6.deselect()
        homeImg = PhotoImage(file="homeicon.png")
        resultLabel = Label(self, text="RESULT!!", font=("Georgia",35),bg="khaki1",width=15)
        scoreLabel2 = Label(self, text="Your score is:",bg="lightpink1",width=30,height=3,font=("Georgia",16))
        scoreLabel1 = Label(self, text="0", bg="skyblue1",width=20,height=3,font=("Georgia",20))
        leaderboardButton = Button(self, text="Leaderboard",command=lambda:controller.show_frame(leaderboardpage),width=20,height=2,bg="mediumpurple2",font=("Georgia",12))
        homepageButton1 = Button(self,compound=LEFT,command=emptyEntry3,image=homeImg,bd=0)
        homepageButton1.image = homeImg
        resultLabel.pack()
        scoreLabel2.pack()
        scoreLabel1.pack()
        leaderboardButton.pack()
        homepageButton1.pack()   
    def showResult(self):
        global score, scoreLabel1,startButton,j,quiznameLabel
        j=0
        startButton.grid()
        scoreLabel1.configure(text=str(score))
        questionLabel.grid_forget()
        option1.grid_forget()
        option2.grid_forget()
        option3.grid_forget()
        option4.grid_forget()
        nextButton.grid_forget()
        lifelineButton.grid_forget()
        endButton.grid_forget()
        timerLabel.grid_forget()
        quiznameLabel.grid_forget()

class historypage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller
        global showButton,historyFrame,homeImg
        historyFrame = Frame(self)
        showButton = Button(self,text="Show History",command=self.displayHistory)
        homepageButton2 = Button(self,command=self.backToHome,image=homeImg,bd=0)
        homepageButton2.image = homeImg
        showButton.grid(row=1,columnspan=4)
        homepageButton2.grid(row=2,columnspan=4)
    def create_historyTable():
        cursor.execute("Create table if not exists History(username TEXT, category TEXT, score INTEGER, count INTEGER, dateTime TEXT, foreign key (username) references User(username), primary key(username,dateTime))")
        connection.commit()
    def historyData_entries(self,user,categ,sc,ct,dt):
        cursor.execute("Insert into History values(?,?,?,?,?)",(user,categ,sc,ct,dt))
        connection.commit()
    def displayHistory(self):
        global historyFrame,showButton
        historyFrame.grid()
        rows = cursor.execute("Select category, score, count, datetime from History where username=? order by datetime desc",(usernameEntry.get(),))
        i = 4
        historyLabel = Label(historyFrame,text="Your History",font=("helvetica",25))
        historyLabel.grid(row=0,columnspan=4)
        heading1 = Label(historyFrame,text="Category",bd=1,relief=SUNKEN,width=25,bg="SKY BLUE")
        heading1.grid(row=3)
        heading2 = Label(historyFrame,text="Score",bd=1,relief=SUNKEN,width=25,bg="SKY BLUE")
        heading2.grid(row=3,column=1)
        heading3 = Label(historyFrame,text="Questions Attempted",bd=1,relief=SUNKEN,width=25,bg="SKY BLUE")
        heading3.grid(row=3,column=2)
        heading4 = Label(historyFrame,text="Date and Time",bd=1,relief=SUNKEN,width=25,bg="SKY BLUE")
        heading4.grid(row=3,column=3)
        for userhist in rows:
            for j in range(len(userhist)):
                e = Label(historyFrame,text=userhist[j],bd=1,relief=SUNKEN,width=25,bg="WHITE")
                e.grid(row=i,column=j)
            i += 1
        showButton["state"] = DISABLED
    def backToHome(self):
        global historyFrame,showButton
        showButton["state"] = NORMAL
        historyFrame.grid_forget()
        self.controller.show_frame(homepage)
        r1.deselect()
        r2.deselect()
        r3.deselect()
        r4.deselect()
        r5.deselect()
        r6.deselect()

class leaderboardpage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller
        global showButton1,leaderboardFrame,homeImg,leaderboardLabel
        leaderboardFrame = Frame(self)
        showButton1 = Button(self,text="Show Leaderboard",command=self.displayLeaderboard)
        homepageButton3 = Button(self,command=self.backToHome1,image=homeImg,bd=0)
        homepageButton3.image = homeImg
        showButton1.grid(row=1,columnspan=4)
        homepageButton3.grid(row=2,columnspan=4)
        leaderboardLabel = Label(leaderboardFrame,text="",font=("helvetica",25))
        leaderboardLabel.grid(row=0,columnspan=4)
    def displayLeaderboard(self):
        global leaderboardFrame,categoryName,categoryVar,leaderboardLabel
        categoryName = categoryVar.get()
        if categoryName == "":
            categoryName = "Brain Teasers"
        leaderboardFrame.grid()
        leaderboardLabel.grid(row=0,columnspan=4)
        rows = cursor.execute("Select username, score from History where category=? order by score desc",(categoryName,))
        i = 4
        leaderboardLabel.configure(text="Leaderboard: "+categoryName)
        heading1 = Label(leaderboardFrame,text="Rank",bd=1,relief=SUNKEN,width=25,bg="SKY BLUE")
        heading1.grid(row=3)
        heading2 = Label(leaderboardFrame,text="Username",bd=1,relief=SUNKEN,width=25,bg="SKY BLUE")
        heading2.grid(row=3,column=1)
        heading3 = Label(leaderboardFrame,text="Score",bd=1,relief=SUNKEN,width=25,bg="SKY BLUE")
        heading3.grid(row=3,column=2)
        for userscore in rows:
            for j in range(len(userscore)):
                rankLabel = Label(leaderboardFrame, text=i-3,bd=1,relief=SUNKEN,width=25,bg="WHITE")
                rankLabel.grid(row=i)
                e = Label(leaderboardFrame,text=userscore[j],bd=1,relief=SUNKEN,width=25,bg="WHITE")
                e.grid(row=i,column=j+1)
            i += 1                
            if i==19:
                break
        showButton1["state"] = DISABLED
    def backToHome1(self):
        global leaderboardFrame,showButton1,leaderboardLabel
        showButton1["state"] = NORMAL
        leaderboardFrame.grid_forget()
        leaderboardLabel.grid_forget()
        self.controller.show_frame(homepage)
        r1.deselect()
        r2.deselect()
        r3.deselect()
        r4.deselect()
        r5.deselect()
        r6.deselect()

signuppage.create_userTable()
historypage.create_historyTable()
app = quizApp()
app.mainloop()
