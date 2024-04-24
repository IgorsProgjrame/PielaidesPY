import tkinter as tk
from tkinter import ttk
from database_manager import Database


bg_color = '#222222'
access = 0

database = Database()

access_denied_alert = 'Nav atļauta piekļuve!'
insert_all_values_alert = 'Ievadiet visas vērtības!'
wrong_credentials_alert = 'Nepareizs lietotājvārds vai parole!'
select_any_alert = 'Izvēlies kādu no precēm!'

def create_login_interface():
    login_frame = tk.Frame(root, width=250, height=300, bg=bg_color)

    login_text = tk.Label(login_frame, text='Pieslēgties', font=('Arial', 15), fg='#fff', bg=bg_color)
    login_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    username_text = tk.Label(login_frame, text='Lietotājvārds', bg=bg_color, fg='white')
    username_input = tk.Entry(login_frame)
    username_text.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    username_input.grid(row=1, column=1, padx=10, pady=10, sticky='w') 

    password_text = tk.Label(login_frame, text='Parole', bg=bg_color, fg='white')
    password_input = tk.Entry(login_frame, show='•')
    password_text.grid(row=2, column=0, padx=10, pady=10, sticky='e')
    password_input.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    submit_button = tk.Button(login_frame, text='Pieslēgties', relief=tk.FLAT,
                              command=lambda: authenticate(username_input.get(), password_input.get(), login_frame))
    submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=30, sticky='nsew')

    login_frame.grid_rowconfigure(0, weight=1)
    login_frame.grid_columnconfigure(0, weight=1)
    login_frame.grid_columnconfigure(1, weight=1)
    login_frame.pack(pady=50)


def authenticate(username_input, password_input, login_frame):
    global access
    access = database.authenticate(username_input=username_input, password_input=password_input)

    if access:
        login_frame.destroy()
        menu()
    else:
        alert = tk.Label(login_frame, text=wrong_credentials_alert, bg=bg_color, fg='#FF0000', font=('Ariel', 12))
        alert.grid(row=10, column=0, columnspan=2)
        login_frame.after(4000, lambda: alert.destroy())

def menu():
    background_frame = tk.Frame(root, width=600, height=300, bg=bg_color)

    buttons_info = [
        ("Apskatīt Noliktavu", lambda: check_inventory(background_frame)),
        ("Pievienot Preci", lambda: add_item(background_frame)),
        ("Dzēst Preci", lambda: check_inventory(background_frame, delete=True)),
        ("Rediģēt Noliktavu", lambda: check_inventory(background_frame, configure=True))
    ]

    for idx, (button_text, button_command) in enumerate(buttons_info):
        button = tk.Button(background_frame, text=button_text, width=16, height=9, command=button_command, bg='#fff')
        button.grid(row=0, column=idx, padx=10, pady=10, sticky='e')


    background_frame.grid_rowconfigure(0, weight=1)
    for i in range(len(buttons_info)):
        background_frame.grid_columnconfigure(i, weight=1)
    background_frame.pack(pady=50)


