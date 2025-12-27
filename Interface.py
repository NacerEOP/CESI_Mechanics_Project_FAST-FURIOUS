import tkinter as tk
from tkinter import messagebox, ttk


import Pente


PRESETS = {
   "Modèle 1 : Dodge Charger R/T, 1970": {"mass": 1760, "width": 1.95, "height": 1.35, "length": 5.28, "Cx": 0.38,
                                          "Cz": 0.3, "mu": 0.1, "a_avg": 5.1},
   "Modèle 2 : Toyota Supra Mark IV, 1994": {"mass": 1615, "width": 1.81, "height": 1.27, "length": 4.51, "Cx": 0.29,
                                             "Cz": 0.3, "mu": 0.1, "a_avg": 5},
   "Modèle 3 : Chevrolet Yenko Camaro 1969": {"mass": 1498, "width": 1.88, "height": 1.30, "length": 4.72, "Cx": 0.35,
                                              "Cz": 0.3, "mu": 0.1, "a_avg": 5.3},
   "Modèle 4 : Mazda RX-7 FD": {"mass": 1385, "width": 1.75, "height": 1.23, "length": 4.3, "Cx": 0.28, "Cz": 0.3,
                                "mu": 0.1, "a_avg": 5.2},
   "Modèle 5 : Nissan Skyline GTR-R34, 1999": {"mass": 1540, "width": 1.79, "height": 1.36, "length": 4.6, "Cx": 0.34,
                                               "Cz": 0.3, "mu": 0.1, "a_avg": 5.8},
   "Modèle 6 : Mitsubishi Lancer Evolution VII": {"mass": 1600, "width": 1.81, "height": 1.48, "length": 4.51,
                                                  "Cx": 0.28, "Cz": 0.3, "mu": 0.1, "a_avg": 5}
}




def load_preset(*args):
   preset_name = preset_var.get()
   if preset_name in PRESETS:
       preset = PRESETS[preset_name]
       mass_entry.delete(0, tk.END)
       mass_entry.insert(0, preset["mass"])
       width_entry.delete(0, tk.END)
       width_entry.insert(0, preset["width"])
       height_entry.delete(0, tk.END)
       height_entry.insert(0, preset["height"])
       length_entry.delete(0, tk.END)
       length_entry.insert(0, preset["length"])
       cx_entry.delete(0, tk.END)
       cx_entry.insert(0, preset["Cx"])
       cz_entry.delete(0, tk.END)
       cz_entry.insert(0, preset["Cz"])
       mu_entry.delete(0, tk.END)
       mu_entry.insert(0, preset["mu"])
       a_avg_entry.delete(0, tk.END)
       a_avg_entry.insert(0, preset["a_avg"])




def submit_parameters():
   try:
       mass = float(mass_entry.get())
       width = float(width_entry.get())
       height = float(height_entry.get())
       length = float(length_entry.get())
       cx = float(cx_entry.get())
       cz = float(cz_entry.get())
       mu = float(mu_entry.get())
       a_avg = float(a_avg_entry.get())


       # Retrieve NOS and Aileron options
       nos_active = nos_var.get()
       nos_location = nos_location_var.get() if nos_active else "Non activé"
       aileron_active = aileron_var.get()
       massAileron = 0
       if aileron_active == True:
           massAileron = 45
       # Call RunModule with all required arguments
       Pente.RunModule(mass+ massAileron, width, height, length, cx, cz, mu, a_avg, nos_active, nos_location, aileron_active)


       # Update the table
       tree.insert("", "end", values=(mass, width, height, length, cx, cz, mu, a_avg, nos_active, nos_location, aileron_active))


   except ValueError:
       messagebox.showerror("Erreur de saisie", "Veuillez entrer des valeurs numériques valides pour tous les champs.")




root = tk.Tk()
root.title("Saisie des Paramètres de Voiture")


# Variables
preset_var = tk.StringVar(value="Choisissez un Modèle")
nos_var = tk.BooleanVar(value=False)
nos_location_var = tk.StringVar(value="Choisir emplacement")
aileron_var = tk.BooleanVar(value=False)


# Widgets de base
preset_label = tk.Label(root, text="Choisissez un Modèle :")
preset_label.grid(row=0, column=0, padx=5, pady=5)
preset_dropdown = tk.OptionMenu(root, preset_var, *PRESETS.keys(), command=load_preset)
preset_dropdown.grid(row=0, column=1, padx=5, pady=5)


