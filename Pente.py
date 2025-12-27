import numpy as np
from scipy.integrate import odeint
import matplotlib


matplotlib.use('TkAgg')  # Use 'TkAgg' or 'Qt5Agg' as a backend
import matplotlib.pyplot as plt
import Loop




def RunModule(Masse, Largeur, Hauteur, Longueur, Cx, Cz, mu, AccMoyenne,nos_active, nos_location, aileron_active):
   g = 9.806
   ro = 1.292
   boost = 1
   if nos_active == True and nos_location == "la pente":
       boost = 1.3


   A = Largeur * Hauteur
   anglePente = np.radians(3.7)


   V0 = 0
   X0 = 0
   y0 = [V0, X0]


   def SetDiffEq(y, t, g, ro, Masse, A, Cx, mu, AccMoyenne, anglePente):
       v = y[0]
       x = y[1]
       dv_dt = (g * np.sin(anglePente) + AccMoyenne*boost
                - mu * g * np.cos(anglePente)
                - (0.5 * Cx * ro * A * v ** 2) / Masse)
       dx_dt = v
       return [dv_dt, dx_dt]


   t = np.linspace(0, 5, 5000)


   solution = odeint(SetDiffEq, y0, t, args=(g, ro, Masse, A, Cx, mu, AccMoyenne, anglePente))


   v = solution[:, 0]
   x = solution[:, 1]


   threshold = 31
   idx_stop = np.argmax(x >= threshold)
   t_stop = t[idx_stop]
   v_stop = v[idx_stop]
   x_stop = x[idx_stop]


   temps_31m = t_stop


   print(f"Vitesse de la voiture à x = {x_stop:.2f} m : {v_stop:.2f} m/s")
   print(f"Temps pour atteindre x = {x_stop:.2f} m : {temps_31m:.2f} s")


   Loop.RunModule(Masse, Largeur, Hauteur, Longueur, Cx, Cz, mu, AccMoyenne, v_stop, temps_31m,nos_active, nos_location, aileron_active)


   plt.figure(1, figsize=(12, 6))
   plt.subplot(2, 1, 1)
   plt.plot(t[:idx_stop + 1], v[:idx_stop + 1], label='Vitesse (m/s)', color='blue')
   plt.xlabel('Temps (s)')
   plt.ylabel('Vitesse (m/s)')
   plt.title('Évolution de la vitesse')
   plt.grid()
   plt.legend()


   plt.subplot(2, 1, 2)
   plt.plot(t[:idx_stop + 1], x[:idx_stop + 1], label='Position (m)', color='red')
   plt.xlabel('Temps (s)')
   plt.ylabel('Position (m)')
   plt.title('Évolution de la position')
   plt.grid()
   plt.legend()


   plt.figtext(0.5, 0.01,
               f"Vitesse de sortie : {v_stop:.2f} m/s | Temps pour atteindre 31m : {temps_31m:.2f} secondes",
               fontsize=10, ha="center", va="center")


   plt.gcf().canvas.manager.set_window_title("Simulation Pente")
   plt.tight_layout()
   plt.show(block=False)
