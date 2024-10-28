import tkinter as tk
from tkinter import messagebox, filedialog
import pywhatkit
import random


# funkcija za slanje poruka
def send_messages():
    try:
        br_sudionika = int(num_participants_entry.get())
        sat = int(hour_entry.get())
        minuta = int(minute_entry.get())

        # stvaranje imenika pastira i ovcica
        imenik = []
        for i in range(br_sudionika):
            name = entries[i][0].get()
            phone = entries[i][1].get()
            if not name or not phone:
                messagebox.showerror("Input Error", "All names and numbers must be filled.")
                return
            imenik.append([name, phone])

        # izmjesamo imenik kako bi nasumicno spojili ovcice i pastire
        random.shuffle(imenik)
        for i in range(br_sudionika - 1):
            pywhatkit.sendwhatmsg("+" + imenik[i][1],
                                  "Bok " + imenik[i][0] + ", tvoja ovcica je: " + imenik[i + 1][0],
                                  sat, minuta)
            minuta += 1  # kako bi funkcionirao kod poruke moraju biti minutu u razmaku

        # zadnja poruka koja spaja zadnju ovcicu s prvim pastirem
        pywhatkit.sendwhatmsg("+" + imenik[-1][1],
                              "Bok " + imenik[-1][0] + ", tvoja ovcica je " + imenik[0][0],
                              sat, minuta)

        messagebox.showinfo("Success", "Messages have been scheduled successfully!")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for participants, time, and phone numbers.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# funkcija za stvaranje polja za unos sudionika
def create_participant_fields():
    try:
        br_sudionika = int(num_participants_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of participants.")
        return

    for widgets in participants_frame.winfo_children():
        widgets.destroy()

    global entries
    entries = []

    participants_frame.configure(background='lightpink')

    # Header
    tk.Label(participants_frame, text="No.", width=5, background="lightblue1").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(participants_frame, text="Ime:", width=20, background="lightblue1").grid(row=0, column=1, padx=5, pady=5)
    tk.Label(participants_frame, text="Broj:", width=20, background="lightblue1").grid(row=0, column=2, padx=5, pady=5)

    for i in range(br_sudionika):
        number_label = tk.Label(participants_frame, text=f"{i + 1}.", width=5, background="lightblue1")
        name_entry = tk.Entry(participants_frame, width=20)
        phone_entry = tk.Entry(participants_frame, width=20)

        # Grid placement for each row
        number_label.grid(row=i + 1, column=0, padx=5, pady=5)
        name_entry.grid(row=i + 1, column=1, padx=5, pady=5)
        phone_entry.grid(row=i + 1, column=2, padx=5, pady=5)

        # Store entries for later access
        entries.append((name_entry, phone_entry))


# funkcija za učitavanje imenika iz txt datoteke
def load_from_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not filepath:
        return

    with open(filepath, 'r') as file:
        lines = file.readlines()

    num_participants_entry.delete(0, tk.END)
    num_participants_entry.insert(0, str(len(lines)))

    create_participant_fields()  # Create fields based on the number of lines in the file

    for i, line in enumerate(lines):
        name, phone = line.strip().split(maxsplit=1)
        entries[i][0].insert(0, name)
        entries[i][1].insert(0, phone)


# Main window setup
root = tk.Tk()
root.title("Pastiri i ovcice")
root.geometry("600x800")
root.configure(background='pink')

# Number of participants
tk.Label(root, text="Broj ovcica i pastira:", background="lightblue1").grid(row=0, column=0, padx=10, pady=10)
num_participants_entry = tk.Entry(root)
num_participants_entry.grid(row=0, column=1, padx=10, pady=10)

# Button to generate participant fields
create_button = tk.Button(root, text="Unesi", command=create_participant_fields,
                          activebackground="royalblue1",
                          activeforeground="white",
                          bg="lightblue1"
                          )
create_button.grid(row=1, column=0, padx=10, pady=10)

# Button to load participants from file
load_button = tk.Button(root, text="Učitaj iz datoteke", command=load_from_file,
                        activebackground="royalblue1",
                        activeforeground="white",
                        bg="lightblue1"
                        )
load_button.grid(row=1, column=1, padx=10, pady=10)

# Frame to hold participant input fields
participants_frame = tk.Frame(root)
participants_frame.grid(row=2, columnspan=2, padx=10, pady=10)

# Time inputs
tk.Label(root, text="Sat slanja poruke(0-24):", background="lightblue1").grid(row=3, column=0, padx=10, pady=10)
hour_entry = tk.Entry(root)
hour_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Minuta slanja poruke(barem dvije minute od sada):", background="lightblue1").grid(row=4, column=0,
                                                                                                       padx=10, pady=10)
minute_entry = tk.Entry(root)
minute_entry.grid(row=4, column=1, padx=10, pady=10)

# Send messages button
send_button = tk.Button(root, text="Posalji pastirima njihove ovcice :)", command=send_messages,
                        activebackground="royalblue1",
                        activeforeground="white",
                        bg="lightblue1"
                        )
send_button.grid(row=5, columnspan=2, padx=10, pady=20)

root.mainloop()
