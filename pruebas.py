from first import *

pacientes = {}
pictures = {}
while True:
    menu = input('BIENVENIDO AL SISTEMA\nPOR FAVOR SELECCIONE UNA OPCION\n 1.INGRESAR PACIENTE\n 2.CARGAR UNA IMAGEN JPG, PNG\n 3.JUGAR CON LAS IMAGENES\n 4.SALIR ')
    if menu == '1':
        paciente = PACIENTE()
        p,n,a,i,m,c = cargar_imagenes_dicom()
        paciente.AsignarImagenes(p)
        paciente.AsignarNombre(n)
        paciente.AsignarEdad(a)
        paciente.AsignarIdentificacion(i)
        paciente.AsignarTimg(m)

        pacientes[paciente.VerIdentificacion()] = paciente
        pictures[paciente.VerIdentificacion()] = paciente.VerImagenes()

        # convertir a nifti y guardar en nueva carpeta

        Dicom_nifti(c) # c es la ruta de los archivos dicom 

        while True:
            menu_2 = input('¿DESEAS HACER UNA ROTACION GEOMETRICA?\n1.SI\n2.NO ')
            if menu_2 == '1':
                imgR = paciente.RotarImagen()
                paciente.plotear(imgR)
                paciente.guardarImagen(imgR)
                break
            elif menu_2 == '2':
                break
            else:
                continue
    elif menu == '2':
        imagenjpgpng = ImagenesJPG_PNG()
        imagenjpgpng.cargarImg()
        cedula = datoEntero('INGRESE UN NUMERO PARA IDENTIFICAR LA IMAGEN: ')
        pictures[cedula] = imagenjpgpng

        print('LA BINARIZACION SE REALIZARA A CONTINUACION\n')
        imagenMODIFICADA = imagenjpgpng.erosion()
        plt.figure(figsize=(14,5))
        plt.subplot(1,2,1)
        plt.imshow(imagenjpgpng.obtnerImagen())
        plt.title('IMAGEN ORIGINAL')
        plt.axis('off')
        plt.subplot(1,2,2)
        plt.imshow(imagenMODIFICADA, cmap ='gray')
        plt.title('IMAGEN MODIFICADA')
        plt.axis('off')
        plt.show()
    
    elif menu == '3':
        cc = datoEntero('INGRESE EL NUMERO CON EL QUE ESTA IDENTIFICADA LA IMAGEN: ')
        c = pictures.get(cc)
        if type(c) == list:
            n = datoEntero(f'Hay {len(c)} imagenes, cual desea visualizar: ')
            c = c[n]
            print('LA BINARIZACION SE REALIZARA A CONTINUACION\n')
            imagenMODIFICADA = erosionimagen(c)
            plt.figure(figsize=(14,5))
            plt.subplot(1,2,1)
            plt.imshow(c ,cmap='gray')
            plt.title('IMAGEN ORIGINAL')
            plt.axis('off')
            plt.subplot(1,2,2)
            plt.imshow(imagenMODIFICADA, cmap='gray')
            plt.title('IMAGEN MODIFICADA')
            plt.axis('off')
            plt.show()

        else:
            pass

        print('LA BINARIZACION SE REALIZARA A CONTINUACION\n')
        imagenMODIFICADA = c.erosion()
        plt.figure(figsize=(14,5))
        plt.subplot(1,2,1)
        plt.imshow(c.obtnerImagen())
        plt.title('IMAGEN ORIGINAL')
        plt.axis('off')
        plt.subplot(1,2,2)
        plt.imshow(imagenMODIFICADA, cmap='gray')
        plt.title('IMAGEN MODIFICADA')
        plt.axis('off')
        plt.show()
    
    elif menu == '4':
        break

    else:
        continue

        







