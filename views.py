from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.db import connection
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from . import views
from datetime import date

def signup(request):
    if request.method == "POST":
        user_id = request.POST['name']

        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']

        password = request.POST['password']

        cursor = connection.cursor()
        cursor.execute("select * from user_register where user_id ='"+user_id+"' ")
        data = cursor.fetchone()
        if data == None:
            cursor.execute("insert into user_register values('" + user_id + "','" + str(name )+ "','" + str(address) + "','" + str(phone) + "','" + str(email) + "','" +str(password) + "')")
            return redirect("login")
        else:
            return HttpResponse("<script>alert('Usesrname already exixt Please enter a unique Username');window.location='../login';</script>")
            

    return render(request, "sign_up.html")

def profile(request):
    user = request.session["uid"]
    cursor = connection.cursor()
    cursor.execute("select * from user_register where user_id = '"+str(user)+"' ")
    vdata = cursor.fetchone()
    cursor.execute("SELECT team_rate.idteam,team_rate.rate, teams.name,teams.logo FROM team_rate join teams where team_rate.idteam = teams.idteams ")
    rates=cursor.fetchall()
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result ='not published' ")
    matches = cursor.fetchall()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result !='not published' ")
    pmatches = cursor.fetchall()
    return render(request, "profile.html",{'vdata':vdata,'data':cdata, 'matches':matches,'pmatches':pmatches, 'rates':rates})

def update_profile(request):
    if request.method == "POST":
        user_id = request.POST['username']
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        cursor = connection.cursor()
        cursor.execute("update user_register set name='"+str(name)+"', address ='"+str(address)+"', email ='"+str(email)+"', phone ='"+str(phone)+"', password ='"+str(password)+"'  where user_id ='"+str(user_id)+"' ")
        return redirect('profile')
        
    
    

def login(request):
    if request.method == "POST":
        userid = request.POST['userid']
        password = request.POST['password']
        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id= '" + userid + "' AND password = '" + password + "'")
        admin = cursor.fetchone()
        if admin == None:
            cursor.execute("select * from user_register where user_id= '" + userid + "' AND password = '" + password + "'")
            user = cursor.fetchone()
            if user == None:
                messages.error(request, 'Invalid Username Or Password!!')
                return redirect("login")
            else:
                request.session["uid"] = userid
                return redirect('user_home')
                
        else:
            return redirect("admin_home")
    cursor = connection.cursor()
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    cursor.execute("SELECT team_rate.idteam,team_rate.rate, teams.name,teams.logo FROM team_rate join teams where team_rate.idteam = teams.idteams ")
    rates=cursor.fetchall()
    return render(request, "login.html",{'data':cdata,'rates':rates})

def admin_home(request):
    cursor = connection.cursor()
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    return render(request, "admin_home.html",{'data':cdata})

def register_team(request):
    return render(request, "register_team.html")
def add_team(request):
    if request.method == "POST" and request.FILES['upload']:
        name=request.POST['name']
        icon=request.FILES['upload']
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        place = request.POST['place']
        trophy = request.POST['trophy']
        year = request.POST['year']
        cursor = connection.cursor()
        cursor.execute("insert into teams values(null,'" + str(name) + "','" + str(place) + "', '" + str(trophy) + "','"+ str(year) + "', '"+str(icon)+"') ")
        return redirect('view_team')

def view_team(request):
    cursor=connection.cursor()
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    return render (request, "view_team.html", {'data': cdata})

