import webbrowser
import subprocess
import pymysql as m
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkinter import PhotoImage
from tkinter import Label

browser_executable = 'C:\Program Files\Google\Chrome\Application\chrome.exe.'


def fetch_data_from_merged_table():
    try:
        db = m.connect(host="localhost", user="root", password="", db="taxxx")
        cur = db.cursor()

        # Fetch data from the merged_data table
        cur.execute("SELECT * FROM merged_data")

        # Fetch all rows
        rows = cur.fetchall()

        for row in rows:
            # Process the data as needed
            print(row)

        db.close()
    except m.Error as e:
        print(f"Database Error: {e}")
        messagebox.showerror("Error", "Database error occurred. Check your database configuration.")

# Function to submit location input in Tab 1
def submit_location():
    try:
        # Check if the locations are the same
        if from_location.get() == to_location.get():
            messagebox.showerror("Error", "From and To locations cannot be the same.")
        else:
            # Switch to Tab 2
            tab_control.select(1)
            
            # Print the selected locations to the console
            global selected_from_location
            selected_from_location = from_location.get()
            selected_to_location = to_location.get()
            print(f"Selected From Location: {selected_from_location}")
            print(f"Selected To Location: {selected_to_location}")
            
            # Display the selected locations as a headline in Tab 3
            display_locations_in_tab3(selected_from_location, selected_to_location)
            
            A = from_combobox.get()
            B = to_combobox.get()
            
            # Establish a database connection
            db_tab1 = m.connect(host="localhost", user="root", password="", db="taxxx")
            cur_tab1 = db_tab1.cursor()
            
            # Insert data into the table
            cur_tab1.execute("INSERT INTO pyy (from_location, to_location) VALUES (%s, %s)", (A, B))
            db_tab1.commit()
            
            print("Successfully inserted into Tab 1's database.")
    except m.Error as e:
        print(f"Database Error: {e}")
        messagebox.showerror("Error", "Database error occurred. Check your database configuration.")

def display_locations_in_tab3(from_location, to_location):
    # Create a Label to display the selected locations in Tab 3
    locations_label_tab3 = ttk.Label(tab3, text=f"From: {from_location} - To: {to_location}", font=("Helvetica", 14), foreground="blue")
    locations_label_tab3.place(x=500, y=100)  # Adjust x and y coordinates as needed
    #["SALEM", "ATTUR", "EDAPPADI", "OMALUR", "SANKAGIRI", "YERCAUD", "VEERAPANDI", "METTUR"]



