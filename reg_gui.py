import csv
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class main_app:
    @classmethod
    def update_record(cls, all_members):
        with open('.\\accounts_temp.csv', 'w', newline='') as temp_file:
            writer = csv.writer(temp_file)
            for i in all_members:
                writer.writerow([all_members[i]['lastname'], all_members[i]['firstname'], i,
                                 all_members[i]['password'], all_members[i]['gender'], all_members[i]['m_status'],
                                 all_members[i]['hobbies'], all_members[i]['p_state']])
        if main_app.file_update():
            return False
        else:
            return True

    @classmethod
    def file_update(cls):
        os.remove('.\\accounts.csv')
        os.rename('.\\accounts_temp.csv', '.\\accounts.csv')
        return False

    def main_interface(self):
        Admin_Interface.all_members = Admin_Interface.Load_data()
        if Admin_Interface.all_members:
            while True:
                main_option = input('[1]-Admin\n[2]-To Register\n[#]-Exit\nEnter Option: ')

                if main_option == '1':
                    Admin_Interface().admin_view()
                elif main_option == '2':
                    reg_window.mainloop()
                elif main_option == '#':
                    print('Exiting...')
                    break
                else:
                    print('Invalid option')
        else:
            print('Seems there is a problem\nRestart application')


class Admin_Interface:
    all_members = None

    @classmethod
    def Load_data(cls):
        members = {}
        if os.path.isfile('.\\accounts.csv'):
            # read data from text file
            with open('.\\accounts.csv') as records:
                reader = csv.reader(records)
                for record in reader:
                    lname, fname, uname, pword, gen, m_status, hobby, p_state = record
                    members[uname] = {'lastname': lname, 'firstname': fname,
                                      'password': pword, 'gender': gen, 'm_status': m_status,
                                      'hobbies': hobby, 'p_state': p_state}
            return members
        else:
            with open('.\\accounts.csv', 'w'):
                pass

    def access(self):
        while True:
            admin_user = input('Enter Username: ')
            if admin_user == '0':
                admin_pass = input('Enter password: ')
                if admin_pass == '0':
                    return True
                else:
                    print('Access denied!')
                    return False
            else:
                print('Invalid Username')
                break

    def view_all(self):
        for i in Admin_Interface.all_members:
            print(f"Username: {i}\nLast Name: {Admin_Interface.all_members[i]['lastname']}" +
                  f"\nFirst Name: {Admin_Interface.all_members[i]['firstname']}" +
                  f"\nGender: {Admin_Interface.all_members[i]['gender']}" +
                  f"\nMarital Status: {Admin_Interface.all_members[i]['m_status']}" +
                  f"\nHobbies: {Admin_Interface.all_members[i]['hobbies']}" +
                  f"\nPersonal Statement: {Admin_Interface.all_members[i]['p_state']}\n")

    def delete_member(self, username):
        if username in Admin_Interface.all_members:
            del Admin_Interface.all_members[username]
            return 'User deleted successfully'
        else:
            return f'{username} not found!'

    def view_member(self, username):
        if username in Admin_Interface.all_members:
            return f"Username: {username}\nLast Name: {Admin_Interface.all_members[username]['lastname']}\nFirst Name: {Admin_Interface.all_members[username]['firstname']}\nGender: {Admin_Interface.all_members[username]['gender']}\nMarital Status: {Admin_Interface.all_members[username]['m_status']}\nHobbies: {Admin_Interface.all_members[username]['hobbies']}\nPersonal Statement: {Admin_Interface.all_members[username]['p_state']}"
        else:
            return f'{username} not found!'

    def admin_view(self):
        if self.access():
            while True:
                main_option = input('[1]-View all members\n[2]-Delete a member\n' +
                                    '[3]-Search for a member\n[#]-Log Out\nEnter option: ')
                if main_option == '1':
                    self.view_all()
                elif main_option == '2':
                    uname = input('Enter Username: ')
                    print(self.delete_member(uname))
                    main_app.update_record(Admin_Interface.all_members)
                elif main_option == '3':
                    uname = input('Enter Username: ')
                    print(self.view_member(uname))
                elif main_option == '#':
                    print('\n\nLogging off Admin...')
                    break
                else:
                    print('Invalid Option')
        else:
            print('Error...')


