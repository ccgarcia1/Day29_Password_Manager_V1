from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # using list comprehension to get the random letters
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    # using list comprehension to get the random symbols
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    # using list comprehension to get the random numbers
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {
                    "email": email,
                    "password": password,
                          }
                }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Ooops", message="The Website field or Password field cannot be blank")

    else:
        try:
            with open("data.json", mode="r") as data_file:
                # try reading the actual data present in the JSON file
                data = json.load(data_file)
                # updating the JSON with new data
                data.update(new_data)
        except:
            # creating the file case it not exists
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", mode="w") as data_file:
                # Saving updated data into the JSON file
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

def find_password():
    website = website_entry.get().lower()
    try:
        with open("data.json", mode="r") as data_file:
            # try reading the actual data present in the JSON file
            data = json.load(data_file)
            data_lower = {key.lower(): value for key, value in data.items()}
            print(data_lower)
    except FileNotFoundError:
        messagebox.showinfo(title="Info", message="There are no records to find!")
    else:
        if website in data_lower:
            email = data_lower[website]["email"]
            password = data_lower[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
            print(f"email: {email} - password: {password}")
        else:
            messagebox.showinfo(title="Info", message=f"No details for {website}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# entries
website_entry = Entry(width=33)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "cleitoncristianogarcia@gmail.com")
password_entry = Entry(width=33)
password_entry.grid(row=3, column=1)

# buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2, columnspan=1)
search_password_button = Button(text="Search", width=15, command=find_password)
search_password_button.grid(row=1, column=2, columnspan=1)
add_button = Button(text="Add", width=44, command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
