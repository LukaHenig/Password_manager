#--------------------------------------------------------#
#File: password_generator                                #
#Programmed by: Luka Henig (luka.henig@gmail.com)        #
#Curse: 100 Days of Code / udemy                         #
#Date: 26/02/2022                                        #
#Description: Working with Tkinter, password-manager to  #
#create and store diffrent passwords as well as learn    #
#how to catch exceptions                                 #
#--------------------------------------------------------#

#imports
import json
from tkinter import*
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """generate new password"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    #to be able to redo the password per click
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    #for instand copy of password
    pyperclip.copy(password)

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search():
    """search for data, for a particular website"""
    website = website_entry.get()
    try:
        with open("src/data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website in data:
            password = data[website]["password"]
            email = data[website]["email"]
            messagebox.showinfo(title=website, message=f"The password is: {password} \nThe Email is: {email} \nPress Ok")
        else:
            messagebox.showinfo(title="Error", message=f"There was no entry for {website}, pleas try again!")
    finally:
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """check and save input data"""
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) > 0 and len(password) > 0:
        is_oke = messagebox.askokcancel(title=website, message=f"These are the details you entered: \nEmail: {email} \nPassword: {password} \nPress Ok to save!")
        if is_oke:
            try:
                with open("src/data.json", "r") as data_file:
                    # reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                    with open("src/data.json", "w") as data_file:
                        # saving new data
                        json.dump(new_data, data_file, indent=4)
            else:
                #updating old data
                data.update(new_data)

                with open("src/data.json", "w") as data_file:
                    #saving new data
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
#window setting
window = Tk()
window.title("Password manager")
window.config(pady=50, padx=50)

#logo setting
canvas = Canvas(width=200, height=200, )
logo_img = PhotoImage(file="src/logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

#label settings
website_lbl = Label(text="Website:")
website_lbl.grid(row=1, column=0)

email_username_lbl = Label(text="Email/Username:")
email_username_lbl.grid(row=2, column=0)

password_lbl = Label(text="Password:")
password_lbl.grid(row=3, column=0)

#entry settings
password_entry = Entry(width=27)
password_entry.grid(row=3, column=1)

website_entry = Entry(width=27)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_username_entry = Entry(width=45)
email_username_entry.grid(row=2, column=1, columnspan=2)
email_username_entry.insert(0, "luka.henig@test.de")

#button settings
generate_password_btn = Button(text="Generate Password", command=generate_password)
generate_password_btn.grid(row=3, column=2)

search_btn = Button(text="Search",width=15, command=search)
search_btn.grid(row=1, column=2)

add_btn = Button(text="Add", width=39, command=save)
add_btn.grid(row=4, column=1, columnspan=2)

#keep screen alive
window.mainloop()