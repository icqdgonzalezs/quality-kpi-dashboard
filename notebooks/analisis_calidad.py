import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv('../data/calidad_muestra.csv')
df['tasa_defectos'] = df['unidades_defectuosas'] / df['unidades_producidas'] * 100

print("=== ANÁLISIS DE KPIs DE CALIDAD ===")
print(f"Tasa de defectos promedio: {df['tasa_defectos'].mean():.2f}%")
print(f"Lote con más defectos: {df.loc[df['unidades_defectuosas'].idxmax(), 'lote']} ({df['unidades_defectuosas'].max()} defectos)")

pareto = df['defecto_tipo'].value_counts()
print("\nFrecuencia de defectos:")
print(pareto)

plt.figure()
pareto.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Diagrama de Pareto - Tipos de Defecto')
plt.xlabel('Tipo de defecto')
plt.ylabel('Cantidad')
plt.tight_layout()
os.makedirs('../imagenes', exist_ok=True)
plt.savefig('../imagenes/pareto_defectos.png')
print("\n📊 Gráfico guardado en imagenes/pareto_defectos.png")
