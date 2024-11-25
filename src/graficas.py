import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
class GenerarGraficas:
    from typing import List, Optional
    
    @staticmethod
    def generar_tabla_historias(lista_Epicas: list[str],cantidad_Historias:List[List[int]])-> pd.DataFrame:    
        # Llenar el DataFrame con los datos de cada épica
        historias_data = []
        for i, epica in enumerate(lista_Epicas):
            historias_data.append({
                'Proyecto / Epica': epica,
                'Cant. en Desarrollo': int(cantidad_Historias[i][0]),
                'Cant. Pendientes Pruebas': int(cantidad_Historias[i][1]),
                'Cant. Pruebas': int(cantidad_Historias[i][2]),
                'Cant. Terminadas': int(cantidad_Historias[i][3]),
                'Total': int(sum(cantidad_Historias[i]))  # Calcula el total para esta épica
            })

        df_historias = pd.DataFrame(historias_data)
        # Convertir columnas a enteros
        df_historias = df_historias.astype({
            'Cant. en Desarrollo': 'int',
            'Cant. Pendientes Pruebas': 'int',
            'Cant. Pruebas': 'int',
            'Cant. Terminadas': 'int',
            'Total': 'int'
        })
    
        return df_historias
    @staticmethod
    def generar_tabla_defectos(lista_Epicas: list[str],bloqueantes: List[List[int]],criticos: List[List[int]],mayor: List[List[int]],normal: List[List[int]],menor: List[List[int]],sin_Clasificar: List[List[int]])-> pd.DataFrame:
        # Crear tabla de defectos
        defectos_data = {
            'Proyecto / Épica': [],
            'Cantidad de Defectos': [],
            'Defectos Abiertos': [],
            'Defectos Cerrados': [],
            'Severidad': []
        }

        # Llenar defectos_data para cada épica
        severidades = ['Bloqueante', 'Crítico', 'Mayor', 'Normal', 'Menor', 'Sin Clasificar']
        for i, epica in enumerate(lista_Epicas):
            defectos_data['Proyecto / Épica'].extend([epica] * len(severidades))
            defectos_data['Cantidad de Defectos'].extend([sum(bloqueantes[i]), sum(criticos[i]), sum(mayor[i]), sum(normal[i]), sum(menor[i]), sum(sin_Clasificar[i])])
            defectos_data['Defectos Abiertos'].extend([bloqueantes[i][0], criticos[i][0], mayor[i][0], normal[i][0], menor[i][0], sin_Clasificar[i][0]])
            defectos_data['Defectos Cerrados'].extend([bloqueantes[i][1], criticos[i][1], mayor[i][1], normal[i][1], menor[i][1], sin_Clasificar[i][1]])
            defectos_data['Severidad'].extend(severidades)

        # Crear el DataFrame de defectos
        defectos_df = pd.DataFrame(defectos_data)
        return defectos_df
    
    # Generar gráficas de historias
    def crear_grafica_historias(cantidad_Historias,i: Optional[int]):
        plt.figure(figsize=(8, 5))
        categories = ['En Desarrollo', 'Pendientes', 'En Pruebas', 'Terminadas']
        values = cantidad_Historias[i]
        plt.bar(categories, values, color=['orange', 'yellow', 'blue', 'green'])
        plt.ylabel('Cantidad de Historias')
        plt.title('Resumen de Historias')

        plt.yticks(range(0, max(values) + 3))

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')
    
    
    def crear_grafica_defectos(bloqueantes: List[List[int]],criticos: List[List[int]],mayor: List[List[int]],normal: List[List[int]],menor: List[List[int]],sin_Clasificar: List[List[int]],i: Optional[int]):
        plt.figure(figsize=(10, 6))

        # Datos para la gráfica de defectos
        defectos_totales = [sum(bloqueantes[i]), sum(criticos[i]), sum(mayor[i]), sum(normal[i]), sum(menor[i]), sum(sin_Clasificar[i])]
        defectos_abiertos = [bloqueantes[i][0], criticos[i][0], mayor[i][0], normal[i][0], menor[i][0], sin_Clasificar[i][0]]
        defectos_cerrados = [bloqueantes[i][1], criticos[i][1], mayor[i][1], normal[i][1], menor[i][1], sin_Clasificar[i][1]]

        # Gráfico de barras apiladas
        bar_width = 0.4
        indices = range(len(defectos_totales))

        plt.bar(indices, defectos_abiertos, bar_width, label='Defectos Abiertos', color='orange')
        plt.bar(indices, defectos_cerrados, bar_width, bottom=defectos_abiertos, label='Defectos Cerrados', color='green')

        plt.xticks(indices, ['Bloqueante', 'Crítico', 'Mayor', 'Normal', 'Menor', 'Sin Clasificar'])
        plt.ylabel('Cantidad de Defectos')
        plt.title('Resumen de Defectos')

        max_value = max(defectos_totales)
        plt.yticks(range(0, max_value + 3)) 

        plt.legend()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')
    
    
