from tkinter import *
import mysql.connector
from tkinter import messagebox

connection = None

def connect_to_database():
    global connection
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root*#",
            database="company1"
        )
        print(connection)
    except mysql.connector.Error as err:
        print("Error connecting to MySQL:", err)

def create_table():
  
    try:
        mycursor = connection.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS passenger (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(60), DOB VARCHAR(60), Address VARCHAR(100), email VARCHAR(80), phone_number VARCHAR(15), user_password VARCHAR(20), confirm_password VARCHAR(20))")
        print("Table created successfully!")
    except mysql.connector.Error as err:
        print("Error creating table:", err)


def create_booking_table():
    try:
        mycursor = connection.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS bookings (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(20),Age int,passenger_id INT, seat_number VARCHAR(10), pickup_location VARCHAR(100), drop_location VARCHAR(100))")
        print("Bookings table created successfully!")
    except mysql.connector.Error as err:
        print("Error creating bookings table:", err)

def register_user():
    name = name_entry.get()
    dob = DOB_entry.get()
    address = address_entry.get()
    email = email_entry.get()
    phone_number = phonenumber_entry.get()
    password = password_entry.get()
    confirm_password = confirmpassword_entry.get()

     # Check if phone_number has exactly 10 digits
    if len(phone_number) != 10 or not phone_number.isdigit():
        messagebox.showerror("Error", "Phone number should be 10 digits long and contain only numbers")
        return
    # Validate password format
    if not validate_password(password):
        messagebox.showerror("Error", "Password must contain at least one uppercase letter, one lowercase letter, one numeric value, one symbol, and be at least 8 characters long")
        return
        pass 

# Define the validate_password function
def validate_password(password):
    # Check if password meets criteria (e.g., at least 8 characters, contains uppercase, lowercase, digit, and special character)
    if len(password) < 8:
        return False
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(not char.isalnum() for char in password)
    return has_uppercase and has_lowercase and has_digit and has_special
        

    # Check if password and confirm_password match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return    
    

    query = "INSERT INTO passanger (Name, DOB, Address, email, phone_number, password,confirm_password) VALUES (%s, %s, %s, %s, %s, %s,%s)"
    values = (name, dob, address, email, phone_number, password,confirm_password)

    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error registering user: {err}")


def show_seat_selection():
    global pickup_var, drop_var, selected_seat_number
    
    seat_window = Tk()
    seat_window.title("Seat Selection")

    pickup_label = Label(seat_window, text="Pickup Location:", font=("jester", 12))
    pickup_label.grid(row=0, column=0, padx=10, pady=10)
    pickup_var = StringVar()
    pickup_options = ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Erode",
     "Vellore", "Thoothukudi", "Thanjavur", "Dindigul", "Cuddalore", "Tiruppur", "Kanyakumari", "Karur", "Namakkal",
      "Perambalur", "Sivaganga", "Ramanathapuram", "Pudukkottai", "Nagapattinam", "Virudhunagar", "Krishnagiri", "Ariyalur", "The Nilgiris"]
    pickup_var.set(pickup_options[0])  
    pickup_dropdown = OptionMenu(seat_window, pickup_var, *pickup_options)
    pickup_dropdown.grid(row=0, column=1, padx=10, pady=10)

    drop_label = Label(seat_window, text="Drop Location:", font=("jester", 12))
    drop_label.grid(row=1, column=0, padx=10, pady=10)
    drop_var = StringVar()
    drop_options = ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Erode",
     "Vellore", "Thoothukudi", "Thanjavur", "Dindigul", "Cuddalore", "Tiruppur", "Kanyakumari", "Karur", "Namakkal", 
     "Perambalur", "Sivaganga", "Ramanathapuram", "Pudukkottai", "Nagapattinam", "Virudhunagar", "Krishnagiri", "Ariyalur", "The Nilgiris"]
    drop_var.set(drop_options[0])  
    drop_dropdown = OptionMenu(seat_window, drop_var, *drop_options)
    drop_dropdown.grid(row=1, column=1, padx=10, pady=10)

    seats_label = Label(seat_window, text="Seating Arrangement:", font=("jester", 12))
    seats_label.grid(row=2, column=0, columnspan=5, pady=10)
    selected_seat_number = None

    def seat_selected(seat_number):
        global selected_seat_number  # Use global keyword to modify the global variable
        selected_seat_number = seat_number

    for i in range(2):
        for j in range(5):
            seat_button_text = f"A{i*5 + j + 1}"
            Button(seat_window, text=seat_button_text, width=5, height=2, command=lambda text=seat_button_text: seat_selected(text)).grid(row=i + 3, 
            column=j, padx=5, pady=5)

    amount_label = Label(seat_window, text="Amount: ₹1500", font=("jester", 12))
    amount_label.grid(row=5, column=0, columnspan=5, pady=10)

    def confirm_booking():
        pickup_location = pickup_var.get()
        drop_location = drop_var.get()
        seat_number = selected_seat_number  
        name=name_entry.get()
        age=age_entry.get()

        query = "INSERT INTO bookings (passenger_id, seat_number,name ,age int, pickup_location, drop_location) VALUES (%s, %s, %s, %s)"
        values = (passenger_id,Name, seat_number,name,age, pickup_location, drop_location,phone_number)  
        try:
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()
            messagebox.showinfo("Success", "Booking confirmed successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error confirming booking: {err}")

 # Get the selected gender from the OptionMenu
    gender = gender_var.get() 
    