def submit_datetime():
    try:
        # Check if the booking date and time are in the future
        booking_datetime = datetime.strptime(booking_date.get() + " " + booking_time.get(), "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()

        if booking_datetime <= current_datetime:
            messagebox.showerror("Error", "Booking date and time must be in the future.")
        else:
            # Switch to Tab 3
            tab_control.select(2)

            A = booking_date.get()
            B = booking_time.get()

            # Establish a database connection
            db_tab2 = m.connect(host="localhost", user="root", password="", db="taxxx")
            cur_tab2 = db_tab2.cursor()

            # Insert data into the booking table
            cur_tab2.execute("INSERT INTO booking (booking_date, booking_time) VALUES (%s, %s)", (A, B))
            db_tab2.commit()

            print("Successfully inserted into Tab 2's database.")
    except m.Error as e:
        print(f"Database Error: {e}")
        messagebox.showerror("Error", "Database error occurred. Check your database configuration.")

#def submit_distance():
    



# Function to submit payment options in Tab 4
def submit_payment():
    selected_option = payment_var.get()

    if selected_option == "QR OR UPI":
        # Create a new window for displaying the image
        tab = tk.Toplevel()
        tab.title("Option 1 Image")
        tab.geometry("500x500")

        # Load the image
        img = PhotoImage(file="C:\\111python\\GooglePay_QR.png")

        # Scale down the image (adjust the values as needed)
        img = img.subsample(5, 5)  # Halve the image size

        # Create a Label to display the scaled image
        label = Label(tab, image=img)
        label.image = img  # Keep a reference to the image to prevent it from being garbage collected
        label.place(x=0, y=0)

        # Function to close the Toplevel window
        def close_window():
            tab.destroy()
            # After the window is closed, show the success messagebox
            messagebox.showinfo("Success", "Booking submitted with Option 1.")

        # Create a button to allow the user to close the window
        close_button = ttk.Button(tab, text="Close Window", command=close_window)
        close_button.place(x=200, y=450)  # Adjust x and y coordinates as needed

    elif selected_option == "Option 2":
        messagebox.showinfo("Success", "Booking submitted with Option 2.")
    elif selected_option == "Option 3":
        # Validate ATM card details
        atm_card_number = atm_card_entry.get()

        if not atm_card_number.isdigit() or len(atm_card_number) != 16:
            messagebox.showerror("Error", "ATM card number must be 16 digits.")
            return

        messagebox.showinfo("Success", "Booking submitted with Option 3 (ATM card).")


# Create the main window
root = tk.Tk()
root.title("Taxi Booking App")
root.geometry("1000x700")

# Load the taxi icon
taxi_icon = PhotoImage(file="C:\\111python\\GooglePay_QR.png")
root.iconphoto(False, taxi_icon)

# Create tab control
tab_control = ttk.Notebook(root)
tab_control.pack(fill="both", expand=True)

# Tab 1 - Location Entry
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Location")

# Load the image
background_image = PhotoImage(file="C:\\111python\\5j.png")

# Create a Label widget to display the background image
image_label = Label(tab1, image=background_image)
image_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load the logo image C:\\111python\\GooglePay_QR.png

logo_image = PhotoImage(file="C:\\111python\\10K.png")

# Scale down the logo image (adjust the values as needed)
scaled_logo_image = logo_image.subsample(3, 3)  # Adjust the subsample factor as per your desired size

# Create a Label widget to display the scaled logo
logo_label = Label(tab1, image=scaled_logo_image)
logo_label.place(x=500, y=50)  # Adjust the x and y coordinates to position the logo

# Create default location options
default = ["SALEM", "ATTUR", "EDAPPADI", "OMALUR", "SANKAGIRI", "YERCAUD", "VEERAPANDI", "METTUR"]

from_location = tk.StringVar()
to_location = tk.StringVar()

from_label = ttk.Label(tab1, text="From Location:", font=("Arial", 14))
to_label = ttk.Label(tab1, text="To Location:", font=("Arial", 14))

# Create ComboBox widgets with default values
from_combobox = ttk.Combobox(tab1, values=default, textvariable=from_location, font=("Arial", 12))
from_combobox.set(default[0])
to_combobox = ttk.Combobox(tab1, values=default, textvariable=to_location, font=("Arial", 12))
to_combobox.set(default[1])

submit1_button = ttk.Button(tab1, text="Submit", command=submit_location, style="TButton")

from_label.place(x=100, y=300)
from_combobox.place(x=250, y=300)
to_label.place(x=100, y=350)
to_combobox.place(x=250, y=350)
submit1_button.place(x=200, y=400)

# Tab 2 - Date and Time Entry
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text="Date & Time")

# Load the image for Tab 2
background_image_tab2 = PhotoImage(file="C:\\111python\\6k.png")

# Create a Label widget to display the background image in Tab 2
image_label_tab2 = Label(tab2, image=background_image_tab2)
image_label_tab2.place(x=0, y=0, relwidth=1, relheight=1)

# Create Date and Time Entry widgets in Tab 2
booking_date = tk.StringVar()
booking_time = tk.StringVar()
date_label = ttk.Label(tab2, text="Booking Date (YYYY-MM-DD):", font=("Arial", 14))
time_label = ttk.Label(tab2, text="Booking Time (HH:MM):", font=("Arial", 14))
date_entry = ttk.Entry(tab2, textvariable=booking_date, font=("Arial", 12))
time_entry = ttk.Entry(tab2, textvariable=booking_time, font=("Arial", 12))
submit2_button = ttk.Button(tab2, text="Submit", command=submit_datetime, style="TButton")

date_label.place(x=100, y=100)
date_entry.place(x=400, y=100)
time_label.place(x=100, y=150)
time_entry.place(x=400, y=150)
submit2_button.place(x=200, y=200)




# Tab 3 - Distance
tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text="Distance")

# Load the image for Tab 3
background_image_tab3 = PhotoImage(file="C:\\111python\\7k.png")

# Create a Label widget to display the background image in Tab 3
image_label_tab3 = Label(tab3, image=background_image_tab3)
image_label_tab3.place(x=0, y=0, relwidth=1, relheight=1)

# Create Entry widgets for user input in Tab 3
name_label = ttk.Label(tab3, text="Name:", font=("Arial", 14))
address_label = ttk.Label(tab3, text="Address:", font=("Arial", 14))
phone_label = ttk.Label(tab3, text="Phone Number:", font=("Arial", 14))
age_label = ttk.Label(tab3, text="Age:", font=("Arial", 14))

