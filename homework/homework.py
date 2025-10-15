import pandas as pd
import matplotlib.pyplot as plt
import os

# === Crear carpetas necesarias ===
os.makedirs("files/output", exist_ok=True)
os.makedirs("files/plots", exist_ok=True)

# === 1. Leer las tablas base ===
timesheet = pd.read_csv("files/input/timesheet.csv")
drivers = pd.read_csv("files/input/drivers.csv")

# Convertir columnas a numéricas
timesheet["hours-logged"] = pd.to_numeric(timesheet["hours-logged"], errors="coerce")
timesheet["miles-logged"] = pd.to_numeric(timesheet["miles-logged"], errors="coerce")

# === 2. Crear "timesheet_with_means" ===
mean_hours = timesheet.groupby("driverId")["hours-logged"].mean().reset_index()
mean_hours.rename(columns={"hours-logged": "mean_hours-logged"}, inplace=True)

timesheet_with_means = pd.merge(timesheet, mean_hours, on="driverId", how="left")

# === 3. Crear "timesheet_below" ===
timesheet_below = timesheet_with_means[
    timesheet_with_means["hours-logged"] < timesheet_with_means["mean_hours-logged"]
]

# === 4. Crear "sum_timesheet" ===
sum_timesheet = (
    timesheet.groupby("driverId")[["hours-logged", "miles-logged"]]
    .sum()
    .reset_index()
)

# === 5. Crear "min_max_timesheet" ===
min_max_timesheet = (
    timesheet.groupby("driverId")["hours-logged"]
    .agg(min_hours="min", max_hours="max")
    .reset_index()
)

# === 6. Crear "summary" ===
drivers_subset = drivers[["driverId", "name"]]
summary = pd.merge(sum_timesheet, drivers_subset, on="driverId", how="left")

# === 7. Guardar "summary" como CSV ===
summary.to_csv("files/output/summary.csv", index=False)
print("✅ Archivo 'files/output/summary.csv' creado correctamente.")

# === 8. Crear "top10" ===
top10 = (
    summary.sort_values("miles-logged", ascending=False)
    .head(10)
    .reset_index(drop=True)
)

# === 9. Gráfico de barras horizontales ===
plt.figure(figsize=(8, 6))
plt.barh(top10["name"], top10["miles-logged"])
plt.xlabel("Millas registradas")
plt.ylabel("Conductor")
plt.title("Top 10 conductores con más millas registradas")
plt.gca().invert_yaxis()
plt.tight_layout()

# Guardar gráfico
plot_path = "files/plots/top10_drivers.png"
plt.savefig(plot_path)
plt.close()  # cerrar para liberar memoria

# === 10. Verificar que el archivo existe ===
print(f"✅ Gráfico guardado correctamente en: {plot_path}")