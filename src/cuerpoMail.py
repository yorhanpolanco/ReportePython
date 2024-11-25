from conversiones import ConversionData
from generacionHtml import GenerarHtml
from graficas import GenerarGraficas
from functools import partial
from dotenv import load_dotenv
import os

ruta_logo = "pictures/dgii_logo.png"
load_dotenv("dev.env")

# Variables
equipo = os.getenv("EQUIPO")
lista_Epicas = os.getenv("LISTA_EPICAS")
datos_Epicas = os.getenv("DATOS_EPICAS")
impedimentos = os.getenv("IMPEDIMENTOS")
actividades = os.getenv("ACTIVIDADES")
acuerdos = os.getenv("ACUERDOS")
consideraciones = os.getenv("CONSIDERACIONES")
cantidad_Historias = os.getenv("CANTIDAD_HISTORIAS") # [Cant. en Desarrollo,Cant. Pendientes,Pruebas	Cant. Pruebas,Cant. Terminadas]
bloqueantes = os.getenv("BLOQUEANTES") # [abiertos, cerrados]
criticos = os.getenv("CRITICOS")
mayor = os.getenv("MAYOR")
normal = os.getenv("NORMAL")
menor = os.getenv("MENOR")
sin_Clasificar = os.getenv("SIN_CLASIFICAR")
actividades_fuera = os.getenv("ACTIVIDADES_FUERA")
nombre_remitente = os.getenv("NOMBRE_REMITENTE")
rol = os.getenv("ROL")

# Formatear texto de epicas
lista_Epicas= list(map(str,lista_Epicas.split(';')))
datos_Epicas= ConversionData.convertir_a_lista_de_listas(datos_Epicas)
impedimentos = ConversionData.convertir_a_lista_de_listas(impedimentos)
actividades = ConversionData.convertir_a_lista_de_listas(actividades)
acuerdos = ConversionData.convertir_a_lista_de_listas(acuerdos)
consideraciones = ConversionData.convertir_a_lista_de_listas(consideraciones)

# Formatear Historias y defectos
cantidad_Historias = ConversionData.convertir_a_lista_de_listas_enteros(cantidad_Historias)
bloqueantes = ConversionData.convertir_a_lista_de_listas_enteros(bloqueantes)
criticos = ConversionData.convertir_a_lista_de_listas_enteros(criticos)
mayor =ConversionData.convertir_a_lista_de_listas_enteros(mayor)
normal = ConversionData.convertir_a_lista_de_listas_enteros(normal)
menor =ConversionData.convertir_a_lista_de_listas_enteros(menor)
sin_Clasificar = ConversionData.convertir_a_lista_de_listas_enteros(sin_Clasificar)
actividades_fuera=list(map(str,actividades_fuera.split(';')))


crear_grafica_historias= partial(GenerarGraficas.crear_grafica_historias, cantidad_Historias)

# Generar html de las graficas de historia
grafica_historias_base64 = GenerarHtml.generar_html_graficas(lista_Epicas,crear_grafica_historias)

crear_grafica_defectos=partial(GenerarGraficas.crear_grafica_defectos,bloqueantes,criticos,mayor,normal,menor,sin_Clasificar)

# Generar html de grafica de defectos
grafica_defectos_base64 = GenerarHtml.generar_html_graficas(lista_Epicas,crear_grafica_defectos)

logo_base64 = ConversionData.imagen_base64(ruta_logo)

# Crear el cuerpo del correo en HTML
cuerpo_correo = f"""
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe de Estatus</title>
    <style>
        body {{
            font-family: Aptos;
            line-height: 1.6;
            margin: 20px;
            color: #333;
        }}
        h1, h2, h3 {{ color: #4cb749; }}
        h4 {{ color: black; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            color:black;
        }}
        td:first-child {{ width: 300px; }}
        .tabla {{ width: 75%; margin: 0; text-align: left; }}
        .status{{ background-color: yellow; font-weight: bold; }}
        th, td {{
            border: 1px solid #8dd873;
            padding: 8px;
            text-align: center;
        }}
        th {{ background-color: #4ea72e; }}
        .tabla tbody tr:nth-child(even) {{ background-color: #ffffff; }}
        .tabla tbody tr:nth-child(odd) {{ background-color: #d9f2d0; }}
        .contact-info {{ margin-top: 40px; }}
        p,li,ul {{ margin: 0; }}
        .equipo{{
            font-weight: bold;
        }}
    </style>
</head>

<body>

    <p>Buenas,</p>
    <br>
    <p>A continuación, presentamos el estatus por parte de QA del Proyecto / Épica / Incidentes del <span class="equipo">{equipo}</span>.</p>
    <h2>Objetivo</h2>
    <p>Presentar un informe periódico sobre los trabajos realizados por el equipo de QA de cara a los pendientes que están siendo trabajados por el  <span class="equipo">{equipo}</span>.</p>

    <h2>Situación Actual</h2>
    
    {GenerarHtml.generar_situacion_actual(lista_Epicas,datos_Epicas,impedimentos,actividades,acuerdos,consideraciones)}

    <div id="resumen">
        <h2>Resumen Historias</h2>
        <div class="tabla">
            {GenerarGraficas.generar_tabla_historias(lista_Epicas,cantidad_Historias).to_html(index=False)}
        </div>
        <h2>Gráfica de Historias</h2>
        {grafica_historias_base64}
        
        <h2>Resumen de Defectos</h2>
        <table class="tabla">
            <thead>
                <tr>
                    <th>Proyecto / Épica</th>
                    <th>Cantidad de Defectos</th>
                    <th>Defectos Abiertos</th>
                    <th>Defectos Cerrados</th>
                    <th>Severidad</th>
                </tr>
            </thead>
            <tbody>
                {GenerarHtml.defectos_html(GenerarGraficas.generar_tabla_defectos(lista_Epicas,bloqueantes,criticos,mayor,normal,menor,sin_Clasificar))}
            </tbody>
        </table>
        
        <h2>Gráfica de Defectos</h2>
        {grafica_defectos_base64}
    </div>

    <h3>Notas:</h3>
    <p>Actividades fuera de la célula:</p>
    <ul>{GenerarHtml.generar_lista_en_vinetas(actividades_fuera)}</ul>

    <div class="contact-info">
        <p>Saludos,</p>
        <p>{nombre_remitente}</p>
        <p>{rol}</p>
        <p>Sección Aseguramiento de la Calidad</p>

        <img src="data:image/png;base64,{logo_base64}" alt="Logo" style="width:150px;height:auto;" />
    </div>
</body>
</html>
"""

# Guardar el HTML en un archivo para verificar
with open('reports/informe_estatus.html', 'w', encoding='utf-8') as f:
    f.write(cuerpo_correo)
    
#os.environ['CUERPO_CORREO'] = cuerpo_correo

print("HTML generado correctamente.")