def check_inventory(background_frame, delete=False, configure=False):
    access_data = database.return_access(access)
    if (delete == True and 'DeleteItem' in access_data) or (configure == True and 'UpdateItem' in access_data) or (configure == False and delete == False):
        background_frame.destroy()
        inventory_frame = tk.Frame(root, width=600, height=300, bg=bg_color)
        inventory_frame.pack(pady=50)


        columns = ('Produkta ID', 'Nosaukums', 'Apjoms', 'Nepieciešamais Apjoms')
        tree = ttk.Treeview(inventory_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        rows = database.check_inventory()
        for row in rows:
            tree.insert('', 'end', values=row)
        
        scrollbar = ttk.Scrollbar(inventory_frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        access_data = database.return_access(access)

        if delete:
            del_button = tk.Button(inventory_frame, text='Dzēst', relief=tk.FLAT, command=lambda: delete_selected_item(tree))
            del_button.grid(row=1, column=0, columnspan=2, pady=10)
        elif configure:
            config_button = tk.Button(inventory_frame, text='Rediģēt', relief=tk.FLAT, command=lambda: add_item(inventory_frame, tree=tree, configure=True))
            config_button.grid(row=1, column=0, columnspan=2, pady=10)

        back_button = tk.Button(inventory_frame, text='Atpakaļ', relief=tk.FLAT, command=lambda: back_to_menu(inventory_frame))
        back_button.grid(row=2, column=0, columnspan=2, pady=10)
    elif (delete and 'DeleteItem' not in access_data) or (configure and 'UpdateItem' not in access_data):
        alert = tk.Label(background_frame, text="Šim lietotājam nav piekļuves", bg=bg_color, fg='#FF0000', font=('Ariel', 12))
        alert.grid(row=10, column=0, columnspan=2)
        background_frame.after(4000, lambda: alert.destroy())

    
def add_item(menu_frame, configure=False, tree=None):
    access_data = database.return_access(access)

    if tree:
        selected_item = tree.selection()

    if ('AddItem' in access_data and configure == False) or ('UpdateItem' in access_data and configure == True):
        if (configure == True and len(selected_item) > 0) or configure == False:
            if configure:
                menu_frame.pack_forget()
                title_text = 'Rediģēt Noliktavu'
            else:
                title_text = 'Pievienot Preci'
                menu_frame.destroy()

            add_item_frame = tk.Frame(root, width=600, height=300, bg=bg_color)

            title_text = tk.Label(add_item_frame, text=title_text, bg=bg_color, fg='#fff', font=('Arial', 15))
            title_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

            item_details = [
                ("Nosaukums", tk.Entry(add_item_frame)),
                ("Apjoms", ttk.Spinbox(add_item_frame, from_=0, to=1000000000, increment=1, width=18)),
                ("Nepieciešamais Apjoms", ttk.Spinbox(add_item_frame, from_=0, to=1000000000, increment=1, width=18))
            ]

            for idx, (label_text, entry_widget) in enumerate(item_details):
                label = tk.Label(add_item_frame, text=label_text, bg=bg_color, fg='white')
                label.grid(row=idx + 1, column=0, padx=10, pady=10, sticky='e')
                entry_widget.grid(row=idx + 1, column=1, padx=10, pady=10, sticky='w')

            if configure:
                selected_item = tree.selection()

                if len(selected_item) > 0:
                    item_id = tree.item(selected_item)['values'][0]
                    item_details[0][1].insert(0, tree.item(selected_item)['values'][1])
                    item_details[1][1].delete(0, tk.END)
                    item_details[1][1].insert(0, tree.item(selected_item)['values'][2])
                    item_details[2][1].delete(0, tk.END)
                    item_details[2][1].insert(0, tree.item(selected_item)['values'][3])
            
                    confirm_button = tk.Button(add_item_frame, text='Apstiprināt', relief=tk.FLAT,
                                            command=lambda: update_item(item_id, *get_item_values(item_details), menu_frame, add_item_frame))
                    confirm_button.grid(row=len(item_details) + 1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
            else:
                confirm_button = tk.Button(add_item_frame, text='Pievienot Preci', relief=tk.FLAT,
                                        command=lambda: insert_item(*get_item_values(item_details), menu_frame, add_item_frame))
                confirm_button.grid(row=len(item_details) + 1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
                

            back_button = tk.Button(add_item_frame, text='Atpakaļ', relief=tk.FLAT, command=lambda: back_to_menu(add_item_frame))
            back_button.grid(row=len(item_details) + 2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

            add_item_frame.grid_rowconfigure(0, weight=1)

            for _ in range(len(item_details) + 3):
                add_item_frame.grid_columnconfigure(0, weight=1)
                add_item_frame.grid_columnconfigure(1, weight=1)
            add_item_frame.pack(pady=50)

    elif configure == False and 'Additem' not in access_data:
        alert = tk.Label(menu_frame, text="Šim lietotājam nav piekļuves", bg=bg_color, fg='#FF0000', font=('Ariel', 12))
        alert.grid(row=10, column=0, columnspan=2)
        menu_frame.after(4000, lambda: alert.destroy())



def get_item_values(item_details):
    return [entry_widget.get() for _, entry_widget in item_details]


def insert_item(name, quantity, required_quantity, menu_frame, add_item_frame):
   
    if name and quantity and required_quantity:
        try:
            quantity = int(quantity)
            required_quantity=int(required_quantity)
            database.add_item(name, quantity, required_quantity)
            add_item_frame.destroy()
            menu()
        except: 
            alert = tk.Label(add_item_frame, text="Radās problēma: err0x73536328367297", bg=bg_color, fg='#FF0000', font=('Ariel', 12))
            alert.grid(row=10, column=0, columnspan=2)
            add_item_frame.after(4000, lambda: alert.destroy())
    else:
        alert = tk.Label(add_item_frame, text=insert_all_values_alert, bg=bg_color, fg='#FF0000', font=('Ariel', 12))
        alert.grid(row=10, column=0, columnspan=2)
        add_item_frame.after(4000, lambda: alert.destroy())


def update_item(item_id, name, quantity, required_quantity, menu_frame, add_item_frame):
    try:
        quantity = int(quantity)
        required_quantity=int(required_quantity)
        database.edit_item(item_id, name, quantity, required_quantity)
        add_item_frame.destroy()
        menu() 
    except: 
        alert = tk.Label(add_item_frame, text="Radās problēma: err0x7052532836790", bg=bg_color, fg='#FF0000', font=('Ariel', 12))
        alert.grid(row=10, column=0, columnspan=2)
        add_item_frame.after(4000, lambda: alert.destroy())
    


def back_to_menu(frame):
    if frame:
        frame.destroy()
    menu()


def delete_selected_item(tree):
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.item(selected_item)['values'][0]
        database.delete_item(item_id)
        tree.delete(selected_item)


root = tk.Tk()
root.geometry('800x700')
root['bg'] = '#323232'


title = tk.Label(root, text='Noliktavas Pārvaldnieks', bg='#323232', fg='#fff', font=('Arial', 20))
title.pack(pady=10)


create_login_interface()

root.mainloop()

