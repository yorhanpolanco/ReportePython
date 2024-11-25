import base64
class ConversionData:
    
    # Convertir a lista de listas de string
    @staticmethod
    def convertir_a_lista_de_listas(texto:str)-> list[list[str]]:
        return [list(map(str.strip, item.split(','))) for item in texto.split(';')]

    # Convertir a lista de listas de enteros
    @staticmethod
    def convertir_a_lista_de_listas_enteros(texto:str)-> list[list[int]]:
        return [list(map(int, x.split(','))) for x in texto.split(';')]
    
    # Función para convertir la imagen a base64
    @staticmethod
    def imagen_base64(ruta_imagen):
        with open(ruta_imagen, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')