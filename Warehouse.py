from tkinter import *
from tkinter import messagebox
import datetime as dt
from datetime import timedelta 
import sqlite3
class WH:
    c=0;    #Location of the product
    total=0;    #total earning
    def __init__(self):
        self.conn = sqlite3.connect("warehouse.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS PRODUCT(PID VARCHAR(10) ,PTYPE TEXT,WEIGHT NUMERIC,INTIME TEXT,OUTIME TEXT,EXPIRY TEXT,LOCATION NUMERIC);''')
        #self.conn.execute('''DROP TABLE PRODUCT;''')
        self.conn.commit()
    def entry(self,id,wt,ptype,e):
        it=f"{dt.datetime.now():%a, %b %d %Y}"
        et=str(e)+' days'
        ot=f"{(dt.datetime.now()+ timedelta(days=(int(e*0.4)))):%a, %b %d %Y}"    #Shipping few days before expiry
        self.c=self.c+1
        if(ptype=='Frozen Products'):
            self.total=self.total+( 3000 if wt<=100 else 7000)
        elif(ptype=='Perishable'):
            self.total=self.total+( 1000 if wt<=100 else 3000)
        else:
            self.total=self.total+( 4000 if wt<=100 else 9000)
        self.cur.execute("INSERT INTO PRODUCT VALUES(:1,:2,:3,:4,:5,:6,:7)",(id,ptype,wt,it,ot,et,self.c))
        self.conn.commit()
        self.submit()
    def search(self):
        s=StringVar();
        def show():
            self.cur.execute('''SELECT * FROM PRODUCT WHERE PID=(:n) or PTYPE=(:n)''',(s.get(),))
            print('PID    PType\t\tWeight   In-time\t\t  Out-time     \tExpiry     #Container')
            rows = self.cur.fetchall()
            for row in rows:
                print(*row,sep='     ')
        w = Toplevel(root)
        w.geometry('600x550')
        w.title("Warehosue Management System")
        w.configure(bg='lightblue')
        lb= Label(w, text="Warehouse Management Sytem - Search Database",font=("Helvetica",12))
        lb.place(x=100,y=60)
        lb1= Label(w, text="Search Value: ")
        lb1.place(x=100,y=120)
        e1 = Entry(w,textvariable=s).place(x=250,y=120)
        Button(w, text='Search Product',width=10,bg='black',fg='white',command=show).place(x=180,y=180)
        
    def view(self):
        self.cur.execute("SELECT * FROM PRODUCT")
        print('PID    PType\t\tWeight   In-time\t\t  Out-time     \tExpiry     #Container')
        rows = self.cur.fetchall()
        for row in rows:
            print(*row,sep='     ')
    def pending(self):
        pass  
    def account(self):
        w = Toplevel(root)
        w.geometry('600x550')
        w.title("Warehosue Management System")
        w.configure(bg='lightblue')
        lb= Label(w, text="Warehouse Management Sytem  - ACCOUNT",font=("Helvetica",12))
        lb.place(x=100,y=60)
        cost="Product Values: \n Weight: \t\t<=100  \t\t>100 \nFrozen Product\t\t3000\t\t7000\nPerishable\t\t1000\t\t3000\nNon Perishable\t\t4000\t\t9000"
        lb1= Label(w, text=cost).place(x=100,y=220)
        lb2= Label(w, text='Balance:\t\t'+'Rs.\t\t'+str(self.total)).place(x=100,y=120)
    def exit(self):
        copy=o
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
        del copy
    def submit(self):
        var.set("The product has been successfully stored")
        label = Label(root, text="The product has been successfully stored",width=0,height=0).place(x=180,y=500)
def insert():
    o.entry(p.get(),w.get(),v.get(),e.get())
    o.submit()
root = Tk()
root.geometry('600x550')
root.title("Warehosue Management System")
root.configure(bg='lightblue')
o=WH()
Label(root,bg='black',width=800,height=2).place(x=0,y=0)
var = StringVar()
Button(root, text='Entry',width=10,bg='black',fg='white',font=('Helvetica',10,'bold'),command=o.submit).place(x=10,y=5)
Button(root, text='Search',width=10,bg='black',fg='white',font=('Helvetica',10,'bold'),command=o.search).place(x=100,y=5)
Button(root, text='View',width=10,bg='black',fg='white',font=('Helvetica',10,'bold'),command=o.view).place(x=200,y=5)
Button(root, text='Pending',width=10,bg='black',fg='white',font=('Helvetica',10,'bold'),command=o.pending).place(x=300,y=5)
Button(root, text='Exit',width=10,bg='black',fg='white',font=('Helvetica',10,'bold'),command=o.exit).place(x=400,y=5)
Button(root, text='Account',width=10,bg='black',fg='white',font=('Helvetica',10,'bold'),command=o.account).place(x=500,y=5)
entry = Entry(bg='black', fg='white')
lb= Label(root, text="Warehouse Management Sytem",font=("Helvetica",12))
lb.place(x=100,y=60)
lb1= Label(root, text="Product Id")
lb1.place(x=100,y=120)
p=StringVar();e1 = Entry(root,textvariable=p).place(x=250,y=120)
lb2 = Label(root, text="Weight").place(x=100,y=170)
w=IntVar();e2= Entry(root,textvariable=w).place(x=250,y=170)
lb3 = Label(root, text="Product type").place(x=100,y=220)
v = StringVar()
r1="Frozen Products";r2="Perishable";r3="Non Persihable";
Radiobutton(root, text="Frozen Products",value=r1, variable=v, padx = 10).place(x=250,y=220)
Radiobutton(root, text="Perishable", variable=v,value=r2, padx = 10).place(x=250,y=260)
Radiobutton(root, text="Non Persihable",value=r3,variable=v, padx = 10).place(x=250,y=300)
lb3 = Label(root, text="Expiry (in days)").place(x=100,y=350)
e=IntVar()
e3 = Entry(root,textvariable=e).place(x=250,y=350)
Button(root, text='Submit',width=10,bg='black',fg='white',command=insert).place(x=180,y=400)
root.mainloop()
