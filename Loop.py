import numpy as np
import matplotlib
import Ravin
import tkinter as tk
from tkinter import messagebox, ttk
matplotlib.use('TkAgg')  # Use 'TkAgg' or 'Qt5Agg' as a backend
import matplotlib.pyplot as plt
from scipy.integrate import odeint


def RunModule(Masse, Largeur, Hauteur, Longueur, Cx, Cz, mu, AccMoyenne, V0,T,nos_active, nos_location, aileron_active):
   # Constantes physiques
   g = 9.806  # Gravité (m/s^2)
   ro = 1.292  # Masse volumique de l'air (kg/m^3)
   drag_area = Largeur * Hauteur  # Surface frontale (m^2)
   boost = 1
   if nos_active == True and nos_location == "le looping":
       boost = 1.3
   # Paramètres du circuit
   rayon_looping = 6  # Rayon du looping (m)
   X0 = 0  # Position initiale
   omega0 = V0 / rayon_looping  # Vitesse angulaire initiale (rad/s)
   y0 = [0, omega0]  # Conditions initiales [position, vitesse angulaire]


   # Equation différentielle
   def equation(y, t):
       theta, omega = y  # theta = y[0], omega = y[1]
       calcul = (-Masse * g * (np.sin(theta) + mu * np.cos(theta))
                 - omega ** 2 * (mu * Masse * rayon_looping + 0.5 * Cx * ro * drag_area * rayon_looping ** 2)
                 + AccMoyenne *boost * Masse) / (Masse * rayon_looping)
       return [omega, calcul]  # [theta_prime, theta_double_prime]


   # Vérification si la voiture complète le looping
   def completes_loop(V0):
       omega0 = V0 / rayon_looping
       sol = odeint(equation, [0, omega0], np.linspace(0, 10, 1000))
       return np.any(sol[:, 0] >= 2 * np.pi)  # Vérifie si theta atteint 2*pi


   # Recherche binaire pour trouver Vmin
   def find_vmin():
       V_low, V_high = 0, 50  # Bornes initiales de recherche
       tol = 1e-2  # Tolérance pour la convergence
       while V_high - V_low > tol:
           V_mid = (V_low + V_high) / 2
           if completes_loop(V_mid):
               V_high = V_mid
           else:
               V_low = V_mid
       return (V_low + V_high) / 2


   # Calcul de Vmin
   Vmin = find_vmin()


   # Vecteur temps
   t = np.linspace(0, 5, 1000)
   sol = odeint(equation, y0, t)


   # Détection de l'angle theta = 2*pi
   i = 0
   while i < len(sol) and sol[i][0] < 2 * np.pi:
       i += 1


   # Vitesse finale de la voiture après le looping
   v_looping_af = sol[i - 1][1] * rayon_looping
   print("Vitesse minimale requise : {:.3f} m/s".format(Vmin))
   print("Vitesse initiale : {:.3f} m/s | Vitesse finale : {:.3f} m/s".format(V0, v_looping_af))
   print("Le temps final du looping est de : {:.3f} s".format(t[i - 1]))


   # Pass the rounded value to the function


   if V0>= Vmin:
       Ravin.RunModule(Masse, Largeur, Hauteur, Longueur, Cx, Cz, mu, AccMoyenne, round(v_looping_af, 3),t[i - 1] + T,nos_active, nos_location, aileron_active)
       # Tracer des résultats
       plt.figure(2, figsize=(10, 6))
       plt.plot(t[:i], sol[:i, 1] * rayon_looping, "olive")
       plt.title("Vitesse de la voiture avec frottements en fonction du temps")
       plt.xlabel("Temps (s)")
       plt.ylabel("Vitesse (m/s)")
       plt.grid()
       plt.tight_layout()


       # Ajout des informations dans le graphique
       plt.figtext(
           0.5, 0.01,
           "Vitesse minimale requise : {:.3f} m/s | Vitesse initiale : {:.3f} m/s | Vitesse finale : {:.3f} m/s | Temps final : {:.3f} s".format(
               Vmin, V0, v_looping_af, t[i - 1]
           ),
           fontsize=10, ha="center", va="center"
       )
       plt.gcf().canvas.manager.set_window_title("Simulation Looping")
       plt.show(block=False)
   else:
       messagebox.showerror("Erreur d'Entrée",f"La voiture n'a pas pu franchir le looping en raison d'une V0 insuffisante : {V0:.2f} m/s < {Vmin:.2f} m/s")
