from tkinter import *
import requests
import bs4
from tkinter.scrolledtext import *
from tkinter.messagebox import *
from sqlite3 import *
import matplotlib.pyplot as plt


def exit_plt(event):
	plt.close()
# ADD Button
def f1():
	add_window.deiconify()
	add_window_ent_rno.focus()
	main_window.withdraw()
# Back Button --> ADD
def f2():
	main_window.deiconify()
	add_window.withdraw()
# VIEW Button
def f3():
	view_window.deiconify()
	main_window.withdraw()
	view_window_st_data.delete(1.0,END)
	info=""
	con=None
	try:
		con=connect('sms.db')
		cursor=con.cursor()
		sql="select * from student order by rno asc"
		cursor.execute(sql)
		data=cursor.fetchall()
		for d in data:
			info=info+ " Roll No: "+ str(d[0]) + " Name: " + str(d[1]) + " Marks: "+ str(d[2]) + "\n"
		view_window_st_data.insert(INSERT,info)
	except OperationalError:
		showerror("Failure","Error Connecting DataBase")
	finally:
		if con is not None:
			con.close()
# Back Button --> View
def f4():
	main_window.deiconify()
	view_window.withdraw()

# Save Button --> ADD
def f5():
	con =None
	try:
		con=connect('sms.db')
		cursor=con.cursor()
		sql= "insert into student values('%d','%s','%d')"
		if not add_window_ent_rno.get():
			raise Exception("Roll No should Not be Empty")
		elif not add_window_ent_rno.get().isdigit():
			raise Exception("Roll No should be Positive Integer Only")
		elif  int(add_window_ent_rno.get())<0:
			raise Exception("Roll No should be Positive Integer Only")
		elif  not add_window_ent_name.get():
			raise Exception("Name should Not be Empty")
		elif not add_window_ent_name.get().isalpha():
			raise Exception("Name should Contain Alphabets only")
		elif len(add_window_ent_name.get()) < 2:
			raise Exception("Enter Valid Name")
		elif not add_window_ent_marks.get():
			raise Exception("Marks should Not be Empty")
		elif int(add_window_ent_marks.get()) < 0 or int(add_window_ent_marks.get()) > 100:
			raise Exception("Enter Valid Marks")
		else:
			rno=int(add_window_ent_rno.get())
			name=add_window_ent_name.get()
			marks=int(add_window_ent_marks.get())
		cursor.execute(sql % (rno,name,marks))
		con.commit()
		showinfo('Success', ' Record added')
	except IntegrityError:
		showerror('Failure','Roll No. Already Exists')
		con.rollback()
	except OperationalError:
		showerror("Failure","Error Connecting DataBase")
		con.rollback()
	except Exception as e:
		showerror('Failure',e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
		add_window_ent_name.delete(0,END)
		add_window_ent_rno.delete(0,END)
		add_window_ent_marks.delete(0,END)
		add_window_ent_rno.focus()

# Delete Button --> DELETE
def f6():
	con=None
	try:
		con=connect("sms.db")
		cursor=con.cursor()
		sql= "delete from student where rno='%d'"
		if not delete_window_ent_rno.get():
			raise Exception("Roll No should Not be Empty")
		elif not delete_window_ent_rno.get().isdigit():
			raise Exception("Roll No should be Positive Integer Only")
		elif  int(delete_window_ent_rno.get())<0:
			raise Exception("Roll No should be Positive")
		else:
			rno=int(delete_window_ent_rno.get())
		cursor.execute(sql % (rno))
		if cursor.rowcount > 0:
			showinfo('Success','Record Deleted')
			con.commit()
		else:
			showerror('Failure','Record does not Exist')
	except OperationalError:
		showerror("Failure","Error Connecting DataBase")
		con.rollback()
	except Exception as e:
		showerror("issue ",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
			delete_window_ent_rno.delete(0,END)
			delete_window_ent_rno.focus()

# DELETE Button
def f7():
	delete_window.deiconify()
	delete_window_ent_rno.focus()
	main_window.withdraw()

# Back Button --> DELETE
def f8():
	main_window.deiconify()
	delete_window.withdraw()

# Update Button --> UPDATE
def f9():
	con=None
	try:
		con=connect("sms.db")
		cursor=con.cursor()
		sql= "update student set name='%s', marks='%d' where rno='%d'"
		if not update_window_ent_rno.get():
			raise Exception("Roll No should Not be Empty")
		elif not update_window_ent_rno.get().isdigit():
			raise Exception("Roll No should be Positive Integer Only")
		elif  int(update_window_ent_rno.get())<0:
			raise Exception("Roll No should be Positive")
		elif  not update_window_ent_name.get():
			raise Exception("Name should Not be Empty")
		elif not update_window_ent_name.get().isalpha():
			raise Exception("Name should Contain Alphabets only")
		elif len(update_window_ent_name.get()) < 2:
			raise Exception("Enter Valid Name")
		elif not update_window_ent_marks.get():
			raise Exception("Marks should Not be Empty")
		elif int(update_window_ent_marks.get()) < 0 or int(update_window_ent_marks.get()) > 100:
			raise Exception("Enter Valid Marks")
		else:
			rno=int(update_window_ent_rno.get())
			name=update_window_ent_name.get()
			marks=int(update_window_ent_marks.get())
		cursor.execute(sql % (name,marks,rno))
		if cursor.rowcount > 0:
			showinfo("Success","Record updated")
			con.commit()
		else:
			showerror("Failure","Record does not exist ")
	except OperationalError:
		showerror("Failure","Error Connecting DataBase")
		con.rollback()
	except Exception as e:
		showerror("Failure ",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
			update_window_ent_name.delete(0,END)
			update_window_ent_rno.delete(0,END)
			update_window_ent_marks.delete(0,END)
			update_window_ent_rno.focus()

# UPDATE Button
def f10():
	update_window.deiconify()
	update_window_ent_rno.focus()
	main_window.withdraw()

# Back Button --> UPDATE
def f11():
	main_window.deiconify()
	update_window.withdraw()

# CHARTS Button
def f12():
	from matplotlib.widgets import Button
	con=None
	try:
		rnos=[]
		marks=[]
		con=connect("sms.db")
		cursor=con.cursor()
		sql="select * from  student order by rno asc"
		cursor.execute(sql)
		data= cursor.fetchone()	
		while data:
			rnos.append(str(data[0]))
			marks.append(int(data[2]))
			data=cursor.fetchone()
		plt.bar(rnos,marks,color=['red','green'])
		plt.title("Batch Information")
		plt.xlabel("Roll No")
		plt.ylabel("Marks")
		axButton=plt.axes([0.8,0.01,0.1,0.05])
		btn=Button(axButton,'BACK')
		btn.on_clicked(exit_plt)
		mng = plt.get_current_fig_manager()
		mng.window.state("zoomed")
		plt.show()
	except OperationalError:
		showerror("Failure","Error Connecting DataBase")
	finally:
		if con is not None:
			con.close()
# EXIT Button
def f13():
	if askokcancel("Quit","Do You Want to Exit?"):
		main_window.destroy()

def f14():
	con=None
	try:
		con= connect("sms.db")
		cursor= con.cursor()
		sql="create table student(rno int primary key, name text,marks int)"
		cursor.execute(sql)
		showinfo("Success","DataBase Created")
	except Exception as e:
		showerror("Failure","DataBase Already Created")
	finally:
		if con is not None:
			con.close()

# Qoute Of the Day Logic
try:
	wa="https://www.brainyquote.com/quote_of_the_day"
	res=requests.get(wa)
	
	data=bs4.BeautifulSoup(res.text,'html.parser')

	info=data.find('img',{'class':'p-qotd'})
	
	qotd=info['alt']
except Exception as e:
	qotd="Some Error Occurred"

# Location Logic
try:
	wa = "https://ipinfo.io/"
	res = requests.get(wa)
	data= res.json()
	loc= data['city']

except Exception as e:
	loc="Error"

# Temperature Logic
try:
	city_name=loc
	a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2="&q=" + city_name
	a3="&appid=" + "8324d016f544191cd290001ff9108582"
	
	wa = a1 + a2 + a3
	res=requests.get(wa)
	data=res.json()
	main=data['main']
	temp=str(main['temp'])
except Exception as e:
	temp="Error"

# INTRO
splash=Tk()
splash.after(4000,splash.destroy)
splash.wm_attributes('-fullscreen','true')
splash.configure(background='cyan')
msg=Label(splash,text="\n \n \n Student Management System \n By \n Amaan Shaikh",font=('Calibri',50,'bold'),fg='blue',bg='cyan')
msg.pack()
splash.mainloop()

# MAIN WINDOW
main_window=Tk()
main_window.title("S.M.S")
main_window.wm_attributes("-fullscreen",'true')
#main_window.geometry("700x700+450+10")
main_window.configure(background="darkseagreen1")

f=('Consolas',25,'bold')
main_window_btn_create=Button(main_window,text="Create DataBase",font=f,width=20,command=f14,background="palegreen")
main_window_btn_add=Button(main_window,text="ADD",font=f,width=20,command=f1,background="palegreen")
main_window_btn_view=Button(main_window,text="View",font=f,width=20,command=f3,background="palegreen")
main_window_btn_update=Button(main_window,text="Update",font=f,width=20,command=f10,background="palegreen")
main_window_btn_delete=Button(main_window,text="Delete",font=f,width=20,command=f7,background="palegreen")
main_window_btn_charts=Button(main_window,text="Charts",font=f,width=20,command=f12,background="palegreen")
main_window_btn_exit=Button(main_window,text="Exit",font=f,width=20,command=f13,background="palegreen")

main_window_lbl1=Label(main_window,text="Location:"+loc+" Temp:"+temp+"\u00B0C",font=f,borderwidth=2, relief="groove",background="palegreen")
main_window_lbl2=Label(main_window,text="QOTD:"+qotd,font=('Consolas',25,'bold'),borderwidth=2, relief="groove",background="palegreen",wraplength=1500)

main_window_btn_create.pack(pady=10)
main_window_btn_add.pack(pady=10)
main_window_btn_view.pack(pady=10)
main_window_btn_update.pack(pady=10)
main_window_btn_delete.pack(pady=10)
main_window_btn_charts.pack(pady=10)
main_window_btn_exit.pack(pady=10)
main_window_lbl1.pack(pady=20)
main_window_lbl2.pack(pady=20)

# ADD WINDOW
add_window=Toplevel(main_window)
add_window.title("Add Student")
#add_window.geometry("700x700+450+10")
add_window.wm_attributes("-fullscreen",'true')
add_window.configure(background="SlateGray1")

add_window_lbl_rno=Label(add_window,text="Enter Roll No",font=f,background="SlateGray1")
add_window_ent_rno=Entry(add_window,font=f,bd=2)
add_window_lbl_name=Label(add_window,text="Enter Name",font=f,background="SlateGray1")
add_window_ent_name=Entry(add_window,font=f,bd=2)
add_window_lbl_marks=Label(add_window,text="Enter Marks",font=f,background="SlateGray1")
add_window_ent_marks=Entry(add_window,font=f,bd=2)
add_window_btn_save=Button(add_window,text="SAVE",font=f,command=f5,background="skyblue",width=20)
add_window_btn_back=Button(add_window,text="BACK",font=f,command=f2,background="skyblue",width=20)

add_window_lbl_rno.pack(pady=10)
add_window_ent_rno.pack(pady=10)
add_window_lbl_name.pack(pady=10)
add_window_ent_name.pack(pady=10)
add_window_lbl_marks.pack(pady=10)
add_window_ent_marks.pack(pady=10)
add_window_btn_save.pack(pady=10)
add_window_btn_back.pack(pady=10)
add_window.withdraw()

# VIEW WINDOW
view_window=Toplevel(main_window)
view_window.title("View Student")
#view_window.geometry("700x700+450+10")
view_window.wm_attributes("-fullscreen",'true')
view_window.configure(background="lightyellow")

view_window_st_data=ScrolledText(view_window,width=40,height=15,font=f)
view_window_btn_back=Button(view_window,text="BACK",font=f,command=f4,background="khaki",width=20)
view_window_st_data.pack(pady=10)
view_window_btn_back.pack(pady=10)
view_window.withdraw()

# UPDATE WINDOW
update_window=Toplevel(main_window)
update_window.title("Update Student")
#update_window.geometry("700x700+450+10")
update_window.wm_attributes("-fullscreen",'true')
update_window.configure(background="lavenderblush2")

update_window_lbl_rno=Label(update_window,text="Enter Roll No",font=f,background="lavenderblush2")
update_window_ent_rno=Entry(update_window,font=f,bd=2)
update_window_lbl_name=Label(update_window,text="Enter Name",font=f,background="lavenderblush2")
update_window_ent_name=Entry(update_window,font=f,bd=2)
update_window_lbl_marks=Label(update_window,text="Enter Marks",font=f,background="lavenderblush2")
update_window_ent_marks=Entry(update_window,font=f,bd=2)
update_window_btn_save=Button(update_window,text="UPDATE",font=f,command=f9,background="MistyRose2",width=20)
update_window_btn_back=Button(update_window,text="BACK",font=f,command=f11,background="MistyRose2",width=20)

update_window_lbl_rno.pack(pady=10)
update_window_ent_rno.pack(pady=10)
update_window_lbl_name.pack(pady=10)
update_window_ent_name.pack(pady=10)
update_window_lbl_marks.pack(pady=10)
update_window_ent_marks.pack(pady=10)
update_window_btn_save.pack(pady=10)
update_window_btn_back.pack(pady=10)
update_window.withdraw()

# DELETE WINDOW
delete_window=Toplevel(main_window)
delete_window.title("Delete Student")
#delete_window.geometry("700x700+450+10")
delete_window.wm_attributes("-fullscreen",'true')
delete_window.configure(background="SlateGray1")

delete_window_lbl_rno=Label(delete_window,text="Enter Roll No",font=f,background="SlateGray1")
delete_window_ent_rno=Entry(delete_window,font=f,bd=2)
delete_window_btn_save=Button(delete_window,text="DELETE",font=f,command=f6,background="skyblue",width=20)
delete_window_btn_back=Button(delete_window,text="BACK",font=f,command=f8,background="skyblue",width=20)

delete_window_lbl_rno.pack(pady=10)
delete_window_ent_rno.pack(pady=10)
delete_window_btn_save.pack(pady=10)
delete_window_btn_back.pack(pady=10)
delete_window.withdraw()

main_window.protocol("WM_DELETE_WINDOW",f13)
add_window.protocol("WM_DELETE_WINDOW",f13)
view_window.protocol("WM_DELETE_WINDOW",f13)
update_window.protocol("WM_DELETE_WINDOW",f13)
delete_window.protocol("WM_DELETE_WINDOW",f13)

main_window.mainloop()
