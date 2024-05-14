import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pydicom
import dicom2nifti
import os


def datoEntero(mns):
    while True:
        dato = input(mns)
        if dato.isnumeric() == True:
            return int(dato)
        else:
            print('DATO ERRONEO, POR FAVOR INTENTE DE NUEVO')
            continue

def cargar_imagenes_dicom():
    while True:
        # Solicitar al usuario la ruta de la carpeta
        carpeta = input("Por favor, introduce la ruta de la carpeta donde están los archivos DICOM: ")
        identificacion = datoEntero('COMO LA IMAGEN SE ENCUENTRA ANONIMIZADA, POR FAVOR INGRESE UN IDENTIFICADOR PARA LAS IMAGENES: ')

        # Verificar si la ruta es válida
        if not os.path.isdir(carpeta):
            print("La ruta especificada no es válida.")
            continue

        # Lista para almacenar las imágenes DICOM
        imagenes_dicom = []

        # Iterar sobre los archivos en la carpeta
        for root, dirs, files in os.walk(carpeta):
            for file in files:
                if file.endswith('.dcm'):
                    archivo_dicom_path = os.path.join(root, file)
                    try:
                        imagen_dicom = pydicom.dcmread(archivo_dicom_path) # lei el dicom
                        imagen = imagen_dicom.pixel_array # extraigo la imagen
                        nombre = str(imagen_dicom.PatientName) # obtengo el nombre del paciente
                        edad = imagen_dicom.PatientAge
                        tipo = imagen_dicom.Modality
                        imagenes_dicom.append(imagen) # añado la imagen a la lista

                        # Dicom_nifti(carpeta) # esta funcion cambia dicom a nifti

                    except Exception as e:
                        print(f"Error al leer el archivo DICOM {archivo_dicom_path}: {e}")

        return imagenes_dicom,nombre,edad,identificacion,tipo,carpeta
    

def Dicom_nifti(ruta):
    # Ruta de la carpeta que contiene los archivos DICOM
    carpeta_dicom = ruta

    # Ruta de la carpeta de destino para los archivos NIfTI
    carpeta_destino = input('NOMBRE DE LA CARPETA PARA GUARDAR LOS ARCHIVOS NIFTI: ')

    # Convertir la carpeta DICOM a archivos NIfTI en la carpeta de destino
    dicom2nifti.convert_directory(carpeta_dicom, carpeta_destino)

    print("¡Conversión completada!")


class PACIENTE():
    def __init__(self) -> None:
        self.__identificacion = 0
        self.__nombre = ''
        self.__edad = 0
        self.__imagenasociada = ''
        self.__imagenes = 0

    def AsignarNombre(self,n):
        self.__nombre = n
    def AsignarIdentificacion(self,i):
        self.__identificacion = i
    def AsignarEdad(self,a):
        self.__edad = a
    def AsignarTimg(self,t):
        self.__imagenasociada = t
    def AsignarImagenes(self,i):
        self.__imagenes = i

    def Vernombre(self):
        return self.__nombre
    def VerEdad(self):
        return self.__edad
    def VerIdentificacion(self):
        return self.__identificacion
    def VerImagenAsociada(self):
        return self.__imagenasociada
    def VerImagenes(self):
        return self.__imagenes
    
    def VerNumeroImg(self):
        return len(self.__imagenes)
    
    def VerImagen(self):
        while True:
            indice = datoEntero(f'hay {len(self.__imagenes)}, cual quieres ver, ingresa un numero dentro del rango mostrado: ')
            return self.__imagenes[indice]
        
    def verForma(self):
        return self.__imagenes[2].shape
    
    
    
    def recortarIMG(self):
        imagen = self.VerImagen()
        print(f'la imagen tiene la siguiente forma {self.verForma()}, por favor ingresa los siguientes datos: ')
        i = datoEntero('inicio:')
        f = datoEntero('final:')
        i2= datoEntero('inicio columna: ')
        f2 = datoEntero('final Columna: ')
        return imagen[i:f,i2:f2]
    
    def RotarImagen(self):
        imagen = self.VerImagen()
        while True:
            try:
                angle = int(input("¿En qué ángulo deseas rotar la imagen? (90, 180, 270): "))
                if angle in [90, 180, 270]:
                    break
                else:
                    print("Por favor, introduce un ángulo válido (90, 180, 270).")
            except ValueError:
                print("Por favor, introduce un número entero válido.")
        
        # Obtener las dimensiones de la imagen
        height, width = imagen.shape[:2]
        
        # Calcular el centro de la imagen
        center = (width / 2, height / 2)
        
        # Definir la matriz de rotación
        rotation_matrix = cv.getRotationMatrix2D(center, angle, 1.0)
        
        # Aplicar la rotación a la imagen
        rotated_img = cv.warpAffine(imagen, rotation_matrix, (width, height))
        return rotated_img
    
    def plotear(self,f):
        plt.figure(figsize=(10,6))
        plt.imshow(f, cmap='gray')
        plt.title(input('Nombre de la grafica: '))
        plt.axis('off')
        plt.show()
    
    def guardarImagen(self,c):
        n = input('nombre de la imagen para guardar en memoria: ')
        cv.imwrite(n +'.jpg',c)