name_entry = ttk.Entry(tab3, font=("Arial", 12))
address_entry = ttk.Entry(tab3, font=("Arial", 12))
phone_entry = ttk.Entry(tab3, font=("Arial", 12))
age_entry = ttk.Entry(tab3, font=("Arial", 12))

name_label.place(x=100, y=100)
name_entry.place(x=300, y=100)
address_label.place(x=100, y=150)
address_entry.place(x=300, y=150)
phone_label.place(x=100, y=200)
phone_entry.place(x=300, y=200)
age_label.place(x=100, y=250)
age_entry.place(x=300, y=250)

# Create a label to display the default distance message
distance_label = ttk.Label(tab3, text=" PER KM 20:ONLY ", font=("Arial", 14, "bold"), foreground="red")
distance_label.place(x=400, y=50)
def db():
    A=name_entry.get()
    B=age_entry.get()
    C=address_entry.get()
    D=phone_entry.get()
    if A=="" or B=="" or C=="" or D=="":
        messagebox.showerror("error","fill the details")

    
    else:
        tab_control.select(3)  # Switch to Tab 4
        db=m.connect(host="localhost",user="root",password="",db="taxxx")
        cur=db.cursor()
        cur.execute("insert into pyt values('"+A+"','"+B+"','"+C+"','"+D+"')")
        db.commit()
        messagebox.showinfo("submit","suuccessfully submitted")
        
submit3_button = ttk.Button(tab3, text="Submit", command=db, style="TButton")
submit3_button.place(x=200, y=350)



# Tab 4 - Payment Options
tab4 = ttk.Frame(tab_control)
tab_control.add(tab4, text="Payment")

# Load the image for Tab 4
background_image_tab4 = PhotoImage(file="C:\\111python\\8k.png")

# Create a Label widget to display the background image in Tab 4
image_label_tab4 = Label(tab4, image=background_image_tab4)
image_label_tab4.place(x=0, y=0, relwidth=1, relheight=1)

# Create Payment Entry widgets in Tab 4
payment_options = ["QR OR UPI", "OFFLINE PAY", "ATM CARD"]
payment_var = tk.StringVar(tab4)
payment_var.set(payment_options[0])
payment_label = ttk.Label(tab4, text="Select Payment Option:", font=("Arial", 14))
payment_combobox = ttk.Combobox(tab4, values=payment_options, textvariable=payment_var, font=("Arial", 12))
payment_label.place(x=100, y=100)
payment_combobox.place(x=100, y=200)

# Create two frames for payment options and ATM card details
payment_frame = ttk.Frame(tab4)
atm_frame = ttk.Frame(tab4)

# Payment Options Frame
payment_option_label = ttk.Label(payment_frame, text="Payment Option Selected: ", font=("Arial", 14))
payment_option_selected_label = ttk.Label(payment_frame, textvariable=payment_var, font=("Arial", 12))
payment_option_label.pack()
payment_option_selected_label.pack()

# ATM Card Details Frame
atm_card_label = ttk.Label(atm_frame, text="ATM Card Number:", font=("Arial", 14))
atm_card_entry = ttk.Entry(atm_frame, font=("Arial", 12))
atm_cvv_label = ttk.Label(atm_frame, text="CVV:", font=("Arial", 14))
atm_cvv_entry = ttk.Entry(atm_frame, show="*", font=("Arial", 12))
atm_expiry_label = ttk.Label(atm_frame, text="Expiry Date (MM/YY):", font=("Arial", 14))
atm_expiry_entry = ttk.Entry(atm_frame, font=("Arial", 12))

atm_card_label.pack()
atm_card_entry.pack()
atm_cvv_label.pack()
atm_cvv_entry.pack()
atm_expiry_label.pack()
atm_expiry_entry.pack()

# Submit Button
submit4_button = ttk.Button(tab4, text="Submit", command=submit_payment, style="TButton")
submit4_button.place(x=400, y=300)



# Function to switch between frames based on the selected payment option
def switch_payment_frame(event):
    selected_option = payment_var.get()
    
    if selected_option == "ATM CARD":
        payment_frame.pack_forget()
        atm_frame.pack()
    else:
        atm_frame.pack_forget()
        payment_frame.pack()

payment_combobox.bind("<<ComboboxSelected>>", switch_payment_frame)

# Initially show the payment options frame
payment_frame.pack()

tab_control.pack(expand=1, fill="both")

root.mainloop()