class Reg_Interface(Frame):

    def __init__(self, master):
        super(Reg_Interface, self).__init__(master)
        self.chk1 = StringVar()
        self.chk2 = StringVar()
        self.chk3 = StringVar()
        self.chk4 = StringVar()
        self.lname_var = StringVar()
        self.fname_var = StringVar()
        self.uname_var = StringVar()
        self.pass_var = StringVar()
        self.gend_var = StringVar()
        self.status_var = StringVar()
        self.ps_var = StringVar()
        self.grid()
        self.create_widget()

    def get_hobby(self):
        mylist = [self.chk1.get(), self.chk2.get(), self.chk3.get(), self.chk4.get()]
        alist = []
        for i in mylist:
            if i != "0":
                alist.append(i)
        hb = ", ".join(alist)
        return hb

    def get_ps(self):
        ps = self.ps_txt.get("1.0", "end-1c")
        return ps

    def submit(self):
        self.get_ps()
        self.new_entry()
        self.lname.delete(0, END)
        self.fname.delete(0, END)
        self.uname.delete(0, END)
        self.pword.delete(0, END)
        self.female.select()
        self.status.set("")
        self.hobby1.deselect()
        self.hobby2.deselect()
        self.hobby3.deselect()
        self.hobby4.deselect()
        self.ps_txt.delete("1.0", "end")

    def new_entry(self):
        if self.uname_var.get() in Admin_Interface.all_members:
            messagebox.showerror(title='Message', message='User already exists!\nTry another username')
        else:
            Admin_Interface.all_members[self.uname_var.get()] = {'lastname': self.lname_var.get(),
                                                                 'firstname': self.fname_var.get(),
                                                                 'password': self.pass_var.get(),
                                                                 'gender': self.gend_var.get(),
                                                                 'm_status': self.status_var.get(),
                                                                 'hobbies': self.get_hobby(),
                                                                 'p_state': self.get_ps()}
            main_app.update_record(Admin_Interface.all_members)
            messagebox.showinfo(title='Message', message='Registration Successful!')

    def reset(self):
        self.lname.delete(0, END)
        self.fname.delete(0, END)
        self.uname.delete(0, END)
        self.pword.delete(0, END)
        self.female.select()
        self.status.set("")
        self.hobby1.deselect()
        self.hobby2.deselect()
        self.hobby3.deselect()
        self.hobby4.deselect()
        self.ps_txt.delete("1.0", "end")

    def close(self):
        reg_window.destroy()

    def create_widget(self):
        self.empty_lbl = Label(self, text="", font='Arial 11 normal')
        self.empty_lbl.grid(row=0, column=1, sticky=W)

        self.lname_lbl = Label(self, text="Last Name: ", font='Arial 11 normal')
        self.lname_lbl.grid(row=1, column=0, sticky=W)
        self.lname = Entry(self, textvariable=self.lname_var, font='Arial 11 normal')
        self.lname.grid(row=1, column=1, columnspan=2, sticky=W)

        self.fname_lbl = Label(self, text="First Name: ", font='Arial 11 normal')
        self.fname_lbl.grid(row=2, column=0, sticky=W)
        self.fname = Entry(self, textvariable=self.fname_var, font='Arial 11 normal')
        self.fname.grid(row=2, column=1, columnspan=2, sticky=W)

        self.uname_lbl = Label(self, text="Username: ", font='Arial 11 normal')
        self.uname_lbl.grid(row=3, column=0, sticky=W)
        self.uname = Entry(self, textvariable=self.uname_var, font='Arial 11 normal')
        self.uname.grid(row=3, column=1, columnspan=2, sticky=W)

        self.pword_lbl = Label(self, text="Password: ", font='Arial 11 normal')
        self.pword_lbl.grid(row=4, column=0, sticky=W)
        self.pword = Entry(self, textvariable=self.pass_var, font='Arial 11 normal', show='*')
        self.pword.grid(row=4, column=1, columnspan=2, sticky=W)

        self.gen_lbl = Label(self, text="Gender: ", font='Arial 11 normal')
        self.gen_lbl.grid(row=5, column=0, sticky=W)

        self.female = Radiobutton(self, text="Female", font='Arial 11 normal',
                                  variable=self.gend_var, value='Female')
        self.female.select()
        self.female.grid(row=5, column=1, sticky=W)

        self.male = Radiobutton(self, text="Male", font='Arial 11 normal',
                                variable=self.gend_var, value='Male')
        self.male.grid(row=5, column=2, sticky=W)


        self.status_lbl = Label(self, text="Marital Status: ", font='Arial 11 normal')
        self.status_lbl.grid(row=6, column=0, sticky=W)

        self.status = ttk.Combobox(self, width=30, textvariable=self.status_var)
        self.status.grid(row=6, column=1, sticky=W, columnspan=2)

        self.status['values'] = ('Single', 'Married')
        self.status['state'] = 'readonly'
        # 'normal' to make the entry editable

        self.hobby_lbl = Label(self, text="Hobbies", font='Arial 11 normal')
        self.hobby_lbl.grid(row=7, column=0, sticky=W)

        self.hobby1 = Checkbutton(self, text="Singing", variable=self.chk1, onvalue="Singing", offvalue="0",
                                  font='Arial 11 normal')
        self.hobby1.deselect()
        self.hobby2 = Checkbutton(self, text="Movie", variable=self.chk2, onvalue="Movie", offvalue="0",
                                  font='Arial 11 normal')
        self.hobby2.deselect()
        self.hobby3 = Checkbutton(self, text="Dancing", variable=self.chk3, onvalue="Dancing", offvalue="0",
                                  font='Arial 11 normal')
        self.hobby3.deselect()
        self.hobby4 = Checkbutton(self, text="Flexing", variable=self.chk4, onvalue="Flexing", offvalue="0",
                                  font='Arial 11 normal')
        self.hobby4.deselect()
        self.hobby1.grid(row=7, column=1, sticky=W)
        self.hobby2.grid(row=8, column=1, sticky=W)
        self.hobby3.grid(row=9, column=1, sticky=W)
        self.hobby4.grid(row=10, column=1, sticky=W)

        self.ps_lbl = Label(self, text="Personal Statement: ", font='Arial 11 normal')
        self.ps_lbl.grid(row=11, column=0, sticky=W)
        self.ps_txt = Text(self, height=5, width=10, wrap='word')
        self.ps_txt.grid(row=11, column=1, columnspan=3, sticky=W)


        self.empty_lbl = Label(self, text="", font='Arial 11 normal')
        self.empty_lbl.grid(row=12, column=1, sticky=W)

        self.submit = Button(self, text='Submit', padx=20, pady=6, command=self.submit)
        self.submit.grid(row=13, column=0, sticky=E)

        self.reset = Button(self, text='Reset', padx=20, pady=6, command=self.reset)
        self.reset.grid(row=13, column=1, sticky=W)

        self.empty_lbl = Label(self, text="", font='Arial 11 normal')
        self.empty_lbl.grid(row=14, column=1, sticky=W)

        self.empty_lbl = Label(self, text="", font='Arial 11 normal')
        self.empty_lbl.grid(row=15, column=1, sticky=W)

        self.button_quit = Button(self, text="Exit", padx=20, pady=6, command=self.close)
        self.button_quit.grid(row=16, column=1, sticky=W)



window = Tk()
window.title('Registration Form')
window.geometry('500x500')
reg_window = Reg_Interface(window)

if __name__ == "__main__":
    Golf_club = main_app()
    Golf_club.main_interface()
