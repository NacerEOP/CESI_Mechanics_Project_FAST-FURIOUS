import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import FinDePiste
from tkinter import messagebox, ttk
# Variable globale pour stocker vx lorsque y = 0
final_vx_at_y0 = 0.0


def Run Module(m, Largeur, Hauteur, Longueur, Cx, Cz, mu, Acc Moyenne, V0,T,nos_active, nos_location, aileron_active):
   # Constantes
   rho = 1.225  # Densité de l'air (kg/m^3)


   A = Largeur * Hauteur
   g = 9.81  # Gravité (m/s^2)
   SurfacePortBonus = 0


   CzBonus = 1
   CxReduit = 1
   if aileron_active == True:


       SurfacePortBonus = 0.8
       CzBonus = 1.1
       CxReduit = 1 - 0.05


   S = Longueur * Largeur + SurfacePortBonus  # Aire de la section transversale (m^2)
   # Équations du mouvement
   def equations(state, t):
       x, vx, y, vy = state
       v = np.sqrt(vx ** 2 + vy ** 2)  # Amplitude de la vitesse


       # Accélérations avec traînée et portance
       ax = -0.5 * rho * Cx*CxReduit * A * v * vx / (m)
       ay = -g + 0.5 * rho * Cz*CzBonus * S * v * vy / (m)


       return [vx, ax, vy, ay]


   # Fonction pour résoudre la trajectoire
   def solve_trajectory(v0_x):
       # Conditions initiales : x0, v0_x, y0, v0_y
       initial_conditions = [0, v0_x, 1, 0]


       # Intervalle de temps
       t = np.linspace(0, 0.5, 1000)  # Résolution jusqu'à 0,5 secondes


       # Résolution des EDO
       solution = odeint(equations, initial_conditions, t)


       x = solution[:, 0]  # Position horizontale
       y = solution[:, 2]  # Position verticale


       return x, y, t


   # Fonction pour trouver la vitesse initiale minimale v0_x pour atteindre x=9 lorsque y=0
   def find_min_v0(target_x):
       def condition(v0_x):
           x, y, _ = solve_trajectory(v0_x)
           # Trouver où y croise 0 et retourner la valeur de x correspondante
           for i in range(len(y) - 1):
               if y[i] > 0 and y[i + 1] <= 0:  # Détecter un croisement
                   return x[i] - target_x
           return -target_x  # Si y n'atteint jamais 0, retourner une erreur élevée


       # Méthode de bissection pour trouver la v0_x minimale
       v0_low = 1.0  # Limite inférieure
       v0_high = 50.0  # Limite supérieure
       tol = 1e-2  # Tolérance pour la précision


       while v0_high - v0_low > tol:
           v0_mid = (v0_low + v0_high) / 2
           if condition(v0_mid) >= 0:  # Dépasse ou atteint la cible
               v0_high = v0_mid
           else:
               v0_low = v0_mid


       return v0_high


   # Fonction pour trouver la vitesse à y = 0
   def get_exit_velocity(y, vx, vy):
       global final_vx_at_y0  # Utiliser la variable globale
       for i in range(len(y) - 1):
           if y[i] > 0 and y[i + 1] <= 0:  # Détecter le croisement y = 0
               final_vx_at_y0 = vx[i]  # Stocker la composante horizontale v_x
               v_exit = np.sqrt(vx[i]**2 + vy[i]**2)  # Vitesse totale à y = 0
               return v_exit
       return 0.0  # Si aucun croisement n'est trouvé


   # Trouver la vitesse horizontale initiale minimale
   target_x = 9  # Position cible en x
   minimal_v0 = find_min_v0(target_x)


   # Résoudre la trajectoire en utilisant la vitesse initiale donnée (V0 réel)
   x_given, y_given, t = solve_trajectory(V0)


   # Calculer les composantes de la vitesse pour la trajectoire donnée
   vx_given = np.gradient(x_given, t)
   vy_given = np.gradient(y_given, t)


   # Calculer la vitesse de sortie à y = 0
   exit_velocity = get_exit_velocity(y_given, vx_given, vy_given)


   # Affichage de la composante v_x lorsque y=0
   print(f"Composante horizontale finale v_x lorsque y=0 : {final_vx_at_y0:.2f} m/s")


   # Résoudre la trajectoire en utilisant la vitesse minimale v0 pour comparaison (optionnel)
   x_min, y_min, _ = solve_trajectory(minimal_v0)


   if V0 >= minimal_v0:




       # Trouver le temps où y atteint 0
       time_at_y0 = None
       for i in range(len(y_given) - 1):
           if y_given[i] > 0 and y_given[i + 1] <= 0:  # Croisement de y = 0
               # Interpolation pour calculer le temps précis
               time_at_y0 = t[i] + (0 - y_given[i]) * (t[i + 1] - t[i]) / (y_given[i + 1] - y_given[i])
               break  # On s'arrête au premier croisement


       # Tracer la trajectoire résultante pour la vitesse donnée V0
       FinDePiste.RunModule(m, Largeur, Hauteur, Longueur, Cx, Cz, mu, AccMoyenne, exit_velocity, T + time_at_y0,nos_active, nos_location, aileron_active)
       plt.figure(3, figsize=(10, 6))
       plt.plot(x_given, y_given, label=f'Trajectoire avec V0 réel = {V0:.2f} m/s', color='blue')
       plt.plot(x_min, y_min, label=f'Trajectoire avec V0 minimal = {minimal_v0:.2f} m/s', color='orange',
                linestyle='--')


       plt.axhline(0, color='gray', linestyle='--')  # Ligne du sol
       plt.axvline(target_x, color='red', linestyle='--', label='Cible x = 9 m')


       plt.title('Trajectoire de la Voiture')
       plt.xlabel('x (m)')
       plt.ylabel('y (m)')
       plt.legend()
       plt.grid()


       # Ajouter les informations calculées en bas du graphique
       plt.figtext(0.5, 0.01,
                   f"V0 minimal pour atteindre x = {target_x} m : {minimal_v0:.2f} m/s | "
                   f"V0 réel = {V0:.2f} m/s | Vitesse de sortie (y=0) = {exit_velocity:.2f} m/s | "
                   f"Temps pour y=0 : {time_at_y0:.3f} s",
                   fontsize=10, ha="center", va="center")


       plt.gcf().canvas.manager.set_window_title("Simulation Ravin")
       plt.show(block=False)
   else:
       messagebox.showerror("Erreur d'Entrée",f"La voiture n'a pas pu franchir le ravin en raison d'une V0 insuffisante : {V0:.2f} m/s < {minimal_v0:.2f} m/s")
