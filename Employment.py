import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker  

# 1. CARGA DE DATOS OPTIMIZADA
print("Cargando datos de empleo (Filtrando columnas para acelerar la carga)...")

# Especificamos explícitamente las únicas columnas que nos interesan
columnas_necesarias = ['Group', 'Series_title_1', 'Series_title_2', 'Series_title_3', 'Period', 'Data_value']

# Cargamos el archivo pesado leyendo SOLO esas columnas
df = pd.read_csv('machine-readable-business-employment-data-mar-2026-quarter.csv', usecols=columnas_necesarias)
print("¡Datos cargados con éxito en segundos!")

# 2. FILTRADO EXACTO
df_agricola = df[
    (df['Group'] == 'Industry by employment variable') & 
    (df['Series_title_2'] == 'Agriculture, Forestry and Fishing') &
    (df['Series_title_1'] == 'Filled jobs') &  
    (df['Series_title_3'] == 'Actual')          
].copy()

# 3. LIMPIEZA Y ORDENAMIENTO
df_agricola = df_agricola.dropna(subset=['Data_value'])
df_agricola = df_agricola.sort_values(by='Period')
df_agricola['Period_Str'] = df_agricola['Period'].astype(str)

# 4. CONFIGURACIÓN DEL LIENZO
fig, ax = plt.subplots(figsize=(11, 5.5))

# Gráfico de Línea + Relleno de Área (Area Chart)
ax.plot(df_agricola['Period_Str'], df_agricola['Data_value'], 
        color='#2e7d32', linewidth=2.5, marker='o', markersize=4, markevery=2, alpha=0.9, label='Plazas Ocupadas')

# Sombreado debajo de la línea
ax.fill_between(df_agricola['Period_Str'], df_agricola['Data_value'], color='#e8f5e9', alpha=0.6)

# 5. LIMPIEZA VISUAL (Eliminar bordes innecesarios)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

# Formatear el eje Y para mostrar "K" (Miles)
ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x/1000), ',') + 'K'))

# Seleccionamos marcadores cada 4 trimestres (1 por año) para el eje X
ticks_anuales = df_agricola['Period_Str'].iloc[::4]
ax.set_xticks(ticks_anuales)

# Extraemos solo el año para mantener el diseño limpio y horizontal
etiquetas_anos = ticks_anuales.apply(lambda x: x.split('.')[0])
ax.set_xticklabels(etiquetas_anos, fontsize=10, color='#2c3e50')

# 6. TEXTOS GERENCIALES
ax.set_title('Evolución del Empleo en el Sector Agrícola (2011 - 2026)\nAnálisis Macroeconómico de Plazas Laborales Activas', 
             fontsize=13, pad=15, weight='bold', color='#1a252f')
ax.set_ylabel('Cantidad de Empleos Ocupados', fontsize=11, labelpad=10, color='#34495e')
ax.set_xlabel('Año de Observación', fontsize=11, labelpad=10, color='#34495e')

# Cuadrícula horizontal sutil
ax.grid(axis='y', linestyle=':', alpha=0.6, color='#95a5a6')

plt.tight_layout()

# Guardamos el gráfico final
plt.savefig('empleo_agricola_dashboard.png', dpi=300)
print("¡Gráfico de alto impacto guardado como 'empleo_agricola_dashboard.png'!")