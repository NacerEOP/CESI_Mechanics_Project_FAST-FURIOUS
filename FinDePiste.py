import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import tkinter as tk
from tkinter import messagebox, ttk


def RunModule(m, Largeur, Hauteur, Longueur, Cx, Cz, mu, am, V0,T,nos_active, nos_location, aileron_active):
   # Paramètres physiques
   R = m * 9.81  # Force normale (Poids, N) avec g = 9.81 m/s²
   ro = 1.292  # Masse volumique de l'air (kg/m³)
   k = 0.5 * Cx * Hauteur * Largeur * ro  # Coefficient de traînée aérodynamique (kg/m)
   boost = 1
   if nos_active == True and nos_location == "la fin de piste":
       boost = 1.3
   # Équation différentielle : dv/dt et dx/dt
   def equations(t, state):
       x, v = state
       dxdt = v
       dvdt = (m * am*boost - mu * R - k * v ** 2) / m
       return [dxdt, dvdt]


   # Fonction d'événement pour arrêter l'intégration lorsque x atteint 10m
   def stop_at_10m(t, state):
       x, v = state
       return x - 10


   stop_at_10m.terminal = True
   stop_at_10m.direction = 1


   # Conditions initiales
   x0 = 0
   initial_state = [x0, V0]


   # Vecteur temps
   t_span = (0, 50)
   t_eval = np.linspace(0, 50, 1000)  # Plus de points pour améliorer la précision


   # Résolution avec solve_ivp
   solution = solve_ivp(equations, t_span, initial_state, t_eval=t_eval, events=stop_at_10m, rtol=1e-8, atol=1e-10)


   # Extraire les résultats
   x = solution.y[0]
   v = solution.y[1]
   t = solution.t


   # Interpolation pour trouver exactement x = 10
   if solution.status == 1:  # Arrêt par événement
       # Prendre les deux derniers points avant et après x = 10
       x_before, x_after = x[-2], x[-1]
       t_before, t_after = t[-2], t[-1]
       v_before, v_after = v[-2], v[-1]


       # Interpolation linéaire pour le temps et la vitesse à x = 10
       t_10 = t_before + (10 - x_before) * (t_after - t_before) / (x_after - x_before)
       v_10 = v_before + (10 - x_before) * (v_after - v_before) / (x_after - x_before)
   else:
       t_10, v_10 = None, None


   # Tracer les résultats
   plt.figure(4,figsize=(10, 6))
   plt.subplot(2, 1, 1)
   plt.plot(t, v, label="Vitesse v_x(t)", color='b')
   plt.title("Vitesse v_x(t) en fonction du temps")
   plt.xlabel("Temps (s)")
   plt.ylabel("Vitesse (m/s)")
   plt.grid(True)


   plt.subplot(2, 1, 2)
   plt.plot(t, x, label="Position x(t)", color='r')
   plt.title("Position x(t) en fonction du temps")
   plt.xlabel("Temps (s)")
   plt.ylabel("Position (m)")
   plt.grid(True)


   # Ajouter la vitesse et le temps exacts à x = 10 m
   if t_10 is not None:
       plt.figtext(0.5, 0.01,
                   f"Vitesse finale à 10m : {v_10:.2f} m/s | Temps pour atteindre 10m : {t_10:.2f} s",
                   fontsize=10, ha="center", va="center")
   else:
       plt.figtext(0.5, 0.01, "L'événement x = 10m n'a pas été détecté", fontsize=10, ha="center", va="center")


   plt.tight_layout()


   plt.gcf().canvas.manager.set_window_title("Simulation Fin de piste")
   plt.show(block=False)


   success_window = tk.Toplevel(tk._default_root)
   success_window.title("Succès")
   success_window.geometry("300x100")  # Adjust size as needed
   tk.Label(success_window, text=f"Course terminée en : {T + t_10:.2f} secondes").pack(pady=20)
   tk.Button(success_window, text="OK", command=success_window.destroy).pack()