# Create a StringVar to store the selected gender
    gender_var = StringVar()
    gender_var.set("Male")  # Set a default value

# Gender options
    gender_options = ["Male", "Female", "Other"]

# Gender label and OptionMenu
    gender_label = Label(root, text="Gender:")
    gender_label.grid(row=6, column=0, padx=10, pady=5)
    gender_dropdown = OptionMenu(root, gender_var, *gender_options)
    gender_dropdown.grid(row=6, column=1, padx=10, pady=5)              

    confirm_button = Button(seat_window, text="Confirm", command=confirm_booking)
    confirm_button.grid(row=6, column=0, columnspan=5, pady=10)

    def cancel_booking():
        query = "DELETE FROM bookings WHERE passenger_id = %s"
        values = (passenger_id,)  
        try:
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()
            messagebox.showinfo("Success", "Booking canceled successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error canceling booking: {err}")

    cancel_button = Button(seat_window, text="Cancel Booking", command=cancel_booking)
    cancel_button.grid(row=7, column=0, columnspan=5, pady=10)

    seat_window.mainloop()

def login():
    login_window = Tk()
    login_window.title("Login")
    
    Label(login_window, text="Email or Phone:").grid(row=0, column=0, padx=10, pady=5)
    email_phone_entry = Entry(login_window)
    email_phone_entry.grid(row=0, column=1, padx=10, pady=5)
    
    Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    password_entry = Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)
    
    def validate_login():
        email_phone = email_phone_entry.get()
        password = password_entry.get()
        
        query = "SELECT * FROM passanger WHERE (email = %s OR phone_number = %s) AND password = %s"
        values = (email_phone, email_phone, password)
        
        try:
            cursor = connection.cursor()
            cursor.execute(query, values)
            user = cursor.fetchone()
            
            if user:
                global passenger_id
                passenger_id = user[0]  # Assuming the first column is the passenger_id
                login_window.destroy()
                show_seat_selection()
            else:
                messagebox.showerror("Login Failed", "Invalid email/phone or password")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error during login: {err}")
    
    login_button = Button(login_window, text="Login", command=validate_login)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    login_window.mainloop()

root = Tk()
root.title("User Registration")

Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=5)
name_entry = Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="DOB:").grid(row=1, column=0, padx=10, pady=5)
DOB_entry = Entry(root)
DOB_entry.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Address:").grid(row=2, column=0, padx=10, pady=5)
address_entry = Entry(root)
address_entry.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Email:").grid(row=3, column=0, padx=10, pady=5)
email_entry = Entry(root)
email_entry.grid(row=3, column=1, padx=10, pady=5)

Label(root, text="Phone Number:").grid(row=4, column=0, padx=10, pady=5)
phonenumber_entry = Entry(root)
phonenumber_entry.grid(row=4, column=1, padx=10, pady=5)

Label(root, text="Password:").grid(row=5, column=0, padx=10, pady=5)
password_entry = Entry(root, show="*")
password_entry.grid(row=5, column=1, padx=10, pady=5)

Label(root, text="confirm Password:").grid(row=6, column=0, padx=10, pady=5)
confirmpassword_entry = Entry(root, show="*")
confirmpassword_entry.grid(row=6, column=1, padx=10, pady=5)

register_button = Button(root, text="Register", command=register_user)
register_button.grid(row=7, column=0, columnspan=2, pady=10)

login_button = Button(root, text="Login", command=login)
login_button.grid(row=8, column=0, columnspan=2, pady=10)

connect_to_database()
create_table()
create_booking_table()

root.mainloop()