def edit_team(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from teams  where idteams ='"+str(id)+"'")
    cdata = cursor.fetchone()
    return render(request, "edit_team.html", {'data': cdata})

def update_team(request,id):
    if request.method == "POST" and request.FILES['upload']:
        name=request.POST['name']
        icon = request.FILES['upload']
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        place = request.POST['place']
        trophy = request.POST['trophy']
        year = request.POST['year']
        cursor = connection.cursor()
        cursor.execute("update teams set name ='"+str(name)+"' where idteams='"+str(id)+"'")
        cursor.execute("update teams set place ='"+str(place)+"' where idteams='"+str(id)+"'")
        cursor.execute("update teams set number_of_trophy ='"+str(trophy)+"' where idteams='"+str(id)+"'")
        cursor.execute("update teams set start_year ='"+str(year)+"' where idteams='"+str(id)+"'")
        cursor.execute("update teams set logo ='"+str(icon)+"' where idteams='"+str(id)+"' ")
        return redirect('view_team')

def delete_team(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from teams where idteams='" + str(id) + "' ")
    return redirect('view_team')

def register_match(request):
    cursor = connection.cursor()
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    print(cdata)
    return render(request, "register_match.html", {'data': cdata})

def add_match(request):
    if request.method == "POST":
        teamid=request.POST['teamid']
        oteamid = request.POST['oteamid']
        date = request.POST['date']
        result = request.POST['result']
        score1 = request.POST['score1']
        score2 = request.POST['score2']
        cursor = connection.cursor()
        if teamid == oteamid:
            cursor = connection.cursor()
            cursor.execute("select * from teams ")
            cdata = cursor.fetchall()
            print(cdata)
            messages.error(request, "Error!! You Entered Same Team As Opponent. Add Deffrent Team..")
            return render(request,"register_match.html", {'data': cdata})
        else:
            if result == 'team a':
                cursor.execute("select name from teams where idteams = '" + str(teamid) + "' ")
                res = cursor.fetchone()
                res = list(res)
                res = res[0]
                cursor.execute("insert into matches values(null,'" + str(teamid) + "','" + str(oteamid) + "', '" + str(date) + "', '" + str(res) +" win', '" + str(score1) + '-' + str(score2) + "') ")
                return redirect('view_match')
            elif result == 'team b':
                cursor.execute("select name from teams where idteams = '" + str(oteamid) + "' ")
                res = cursor.fetchone()
                res = list(res)
                res = res[0]
                print(res)
                cursor.execute("insert into matches values(null,'" + str(teamid) + "','" + str(oteamid) + "', '" + str(date) + "', '" + str(res) + " win', '" + str(score1) + '-' + str(score2) + "') ")
                return redirect('view_match')
            elif result == 'draw':
                cursor.execute("insert into matches values(null,'" + str(teamid) + "','" + str(oteamid) + "', '" + str(date) + "', 'draw', '" + str(score1) + '-' + str(score2) + "') ")
                return redirect('view_match')
            elif result == 'not published':
                cursor.execute("insert into matches values(null,'" + str(teamid) + "','" + str(oteamid) + "', '" + str(date) + "', 'not published', '" + str(score1) + '-' + str(score2) + "') ")
                return redirect('view_match')
            else:
                return redirect('view_match')

def view_match(request):
    cursor=connection.cursor()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent, m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result ='not published' ")
    matches = cursor.fetchall()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent, m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result !='not published' ")
    pmatches = cursor.fetchall()
    return render(request, "view_matches.html", {'matches': matches,'pmatches':pmatches})


def edit_match(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from matches  where idmatches ='"+str(id)+"'")
    cdata = cursor.fetchone()
    cursor.execute("SELECT  p1.name ,p2.name as opponent FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams  where idmatches ='"+str(id)+"' ")
    cname=cursor.fetchone()
    cursor.execute("select * from teams ")
    rdata = cursor.fetchall()
    return render(request, "edit_match.html", {'row': cdata, 'name': cname, 'data': rdata})

def update_match(request, id):
    if request.method == "POST":
        teamid = request.POST['teamid']
        oteamid = request.POST['oteamid']
        date = request.POST['date']
        result = request.POST['result']
        score = request.POST['score']
        #score2 = request.POST['score2']
        cursor=connection.cursor()
        if teamid == oteamid:
            cursor.execute("select * from teams ")
            cdata = cursor.fetchall()
            print(cdata)
            messages.error(request, "Error!! You Entered Same Team As Opponent. Add Deffrent Team..")
            return render(request, "erroredit_match.html", {'data': cdata})
        else:
            cursor.execute("update matches set idteam='"+str(teamid)+"' where idmatches='"+str(id)+"' ")
            cursor.execute("update matches set opponent='"+str(oteamid)+"' where idmatches='"+str(id)+"' ")
            cursor.execute("update matches set match_date='"+str(date)+"' where idmatches='"+str(id)+"' ")
            cursor.execute("update matches set score='" + str(score)+"' where idmatches='"+str(id)+"' ")

            cursor.execute("update matches set result='" + str(result) + "' where idmatches='" + str(id) + "' ")
            return redirect('view_match')

def delete_match(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from matches where idmatches='" + str(id) + "' ")
    return redirect('view_match')

def tickets(request):
    cursor = connection.cursor()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,ticket_booking.no_of_ticket,ticket_booking.total,ticket_booking.book_date ,p2.name as opponent, ticket_booking.idticket_booking FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams join ticket_booking where m.idmatches = ticket_booking.idmatch")
    tickets = cursor.fetchall()
    print(tickets)
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    return render(request,'all_tickets.html',{'tickets':tickets, 'data':cdata})

def rating(request):
    cursor = connection.cursor()
    cursor.execute("SELECT team_rate.idteam,team_rate.rate, teams.name,teams.logo FROM team_rate join teams where team_rate.idteam = teams.idteams ")
    rates = cursor.fetchall()
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    return render(request, "ratings.html", {'data': cdata, 'rates':rates})

def feedbacks(request):
    cursor = connection.cursor()
    cursor.execute("select * from feedback" )
    feedback=cursor.fetchall()
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    return render(request,"feedbacks.html",{'feedback':feedback,'data': cdata })

def user_home(request):
    cursor = connection.cursor()
    cursor.execute("SELECT team_rate.idteam,team_rate.rate, teams.name,teams.logo FROM team_rate join teams where team_rate.idteam = teams.idteams ")
    rates=cursor.fetchall()
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result ='not published' ")
    matches = cursor.fetchall()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result !='not published' ")
    pmatches = cursor.fetchall()
    return render(request, "user_home.html",{'data':cdata, 'matches':matches,'pmatches':pmatches, 'rates':rates})

def user_team_view(request,id):
    cursor =connection.cursor()
    cursor.execute("select * from teams  where idteams='"+str(id)+"'")
    ddata = cursor.fetchone()
    cursor.execute(
        "SELECT team_rate.idteam,team_rate.rate, teams.name,teams.logo FROM team_rate join teams where team_rate.idteam = teams.idteams ")
    rates = cursor.fetchall()
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    cursor.execute(
        "SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result ='not published' ")
    matches = cursor.fetchall()
    cursor.execute(
        "SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result !='not published' ")
    pmatches = cursor.fetchall()
    return render(request,'usr_team_view.html',{'ddata':ddata,'data':cdata, 'matches':matches,'pmatches':pmatches, 'rates':rates})

def rate(request,id):
    if request.method == "POST":
        cursor = connection.cursor()
        user = request.session["uid"]
        rate = request.POST['rate']
        cursor.execute("select * from rating where user_id= '" + str(user) + "' AND idteam = '" + str(id) + "'")
        exist = cursor.fetchone()
        if exist == None:
            cursor.execute(" insert into rating values( null,'" + str(user) + "','" + str(id) + "','" + str(rate) + "',curdate() ) ")
            cursor = connection.cursor()
            cursor.execute("select * from user_register")
            us = cursor.fetchall()
            n = 0
            for i in us:
                n = n + 1
            max_pers_user = 100 / n
            cursor.execute("select idteams from teams ")
            teams = cursor.fetchall()
            for i in teams:
                l = list(i)
                cursor = connection.cursor()
                cursor.execute("select * from rating where idteam ='" + str(l[0]) + "' and user_rating ='5' ")
                n5 = cursor.fetchall()
                r5 = 0
                for i in n5:
                    r5 = r5 + 1
                v5 = r5 * max_pers_user

                cursor.execute("select * from rating where idteam ='" + str(l[0]) + "' and user_rating ='4' ")
                n4 = cursor.fetchall()
                r4 = 0
                for i in n4:
                    r4 = r4 + 1
                v4 = (r4 * max_pers_user * 4) / 5
                cursor.execute("select * from rating where idteam ='" + str(l[0]) + "' and user_rating ='3' ")
                n3 = cursor.fetchall()
                r3 = 0
                for i in n3:
                    r3 = r3 + 1
                v3 = (r3 * max_pers_user * 3) / 5
                cursor.execute("select * from rating where idteam ='" + str(l[0]) + "' and user_rating ='2' ")
                n2 = cursor.fetchall()
                r2 = 0
                for i in n2:
                    r2 = r2 + 1
                v2 = (r2 * max_pers_user * 2) / 5
                cursor.execute("select * from rating where idteam ='" + str(l[0]) + "' and user_rating ='1' ")
                n1 = cursor.fetchall()
                r1 = 0
                for i in n1:
                    r1 = r1 + 1
                v1 = (r1 * max_pers_user * 1) / 5
                val = v1 + v2 + v3 + v4 + v5
                cursor.execute("select * from team_rate where idteam='" + str(l[0]) + "'")
                yes = cursor.fetchone()
                if yes == None:
                    cursor.execute("insert into team_rate values(null,'" + str(l[0]) + "','" + str(val) + "') ")
                else:
                    cursor.execute("update team_rate set rate ='" + str(val) + "' where idteam ='" + str(l[0]) + "'")
            return redirect('user_home')
        else:
            cursor.execute("update rating set user_rating ='" + str(rate) + "' where idteam='" + str(id) + "' and user_id = '"+str(user)+"' ")
            cursor = connection.cursor()
            cursor.execute("select * from user_register")
            us = cursor.fetchall()
            n = 0
            for i in us:
                n = n + 1
            max_pers_user = 100 / n
            cursor.execute("select idteams from teams ")
            teams = cursor.fetchall()
            for i in teams:
                l = list(i)
                cursor = connection.cursor()
                cursor.execute("select * from rating where idteam ='" + str(l[0]) + "' and user_rating ='5' ")
                n5 = cursor.fetchall()
                r5 = 0
                for i in n5:
                    r5 = r5 + 1
                v5 = r5 * max_pers_user

                cursor.execute("select * from rating where idteam ='" + str(l[0]) + "' and user_rating ='4' ")
                n4 = cursor.fetchall()
                r4 = 0
                for i in n4:
                    r4 = r4 + 1
                v4 = (r4 * max_pers_user * 4) / 5
                cursor.execute("select * from rating where idteam ='" + str(l[0]) + "' and user_rating ='3' ")
                n3 = cursor.fetchall()
                r3 = 0
                for i in n3:
                    r3 = r3 + 1
                v3 = (r3 * max_pers_user * 3) / 5
                cursor.execute("select * from rating where idteam ='" + str(l[0]) + "' and user_rating ='2' ")
                n2 = cursor.fetchall()
                r2 = 0
                for i in n2:
                    r2 = r2 + 1
                v2 = (r2 * max_pers_user * 2) / 5
                cursor.execute("select * from rating where idteam ='" + str(l[0]) + "' and user_rating ='1' ")
                n1 = cursor.fetchall()
                r1 = 0
                for i in n1:
                    r1 = r1 + 1
                v1 = (r1 * max_pers_user * 1) / 5
                val = v1 + v2 + v3 + v4 + v5
                cursor.execute("select * from team_rate where idteam='" + str(l[0]) + "'")
                yes = cursor.fetchone()
                if yes == None:
                    cursor.execute("insert into team_rate values(null,'" + str(l[0]) + "','" + str(val) + "') ")
                else:
                    cursor.execute("update team_rate set rate ='" + str(val) + "' where idteam ='" + str(l[0]) + "'")
            return redirect('user_home')


def book_ticket(request):
    cursor=connection.cursor()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent, m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result ='not published' ")
    matche = cursor.fetchall()
    cursor.execute("SELECT team_rate.idteam,team_rate.rate, teams.name,teams.logo FROM team_rate join teams where team_rate.idteam = teams.idteams ")
    rates = cursor.fetchall()
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result ='not published' ")
    matches = cursor.fetchall()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result !='not published' ")
    pmatches = cursor.fetchall()
    return render(request,'book_match_ticket.html',{'vdata': matche,'data':cdata, 'matches':matches,'pmatches':pmatches, 'rates':rates})

def book(request, id):
    if request.method == "POST":
        request.session["gateidmaster"] = id
        ticket =int(request.POST['ticket'])
        total=int(ticket*150)
        return render(request, "card_gateway.html",{'ticket':ticket, 'total':total})


def card_verify(request):
    id=request.session["gateidmaster"]
    if request.method == "POST":
        card_name = request.POST['card_name']
        card_num = request.POST['card_num']
        total = request.POST['total']
        ticket=request.POST['ticket']
        cvv = request.POST['cvv']
        exp = "11/11/2025"
        user = request.session["uid"]
        cursor = connection.cursor()
        cursor.execute("select * from account where card_no = '" + str(card_num) + "' and cvv = '" + str(cvv) + "' and expiry_date = '" + str(exp) + "' and name = '" + str(card_name) + "'")
        admin = cursor.fetchone()
        if admin == None:
            messages.info(request, "entered values are incorrect. please try again..")
            return redirect('book_ticket')
        else:
            cursor = connection.cursor()
            cursor.execute(" insert into ticket_booking values( null,'" + str(id) + "','" + str(user) + "','" + str(ticket) + "', '" + str(total) + "',curdate() ) ")
            return redirect('booked_tickets')

def booked_tickets(request):
    cursor = connection.cursor()
    user = request.session["uid"]
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,ticket_booking.no_of_ticket,ticket_booking.total,ticket_booking.book_date ,p2.name as opponent FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams join ticket_booking where m.idmatches = ticket_booking.idmatch and ticket_booking.user_id='"+user+"'")
    tickets = cursor.fetchall()
    print(tickets)
    cursor.execute("SELECT team_rate.idteam,team_rate.rate, teams.name,teams.logo FROM team_rate join teams where team_rate.idteam = teams.idteams ")
    rates = cursor.fetchall()
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    cursor.execute(
        "SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result ='not published' ")
    matches = cursor.fetchall()
    cursor.execute(
        "SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result !='not published' ")
    pmatches = cursor.fetchall()
    print(tickets)
    return render(request,'booked_tickets.html',{'tickets':tickets,'data':cdata, 'matches':matches,'pmatches':pmatches, 'rates':rates})



def feedback(request):
    user = request.session["uid"]
    cursor = connection.cursor()
    cursor.execute("SELECT team_rate.idteam,team_rate.rate, teams.name,teams.logo FROM team_rate join teams where team_rate.idteam = teams.idteams ")
    rates = cursor.fetchall()
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result ='not published' ")
    matches = cursor.fetchall()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result !='not published' ")
    pmatches = cursor.fetchall()
    return render(request, "feedback.html", {"user": user,'data':cdata, 'matches':matches,'pmatches':pmatches, 'rates':rates})

def sendfb(request):

    cursor = connection.cursor()
    if request.method == "POST":
        fbdetails = request.POST['fbdetails']
        user=str(request.session["uid"])
        cursor.execute("insert into feedback values( null,'" + str(user) + "', '" + str(fbdetails) + "',curdate() )")
        messages.info(request, "done")
        return redirect("view_fb")

def view_fb(request):
    ser = str(request.session["uid"])
    cursor=connection.cursor()
    cursor.execute("select * from feedback where user_id='"+ser+"' ")
    table=cursor.fetchall()
    table0 = list(table)
    length = len(table0)
    if length == 0:
        value="feedback"
        cursor.execute(
            "SELECT team_rate.idteam,team_rate.rate, teams.name,teams.logo FROM team_rate join teams where team_rate.idteam = teams.idteams ")
        rates = cursor.fetchall()
        cursor.execute("select * from teams ")
        cdata = cursor.fetchall()
        cursor.execute(
            "SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result ='not published' ")
        matches = cursor.fetchall()
        cursor.execute(
            "SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result !='not published' ")
        pmatches = cursor.fetchall()
        return render(request,"no_carts.html",{"val":value,'data':cdata, 'matches':matches,'pmatches':pmatches, 'rates':rates})
    else:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT team_rate.idteam,team_rate.rate, teams.name,teams.logo FROM team_rate join teams where team_rate.idteam = teams.idteams ")
        rates = cursor.fetchall()
        cursor.execute("select * from teams ")
        cdata = cursor.fetchall()
        cursor.execute(
            "SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result ='not published' ")
        matches = cursor.fetchall()
        cursor.execute(
            "SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result !='not published' ")
        pmatches = cursor.fetchall()
        return render(request,"view_fb.html",{"table":table,'data':cdata, 'matches':matches,'pmatches':pmatches, 'rates':rates} )

def user_view_match(request,id):
    cursor=connection.cursor()
    cursor.execute("SELECT m.idmatches, m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where m.idmatches='"+str(id)+"' ")
    match = cursor.fetchone()
    cursor.execute("SELECT team_rate.idteam,team_rate.rate, teams.name,teams.logo FROM team_rate join teams where team_rate.idteam = teams.idteams ")
    rates = cursor.fetchall()
    cursor.execute("select * from teams ")
    cdata = cursor.fetchall()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result ='not published' ")
    matches = cursor.fetchall()
    cursor.execute("SELECT m.idteam ,m.match_date,m.result,m.score, p1.name ,p2.name as opponent,m.idmatches FROM matches m JOIN teams p1 ON m.idteam = p1.idteams JOIN teams p2 ON m.opponent = p2.idteams where result !='not published' ")
    pmatches = cursor.fetchall()

    return render(request,"view_match.html",{"vdata":match,'data':cdata, 'matches':matches,'pmatches':pmatches, 'rates':rates})