class ImagenesJPG_PNG():
    def __init__(self) -> None:
        self.__img = ''
        self.__forma = 0

    def media(self):
        return np.mean(self.__img)
    
    def cargarImg(self):
        while True:
            imagen = cv.imread(input('ingrese la ruta del archivo: '))
            imagen = cv.cvtColor(imagen, cv.COLOR_BGR2RGB) 

            # Verifica si la imagen se ha cargado correctamente
            if imagen is None:
                print('No se pudo leer la imagen.\n')
                continue
            else:
                print('La imagen se ha cargado correctamente.')
                self.__img= imagen
                self.__forma = np.shape(imagen)
                break
    
    def obtnerImagen(self):
        return self.__img
            
    def verImg(self,c):
         return cv.imshow(input('nombre de la imagen: '),c), cv.waitKey(0), cv.destroyAllWindows()
    
    def verforma(self):
        print(f'filas: {self.__forma[0]}\nColumnas: {self.__forma[1]}\nCanales: {self.__forma[2]}')
        return self.__forma
    
    def Umbinary(self):
        Umb,imgB=cv.threshold(cv.cvtColor(self.__img,cv.COLOR_RGB2GRAY),self.media(),255,cv.THRESH_BINARY)
        return imgB
    
    def UmbinaryInv(self):
        Umb,imgB=cv.threshold(cv.cvtColor(self.__img,cv.COLOR_RGB2GRAY),self.media(),255,cv.THRESH_BINARY_INV)
        return imgB
    
    def UmTruncado(self):
        Umb,imgB=cv.threshold(cv.cvtColor(self.__img,cv.COLOR_RGB2GRAY),self.media(),255,cv.THRESH_TRUNC)
        return imgB
    
    def UmTozero(self):
        Umb,imgB=cv.threshold(cv.cvtColor(self.__img,cv.COLOR_RGB2GRAY),self.media(),255,cv.THRESH_TOZERO)
        return imgB
    
    def UmAdapTH_GAUSS(self):
        imgB = cv.adaptiveThreshold(cv.cvtColor(self.__img,cv.COLOR_RGB2GRAY),255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV,17,7)
        return imgB
    
    def erosion(self):
        print('INGRESE LOS DATOS PARA EL KERNEL')
        f = datoEntero('Filas: ')
        c = datoEntero('Columnas: ')
        kernel = np.ones((f,c), np.uint8)
        binaria = self.UmbinaryInv()
        imgErosionada = cv.erode(binaria,kernel, iterations=2)
        texto = f'''imagen Binarizada con Umbralizacion invertida\n kernel:{f}{c}'''
        imafinal= cv.putText(imgErosionada,texto,(40,90), cv.FONT_HERSHEY_SIMPLEX, 3, (255,255,0),2,cv.LINE_AA)
        n = input('nombre de la imagen a guardar: ')
        cv.imwrite(n +'.jpg',imafinal)

        return imafinal


def erosionimagen(x):
    print('INGRESE LOS DATOS PARA EL KERNEL')
    f = datoEntero('Filas: ')
    c = datoEntero('Columnas: ')
    kernel = np.ones((f,c), np.uint8)
    um,binaria=cv.threshold(x,0,255,cv.THRESH_BINARY_INV)
    imgErosionada = cv.erode(binaria,kernel, iterations=2)
    texto = f'''imagen Binarizada con Umbralizacion invertida\n kernel:{f}{c}'''
    imafinal= cv.putText(imgErosionada,texto,(40,90), cv.FONT_HERSHEY_SIMPLEX, 3, (255,255,0),2,cv.LINE_AA)
    n = input('nombre de la imagen a guardar: ')
    return cv.imwrite(n +'.jpg',imafinal)
    

    
    
    
    


        
    

    

        
        

    




# paciente = PACIENTE()

# p,n,a,i,m = cargar_imagenes_dicom()
# paciente.AsignarImagenes(p)
# paciente.AsignarNombre(n)
# paciente.AsignarEdad(a)
# paciente.AsignarIdentificacion(i)
# paciente.AsignarTimg(m)

# print(paciente.Vernombre())
# print(paciente.VerEdad())
# print(paciente.VerIdentificacion())
# print(paciente.VerImagenAsociada())
# plt.imshow(paciente.VerImagenes()[2])
# # plt.show()

# # paciente.VerImagen()
# # paciente.recortarIMG()
# paciente.plotear(paciente.RotarImagen())




