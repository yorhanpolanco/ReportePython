import pandas as pd
class GenerarHtml:
    from typing import List, Union, Optional
    
    # Formateador de Viñetas1
    @staticmethod
    def generar_lista_en_vinetas(lista_de_listas: Union[List[str], List[List[str]]], i: Optional[int] = None)->str:
        vinetas_html = ""

        if i is not None and i < len(lista_de_listas):
            lista_a_procesar = lista_de_listas[i]
        else:
            lista_a_procesar = lista_de_listas

        for item in lista_a_procesar:
            if isinstance(item, list):
                for sub_item in item:
                    if sub_item is None or sub_item.strip() == '':
                        vinetas_html += "<li>N/A</li>"
                        break
                    else:
                        vinetas_html += f"<li>{sub_item.capitalize()}</li>"
            else:
                if item is None or item.strip() == '':
                    vinetas_html += "<li>N/A</li>"
                else:
                    vinetas_html += f"<li>{item.capitalize()}</li>"
        return vinetas_html
    
    
    @staticmethod
    def generar_situacion_actual(lista_Epicas: list[str],datos_Epicas: list[list[str]],impedimentos: list[list[str]],actividades: list[list[str]],acuerdos: list[list[str]],consideraciones: list[list[str]]):
        situacion_actual_html = ""
        for i, epica in enumerate(lista_Epicas):
            datos = datos_Epicas[i]
            situacion_actual_html += f"""
            <div id="situacion">        
                <h3>{epica}</h3>
                <p><strong>Responsable(s) QA:</strong> {datos[0]}</p>
                <p><strong>Plataforma:</strong> {datos[1]}</p>
                <p><strong>Porcentaje de avance:</strong> <span class="status">{datos[2]}</span></p>
                <p><strong>Situación del proyecto:</strong> {datos[3]}</p>
                <p><strong>Impedimentos:</strong></p>
                    <ul>{GenerarHtml.generar_lista_en_vinetas(impedimentos,i)}</ul>
                <p><strong>Próximas actividades:</strong></p>
                    <ul>{GenerarHtml.generar_lista_en_vinetas(actividades,i)}</ul>
                <p><strong>Acuerdos:</strong></p>
                    <ul>{GenerarHtml.generar_lista_en_vinetas(acuerdos,i)}</ul>
                <p><strong>Consideraciones:</strong></p>
                    <ul>{GenerarHtml.generar_lista_en_vinetas(consideraciones,i)}</ul>
            </div>
            """
        return situacion_actual_html
    
    # Generar Html de tabla de defectos
    @staticmethod
    def defectos_html(defectos_df:pd.DataFrame)->str:
        rows = []
        for i, row in defectos_df.iterrows():
            if i == 0 or (row['Proyecto / Épica'] != defectos_df.iloc[i-1]['Proyecto / Épica']):
                # Si es la primera fila o si el nombre de la épica ha cambiado, combinar celdas
                rowspan = sum(defectos_df['Proyecto / Épica'] == row['Proyecto / Épica'])
                rows.append(f"""
                <tr>
                    <td rowspan="{rowspan}">{row['Proyecto / Épica']}</td>
                    <td>{row['Cantidad de Defectos']}</td>
                    <td>{row['Defectos Abiertos']}</td>
                    <td>{row['Defectos Cerrados']}</td>
                    <td>{row['Severidad']}</td>
                </tr>
                """)
            else:
                # Para las filas siguientes del mismo grupo, no mostrar la épica nuevamente
                rows.append(f"""
                <tr>
                    <td>{row['Cantidad de Defectos']}</td>
                    <td>{row['Defectos Abiertos']}</td>
                    <td>{row['Defectos Cerrados']}</td>
                    <td>{row['Severidad']}</td>
                </tr>
                """)

        return ''.join(rows)
    
    @staticmethod
    def generar_html_graficas( lista_Epicas,crear_grafica):
        html_graficas_base64 = ""
        for i, epica in enumerate(lista_Epicas):
            html_graficas_base64 += f"""
            <h3>{epica}</h3>
            <img src="data:image/png;base64,{crear_grafica(i)}" />
            """
        return html_graficas_base64