fields = [("Masse (kg)", 1), ("Largeur (m)", 2), ("Hauteur (m)", 3), ("Longueur (m)", 4),
         ("Coefficient de Traînée (Cx)", 5), ("Coefficient de Portance (Cz)", 6),
         ("Coefficient de Frottement (Mu)", 7), ("Accélération Moyenne (m/s²)", 8)]
entries = []


for label, row in fields:
   tk.Label(root, text=label).grid(row=row, column=0, padx=5, pady=5)
   entry = tk.Entry(root)
   entry.grid(row=row, column=1, padx=5, pady=5)
   entries.append(entry)


mass_entry, width_entry, height_entry, length_entry, cx_entry, cz_entry, mu_entry, a_avg_entry = entries


# Options personnalisables
nos_check = tk.Checkbutton(root, text="Activer Booster NOS", variable=nos_var)
nos_check.grid(row=9, column=0, sticky="w", padx=5, pady=5)


nos_location_label = tk.Label(root, text="Emplacement NOS :")
nos_location_label.grid(row=10, column=0, padx=5, pady=5)
nos_location_menu = ttk.Combobox(root, textvariable=nos_location_var, state="disabled",
                                values=["la pente", "le looping", "le ravin", "la fin de piste"])
nos_location_menu.grid(row=10, column=1, padx=5, pady=5)




def toggle_nos_location(*args):
   state = "readonly" if nos_var.get() else "disabled"
   nos_location_menu.config(state=state)




nos_var.trace_add("write", toggle_nos_location)


aileron_check = tk.Checkbutton(root, text="Activer Aileron et Jupe Avant", variable=aileron_var)
aileron_check.grid(row=11, column=0, sticky="w", padx=5, pady=5)


# Bouton soumettre
submit_button = tk.Button(root, text="Soumettre", command=submit_parameters)
submit_button.grid(row=12, column=0, columnspan=2, pady=10)


# Tableau
table_frame = tk.Frame(root)
table_frame.grid(row=13, column=0, columnspan=2, padx=10, pady=10)


columns = (
"Masse", "Largeur", "Hauteur", "Longueur", "Cx", "Cz", "Mu", "Accélération Moyenne", "NOS Activé", "Emplacement NOS",
"Aileron Activé")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")


for col in columns:
   tree.heading(col, text=col)
   tree.column(col, width=100, anchor="center")


tree.pack()


root.mainloop()
import tkinter as tk
from tkinter import messagebox, ttk


import Pente


PRESETS = {
   "Modèle 1 : Dodge Charger R/T, 1970": {"mass": 1760, "width": 1.95, "height": 1.35, "length": 5.28, "Cx": 0.38,
                                          "Cz": 0.3, "mu": 0.1, "a_avg": 5.1},
   "Modèle 2 : Toyota Supra Mark IV, 1994": {"mass": 1615, "width": 1.81, "height": 1.27, "length": 4.51, "Cx": 0.29,
                                             "Cz": 0.3, "mu": 0.1, "a_avg": 5},
   "Modèle 3 : Chevrolet Yenko Camaro 1969": {"mass": 1498, "width": 1.88, "height": 1.30, "length": 4.72, "Cx": 0.35,
                                              "Cz": 0.3, "mu": 0.1, "a_avg": 5.3},
   "Modèle 4 : Mazda RX-7 FD": {"mass": 1385, "width": 1.75, "height": 1.23, "length": 4.3, "Cx": 0.28, "Cz": 0.3,
                                "mu": 0.1, "a_avg": 5.2},
   "Modèle 5 : Nissan Skyline GTR-R34, 1999": {"mass": 1540, "width": 1.79, "height": 1.36, "length": 4.6, "Cx": 0.34,
                                               "Cz": 0.3, "mu": 0.1, "a_avg": 5.8},
   "Modèle 6 : Mitsubishi Lancer Evolution VII": {"mass": 1600, "width": 1.81, "height": 1.48, "length": 4.51,
                                                  "Cx": 0.28, "Cz": 0.3, "mu": 0.1, "a_avg": 5}
}




def load_preset(*args):
   preset_name = preset_var.get()
   if preset_name in PRESETS:
       preset = PRESETS[preset_name]
       mass_entry.delete(0, tk.END)
       mass_entry.insert(0, preset["mass"])
       width_entry.delete(0, tk.END)
       width_entry.insert(0, preset["width"])
       height_entry.delete(0, tk.END)
       height_entry.insert(0, preset["height"])
       length_entry.delete(0, tk.END)
       length_entry.insert(0, preset["length"])
       cx_entry.delete(0, tk.END)
       cx_entry.insert(0, preset["Cx"])
       cz_entry.delete(0, tk.END)
       cz_entry.insert(0, preset["Cz"])
       mu_entry.delete(0, tk.END)
       mu_entry.insert(0, preset["mu"])
       a_avg_entry.delete(0, tk.END)
       a_avg_entry.insert(0, preset["a_avg"])




