def main():
    import plotly.graph_objects as go
    import mysql.connector
    from easygui import passwordbox
    passw=passwordbox('input password of mysql')
    try: 
        handle=mysql.connector.connect(host='localhost',user='root',passwd='{}'.format(passw))
    except:
        print("wrong password try again")
    else:
        print(handle)
        c=handle.cursor()
        global y
        print("use the function NO1 to have the required table created")
        print("use the function NO2 to have the required values input")
        print("use the start() function to start the menu program")
            
        def database():
            print()
            x=input('do u want to create database(input in small letters)')
            if x=='yes' or x=='y':
                y=input('enter name')
                c.execute('create database {}'.format(y))
            c.execute('show databases')
            print()
            for i in c:
                for j in i:
                    print(j,end=" ")
                print()
            y=input('select database')
            c.execute('use {}'.format(y))
            c.execute('show tables')
            v=1
            for i in c:
                if i[0]=='users':
                    v=0
            if v==1:
                c.execute('create table users(____________user____________ varchar(30) not NULL primary key, ____password_____ varchar(30))')
        database()
        def chance1():
            z=5
            while z!=0:
                n= passwordbox("What is your ADMIN password ?")
                if n=='SSG':
                    a=input('enter username')
                    password = passwordbox("What is your password ?") # It will ask to enter password and display * on the screen
                    c.execute('select * from users')
                    k=[]
                    for i in c:
                        k.append(i)
                    if len(k)!=0:
                        for i in k:
                            if i[0]!=a:
                                print('inputted')
                                c.execute('insert into users values("{}","{}")'.format(a,password))
                                handle.commit()
                                break
                            else:
                                print('username already exists')
                                chance1()
                    else:
                        c.execute('insert into users values("{}","{}")'.format(a,password))
                        handle.commit()
                    x=input('do you want to add user again')
                    if x=='yes' or x=='y':
                        chance1()
                    z=0
                else:
                    z=z-1
                    print('wrong password try again')
                    print('attempts left=',z)
        o=input('do you want to add user')
        if o=='yes' or o=='y':
            chance1()
        
        def showtables():
            c.execute('show tables')
            for i in c:                                                                 #a user defined function for printing the tables present in the database
                for j in i:
                    print(j,end=" ")
                print()                                                                          

        def showcolumns(x):
            c.execute('show columns from {}'.format(x))
            global l                                                                    #this code seemed to repeat at numerous user defined functions
            l=[]                                                                        #So again this is a user defined function which create a list "l"
            global records                                                              #which has the names of different columns as elements
            records=c.fetchall()
            for i in records:
                l.append(i[0])


        def display():
            print()
            list2=[]                                            
            for i in c:
                L=[]
                for j in i:
                    L.append(j)
                list2.append(L)
        
            for i in range(len(list2)):                                                 #this part of code mainly focuses on printing each column downwards
                for j in range(len(list2[i])):                                          #with putting the mark ":" after a number of spaces to align with header
                    if j==(len(l)-1):                                                   #for that purpose, the code print(list2[i][j]," "*((len(str(l[j]))-2)-len(str(list2[i][j]))),':',end='')
                        print(list2[i][j])                                              #basically does the function of printing ":" after spaces by 
                    else:                                                               #calculating the number of spaces required to left to add by subtracting 
                        print(list2[i][j]," "*((len((l[j]))-2)-len((list2[i][j]))),':',end='')
                print()                                                                 #the lengths of header-2 from the length of each column of each row!!!
            print()


        def DISPLAY():
            showtables()
            global b
            b=input('enter table name')
            if b.lower()!='users':
                showcolumns(b)
                list2=[]
                list1=l
                e=':'.join(list1)
                print(e)
                c.execute('select * from {}'.format(b))
                display()
            else:
                print("cant print password table")
                DISPLAY()


        def FILTERSEARCH():
            DISPLAY()
            print(l)
            command=[]
            p=int(input('number of columns u want to select'))
            f=[]
            while p!=0:
                t=input('enter column name')
                if t in l:
                    f.append(t)
                    p=p-1
                else:
                    print('not a column')
            for i in f:
                newl=[]
                a=''
                q=f.index(i)
                while a.lower()!='0':                                                         #this function basically need to get user input values for the same
                    d=input('enter {}'.format(i))                                   #column name again and again until user tells it stop
                    if records[q][1]==b'int':                                       #this need to be done for each column and hence the while and for loop
                        if d!="":                                                   #however there is a for loop for intendation purposes
                            newl.append(i+'='+d)
                    elif records[q][1]==b'float':
                        if d!="":
                            newl.append(i+'>'+d)                                    #append function basically appends "columnname>minimumvalue"
                    elif records[q][1]==b'date':                                    #for date and integer espicially as always we do such operation for
                        if d!="":                                                   #such column types
                            newl.append(i+'>='+d)
                    elif d!='':                                                     #for string column types append function appends 
                        newl.append(i+'='+d)                                        #columnname=input value
                    a=(input('enter 0 to stop'))
                str1=" or ".join(newl)
                z='('+str1+')'                                                      
                if z!='()':                                                             
                    command.append(z)
            m=" and ".join(command)
            showcolumns(b)
            list2=[]
            list1=l
            e=':'.join(list1)
            print(e)
            print()
            try:
                c.execute("select * from {} where ({})".format(b,m))
                display()
            except:
                print('DATA    IN     DOUBLE    QUOTES    PLEASE!!!')
                FILTERSEARCH()

                
        def REMOVE():
            showtables()
            b=input('enter table name')
            if b.lower()!='users':
                showcolumns(b)                                                              #takes the table name, prints the column name appropriately
                list2=[]                                                                    #then fixes the required statement to be inserted in c.execute(....)
                list1=l                                                                     #by input from user and then to display such a change is made DISPLAY() is called
                e=':'.join(list1)                                                           #references to FILTERSEARCH() on how the statement is made to be inserted
                print(e)
                c.execute('select * from {}'.format(b))
                display()
                showcolumns(b)
                command=[]
                for i in range(len(l)):
                    d=input('enter {}'.format(l[i]))
                    if records[i][1]==b'int' or records[i][1]==b'float':
                        if d!="":
                            command.append(l[i]+'='+d)
                    elif records[i][1]==b'date':
                        if d!="":
                            command.append(l[i]+'='+d)    
                    elif d!='':
                        command.append(l[i]+'='+d)
                str1=" or ".join(command)
                try:
                    c.execute("delete from {} where {}".format(b,str1))
                    DISPLAY()
                    handle.commit()
                except:
                    handle.rollback()
                    print()
                    print('GIVE DATA IN DOUBLE QUOTES')
                    print()
                    REMOVE()


                
        def UPDATE():
            showtables()
            b=input('enter table name')
            if b.lower()!='users':
                showcolumns(b)
                list2=[]                                                                    #set value and where value is input from user and appropriately inserted to 
                list1=l                                                                     #c.execute(.....)
                e=':'.join(list1)
                print(e)
                c.execute('select * from {}'.format(b))
                display()
                SET=input('enter set clause statement (column_name=value)')
                where=input('enter where clause statement (column_name=value)')
                print("update {} set ({}) where {}".format(b,SET,where))
                try:
                    c.execute("update {} set {} where {}".format(b,SET,where))
                    DISPLAY()
                    handle.commit()
                except:
                    print('error',"\n")
                    UPDATE()


        def search():
            showtables()
            b=input('enter table name')
            showcolumns(b)
            print(l)
            h=input('enter table column to search')
            k=input("searching ")
            list2=[]
            list1=l
            e=':'.join(list1)
            print(e)
            
            if b.lower()!='users':
                    try:
                        if h in l:
                            c.execute("select * from {} where {} LIKE '%{}%'".format(b,h,k))
                            display()
                    except:
                        print()
                        print('error. try again')
                        search()
            else:
                print('try again')
                search()
                    
                    
                    
        def DTABLE():
            showtables()
            x=input('enter table')
            if x.lower()!='users':
                showcolumns(x)
                L=[]
                c.execute('select * from {}'.format(x))
                n=0
                for i in c:
                    q=[]
                    for j in i:
                        q.append(j)
                    L.append(q)
                data=[]
                kl=[]
                c.execute('select * from {}'.format(x))
                s=[]
                for i in c:
                    n=n+1
                for i in range(len(l)):
                    s.append(i)
                    r=int(input('enter column width for {}'.format(l[i])))
                    kl.append(r)
                    q=[]
                    for j in range(n):
                        q.append(L[j][i])
                    data.append(q)
                colour='''aliceblue, antiquewhite, aqua, aquamarine, azure,beige, bisque, black, blanchedalmond, blue,blueviolet, brown,
                burlywood, cadetblue,chartreuse, chocolate, coral, cornflowerblue,cornsilk, crimson, cyan, darkblue, darkcyan,darkgoldenrod,
                darkgray, darkgrey, darkgreen,darkkhaki, darkmagenta, darkolivegreen, darkorange,darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,darkturquoise, darkviolet, deeppink, deepskyblue,dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,ghostwhite, gold, goldenrod, gray, grey, green,greenyellow, honeydew, hotpink, indianred,
                indigo,ivory, khaki, lavender, lavenderblush, lawngreen,lemonchiffon, lightblue, lightcoral, lightcyan,lightgoldenrodyellow, lightgray,
                lightgrey,lightgreen, lightpink, lightsalmon, lightseagreen,lightskyblue, lightslategray, lightslategrey,lightsteelblue, lightyellow, lime,
                limegreen,linen, magenta, maroon, mediumaquamarine,mediumblue, mediumorchid, mediumpurple,mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,mintcream, mistyrose, moccasin, navajowhite, navy,oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,palevioletred, papayawhip, peachpuff, peru, pink,plum, powderblue, purple, red, rosybrown,
                royalblue, rebeccapurple, saddlebrown, salmon,sandybrown, seagreen, seashell, sienna, silver,skyblue, slateblue, slategray, slategrey, snow,
                springgreen, steelblue, tan, teal, thistle, tomato,turquoise, violet, wheat, white, whitesmoke,yellow, yellowgreen'''
                print()
                print(colour)
                print()
                A=input('enter color for header')
                B=input('enter color for cells')
                E=input('enter header font colour')
                F=input('enter cell font color ')
                fig = go.Figure(data=[go.Table(
                    columnorder = s,
                    columnwidth = kl,
                    header=dict(
                        values=l,
                        line_color='black',
                        fill_color=A,
                        align='center',
                        font=dict(color=E, size=25),
                        height=40
                        ),
                    cells=dict(
                        values=data,
                        line_color='black',
                        fill_color = B,
                        align ='left',
                        font = dict(color = F, size = 20),
                        height=30
                        ))
                                      ])
                

                fig.show()
            else:
                print('try again')
                DTABLE()
        def usecreate1():
            c.execute("create table movie(SLNO integer not NULL primary key,list______________of______________movies varchar(80), Genre___of___movie varchar(20), date___released date, rating___of___movie float, type___of___movie varchar(20), Language__of__movie varchar(20))")
            c.execute("create table Clients(SLNO integer not NULL primary key,Clients_having_sub varchar(30), Age_of_clients integer, Subscription varchar(20),cost integer)")
            handle.commit()
        def CREATE():
            x=input('enter table name')
            y=int(input('enter number of columns'))
            l=[]
            for i in range(y):
                a=input('enter column name')
                b=input('enter type')
                if b.lower()=='varchar' or b.lower()=='char':
                    h=int(input('enter char/varchar limit'))
                    d="{} {}({})".format(a,b,h)
                    l.append(d)
                    
                d="{} {}".format(a,b)
                l.append(d)
            sr=','.join(l)
            print(sr)
            c.execute('create table {}({})'.format(x,sr))
                
            
        def input1():
            y=0
            showtables()
            b=input('enter table name')
            showcolumns(b)
            a=1
            c.execute('select * from {}'.format(b))
            for i in c:
                y=y+1
            print(y)
            c.execute("desc {}".format(b))
            L=[]
            for i in c:
                m=[]
                for j in i:
                    m.append(j)
                L.append(m)
            while(a!=0):
                d={"Premium":799,"Standard":649,"Basic":499,"Mobile":199}
                y=y+1
                z=['{}'.format(y)]
                for i in l:
                    j=l.index(i)
                    if i=='SLNO':
                        pass
                    elif L[j][1]==b'int':
                        t=(input('enter table values for column {} of data type ({})'.format(i,L[j][1])))    
                        z.append(t)
                    else:
                        print('enter in double quotes')
                        if L[j][0]=='Subscription':
                            print(d)
                        t=input('enter table values for column {} of data type ({})'.format(i,L[j][1]))
                        z.append(t)
                s=','.join(z)
                c.execute('insert into {} values({})'.format(b,s))
                handle.commit()
                a=int(input('enter 1 to stop'))
                if a==1:
                    break

        def start():
            s=0
            while s==0:
                print()
                print("MENU")
                print("OPTIONS")
                print("1. CREATE ONCE","2. INPUT ONCE","3. INPUT EACH RECORD","4. DISPLAY","5.FILTER SEARCH","6.REMOVE","7. UPDATE","8. SEARCH",'9. DISPLAY AS TABLE','10. CREATE A NEW TABLE','11. QUIT',sep="\n")
                ch=int(input("enter option (1-11)"))
                if ch==1:
                    usecreate1()
                elif ch==2:
                    useinput1()
                elif ch==3:
                    input1()
                elif ch==4:
                    DISPLAY()
                elif ch==5:
                    FILTERSEARCH()
                elif ch==6:
                    REMOVE()
                elif ch==7:
                    UPDATE()
                elif ch==8:
                    search()
                elif ch==9:
                    DTABLE()
                elif ch==10:
                    CREATE()
                elif ch==11:
                    break
                else:
                    print("wrong input")
                    start()
        def useinput1():
            c.execute("insert into movie values(1,'the Avengers', 'SCI-FI','2011-05-04', 8.0, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(2,'Avengers 4', 'SCI-FI','2019-04-26', 8.4, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(3,'Iron Man 1', 'SCI-FI','2008-05-02', 7.9, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(4,'Iron Man 2', 'SCI-FI','2010-05-07', 7.0, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(5,'Iron Man 3', 'SCI-FI','2013-05-03', 7.2, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(6,'Captain America 1', 'SCI-FI','2011-07-22', 6.9, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(7,'Captain America 2', 'SCI-FI','2014-04-04', 7.7, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(8,'Captain America 3', 'SCI-FI','2016-05-06', 7.8, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(9,'Thor 2', 'SCI-FI','2013-11-08', 6.9, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(10,'Thor 1', 'SCI-FI','2011-05-06', 7.0, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(11,'Thor 3', 'SCI-FI','2017-11-03', 7.9, 'MOVIE', 'ENGLISH')")          
            c.execute("insert into movie values(12,'Increadible Hulk', 'SCI_FI','2008-06-13', 6.7, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(13,'Avengers 2', 'SCI-FI','2015-02-01', 8.0, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(14,'Avengers 3', 'SCI-FI','2018-04-27', 8.4, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(15,'Doctor Strange', 'SCI-FI','2016-11-04', 7.5, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(16,'Spiderman 1', 'SCI-FI','2017-07-07', 7.4, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(17,'Spiderman 2', 'SCI-FI','2019-07-02', 7.5, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(18,'Spiderman Into The Spider-verse', 'SCI-FI','2018-12-14', 8.4, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(19,'Guardians Of The Galaxy', 'SCI-FI','2014-08-01', 8.4, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(20,'Guardians Of The Galaxy 2', 'SCI-FI','2019-05-018', 7.6, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(21,'Captain Marvel', 'SCI-FI','2019-03-08', 6.9, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(22,'Stranger Things', 'Drama','2016-06-09', 8.8, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(23,'Ozark', 'Crime','2017-05-18', 8.4, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(24,'The Crown', 'Drama','2016-04-23', 8.7, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(25,'Money Heist', 'ACTION','2017-06-07', 8.4, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(26,'The Witcher', 'ACTION','2019,-12-19', 8.2, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(27,'Black Mirror', 'Drama', '2011,-03-27', 8.8, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(28,'Designated Survivor', 'ACTION', '2016-01-22', 7.5, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(29,'Good Girls', 'Comedy', '2018-07-23', 7.9, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(30,'Riverdale', 'Crime', '2018-07-23', 7.9, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(31,'13 Reasons Why', 'Drama','2017-04-22', 7.7, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(32,'The Good Place', 'Comedy', '2016-03-16', 8.2, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(33,'The Irishman', 'Crime','2019-07-19', 7.9, 'Movie', 'ENGLISH')")
            c.execute("insert into movie values(34,'extraction', 'ACTION', '2020-12-12', 6.7, 'MOVIE', 'ENGLISH')")
            c.execute("insert into movie values(35,'Anne With an e', 'Drama','2017-07-19', 8.7, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(36,'The Punisher', 'ACTION','2017-09-10', 8.5, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(37,'Grace AND Frakie', 'Comedy','2015-07-19', 8.3, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(38,'Sense 8', 'Drama','2015-11-16', 8.4, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(39,'narcos mexico', 'Crime','2018-02-19', 8.4, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(40,'Atypical', 'Comedy','2017-01-12', 8.3, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(41,'Sacred Games', 'ACTION', '2018-02-19', 8.7, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(42,'Iron Fist', 'ACTION', '2017-11-17', 6.5, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(43,'Like Cage', 'ACTION','2016-12-16', 7.3, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(44,'Hemlock Grov', 'Drama','2013-11-09', 7.1, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(45,'Cable Girls', 'Drama','2017-09-29', 7.7, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(46,'Narcos', 'Crime', '2015-09-19', 8.8, 'tvshow', 'ENGLISH')")
            c.execute("insert into movie values(47,'Mind Hunter', 'Crime','2017-11-21', 8.6, 'tvshow', 'ENGLISH')")
            c.execute("insert into Clients values(1,'Kavin', 17, 'Mobile', 199)")
            c.execute("insert into Clients values(2,'Pranav K', 17, 'Basic', 499)")
            c.execute("insert into Clients values(3,'Rishin', 17, 'Standard', 649)")
            c.execute("insert into Clients values(4,'Neeraj', 17, 'Premium', 799)")
            c.execute("insert into Clients values(5,'Adwyth',17,'Standard',649)")
            c.execute("insert into Clients values(6,'Alna',17,'Basic',499)")
            c.execute("insert into Clients values(7,'Maria',17,'Premium',799)")
            c.execute("insert into Clients values(8,'Rohith',17, 'Basic',499)")
            c.execute("insert into Clients values(9,'Santanu',17, 'Premium',799)")
            c.execute("insert into Clients values(10,'Aatish',17,'Standard',649)")
            c.execute("insert into Clients values(11,'Aparna',17,'Standard',649)")
            c.execute("insert into Clients values(12,'Kavya',17, 'Premium',799)")
            c.execute("insert into Clients values(13,'Nabhan',17, 'Basic',499)")
            c.execute("insert into Clients values(14,'Nandana',17, 'Mobile',199)")
            c.execute("insert into Clients values(15,'Nia',17, 'Premium',799)")
            c.execute("insert into Clients values(16,'Ann',17, 'Basic',499)")
            c.execute("insert into Clients values(17,'Pranav R',17,'Standard',649)")
            c.execute("insert into Clients values(18,'Prithish',17, 'Premium',799)")
            c.execute("insert into Clients values(19,'Stephin',17, 'Premium',799)")
            c.execute("insert into Clients values(20,'Govind',17, 'Premium',799)")
            handle.commit()
        for i in (0,20):
            print()
        c.execute('select * from users')
        w=[]
        for i in c:
            w.append(i)
        
        u=0
        v=5
        tr=1
        while v!=0:
            a=input('enter username for entering into program')
            password = passwordbox("What is your password ?")
            for i in w:
                if i[0]==a and i[1]==str(password):
                    u=1
                    v=0
                    start()
                else:
                    pass
            
            if u==0:
                if v!=0:
                    v=v-1
                    if v==0:
                        tr=v
                    print('chance left: ',v)
                    print('Try again')
        if tr==0:
            print('chance are over')
    finally:
        print('--------------------------------------------------------------------------------------------------------------------------------------')
        print('thank you')
main()
print('to try again use main() function')