def submit_parameters():
   try:
       mass = float(mass_entry.get())
       width = float(width_entry.get())
       height = float(height_entry.get())
       length = float(length_entry.get())
       cx = float(cx_entry.get())
       cz = float(cz_entry.get())
       mu = float(mu_entry.get())
       a_avg = float(a_avg_entry.get())


       # Retrieve NOS and Aileron options
       nos_active = nos_var.get()
       nos_location = nos_location_var.get() if nos_active else "Non activé"
       aileron_active = aileron_var.get()
       massAileron = 0
       if aileron_active == True:
           massAileron = 45
       # Call RunModule with all required arguments
       Pente.RunModule(mass+ massAileron, width, height, length, cx, cz, mu, a_avg, nos_active, nos_location, aileron_active)


       # Update the table
       tree.insert("", "end", values=(mass, width, height, length, cx, cz, mu, a_avg, nos_active, nos_location, aileron_active))


   except ValueError:
       messagebox.showerror("Erreur de saisie", "Veuillez entrer des valeurs numériques valides pour tous les champs.")




root = tk.Tk()
root.title("Saisie des Paramètres de Voiture")


# Variables
preset_var = tk.StringVar(value="Choisissez un Modèle")
nos_var = tk.BooleanVar(value=False)
nos_location_var = tk.StringVar(value="Choisir emplacement")
aileron_var = tk.BooleanVar(value=False)


# Widgets de base
preset_label = tk.Label(root, text="Choisissez un Modèle :")
preset_label.grid(row=0, column=0, padx=5, pady=5)
preset_dropdown = tk.OptionMenu(root, preset_var, *PRESETS.keys(), command=load_preset)
preset_dropdown.grid(row=0, column=1, padx=5, pady=5)


fields = [("Masse (kg)", 1), ("Largeur (m)", 2), ("Hauteur (m)", 3), ("Longueur (m)", 4),
         ("Coefficient de Traînée (Cx)", 5), ("Coefficient de Portance (Cz)", 6),
         ("Coefficient de Frottement (Mu)", 7), ("Accélération Moyenne (m/s²)", 8)]
entries = []


for label, row in fields:
   tk.Label(root, text=label).grid(row=row, column=0, padx=5, pady=5)
   entry = tk.Entry(root)
   entry.grid(row=row, column=1, padx=5, pady=5)
   entries.append(entry)


mass_entry, width_entry, height_entry, length_entry, cx_entry, cz_entry, mu_entry, a_avg_entry = entries


# Options personnalisables
nos_check = tk.Checkbutton(root, text="Activer Booster NOS", variable=nos_var)
nos_check.grid(row=9, column=0, sticky="w", padx=5, pady=5)


nos_location_label = tk.Label(root, text="Emplacement NOS :")
nos_location_label.grid(row=10, column=0, padx=5, pady=5)
nos_location_menu = ttk.Combobox(root, textvariable=nos_location_var, state="disabled",
                                values=["la pente", "le looping", "le ravin", "la fin de piste"])
nos_location_menu.grid(row=10, column=1, padx=5, pady=5)




def toggle_nos_location(*args):
   state = "readonly" if nos_var.get() else "disabled"
   nos_location_menu.config(state=state)




nos_var.trace_add("write", toggle_nos_location)


aileron_check = tk.Checkbutton(root, text="Activer Aileron et Jupe Avant", variable=aileron_var)
aileron_check.grid(row=11, column=0, sticky="w", padx=5, pady=5)


# Bouton soumettre
submit_button = tk.Button(root, text="Soumettre", command=submit_parameters)
submit_button.grid(row=12, column=0, columnspan=2, pady=10)


# Tableau
table_frame = tk.Frame(root)
table_frame.grid(row=13, column=0, columnspan=2, padx=10, pady=10)


columns = (
"Masse", "Largeur", "Hauteur", "Longueur", "Cx", "Cz", "Mu", "Accélération Moyenne", "NOS Activé", "Emplacement NOS",
"Aileron Activé")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")


for col in columns:
   tree.heading(col, text=col)
   tree.column(col, width=100, anchor="center")


tree.pack()


root.mainloop()
