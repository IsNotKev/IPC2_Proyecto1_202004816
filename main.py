from tkinter.filedialog import askopenfilename
import xml.etree.ElementTree as ET
from Lista import Lista

class Posicion(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Celda(Posicion):
    def __init__(self, x, y,combustible):
        super().__init__(x, y)
        self.combustible = combustible

class Terreno(object):
    def __init__(self,nombre,filas,columnas,celdas,inicio,fin):
        self.nombre = nombre
        self.filas = filas
        self.columnas = columnas
        self.celdas = celdas
        self.inicio = inicio
        self.fin = fin
     

if __name__ == "__main__":
    opcion = ''
    terrenos = Lista()
    tprocesado = None
    while True:
        print('')
        print('--------- Menú Principal ---------')
        print('|1. Cargar Archivo               |')
        print('|2. Procesar Archivo             |')
        print('|3. Escribir Archivo de Salida   |')
        print('|4. Mostrar Datos del Estudiante |')
        print('|5. Generar Gráfica              |')
        print('|6. Salir                        |')
        print('----------------------------------')
        print('')

        opcion = input('Elija una opción\n\n')

        if opcion == '1':
            terrenos = Lista()
            tprocesado = None
            print('\n---------------- Cargar Archivo ----------------')
            print('Elija el Archivo Con Extension XML Que Desee Cargar.')

            filename = askopenfilename()

            extension = filename.split('.')

            if extension[len(extension)-1] != 'xml' and extension[len(extension)-1] != 'XML':
                input('\nArchivo Con Extensión Incorrecta. Presione Enter Para Continuar.')
                continue


            doc = ET.parse(filename)

            root = doc.getroot()

            terrenosLeidos = root.findall('terreno')

            for i in terrenosLeidos:
                #NOMBRE
                nombre = i.attrib.get('nombre')
                #DIMENSIONES
                dimension = i.findall('dimension')
                f = int((dimension[0].findall('m'))[0].text)
                c = int((dimension[0].findall('n'))[0].text)
                #POSICION INICIAL
                posinicio = i.findall('posicioninicio')
                x = int((posinicio[0].findall('x'))[0].text)
                y = int((posinicio[0].findall('y'))[0].text)
                posicioninicial = Posicion(x,y)
                #POSICION FINAL
                posfin = i.findall('posicionfin')
                x2 = int((posfin[0].findall('x'))[0].text)
                y2 = int((posfin[0].findall('y'))[0].text)
                posicionfinal = Posicion(x2,y2)
                
                #MATRIZ
                posiciones = i.findall('posicion')
                celdas = Lista()
                for j in range(1,f+1):
                    nuevaFila = Lista()
                    for k in range(1,c+1):
                        for pos in posiciones:
                            x3 = int(pos.attrib.get('x'))
                            y3 = int(pos.attrib.get('y'))
                            if x3 == j and y3 == k:                                
                                gas = int(pos.text)                               
                                nuevaCelda = Celda(x3,y3,gas)
                                nuevaFila.agregar(nuevaCelda)
                    celdas.agregar(nuevaFila)
                    
                #celdas.graficarMatriz()        
                #celdas.imprimirMatriz()
                nuevoTerreno = Terreno(nombre,f,c,celdas,posicioninicial,posicionfinal)
                #print('\nNombre: ' + nuevoTerreno.nombre + '\nFilas: ' + str(nuevoTerreno.filas)+ '\nColumnas: ' + str(nuevoTerreno.columnas) + '\nInicio: ' + str(nuevoTerreno.inicio.x) +','+ str(nuevoTerreno.inicio.y)+ '\nFin: ' + str(nuevoTerreno.fin.x) +','+ str(nuevoTerreno.fin.y) + '\nCeldas: ')
                #nuevoTerreno.celdas.imprimirMatriz()
                terrenos.agregar(nuevoTerreno)
            print('\nSe leyeron ' + str(terrenos.tamano()) + ' terrenos')
            input('\nArchivo Cargado Correctamente. Presione Enter Para Continuar.')
        elif opcion == '2':
            tprocesado = None
            if terrenos.tamano() == 0:
                input('\nCargue Un Archivo Con Terrenos Para Procesar. Presione Enter Para Continuar.')
            else:
                n = input('\nIngrese El Nombre Del Terreno Que Desee Procesar\n')
                terrenos.procesar(n)
                tprocesado = terrenos.encontrarTerreno(n)
        elif opcion == '3':
            # create the file structure

            if tprocesado == None:
                input('\nNingún terreno Procesado. Presione Enter Para Continuar.')
            else:
                camino = tprocesado.celdas.devolverCamino(tprocesado.inicio,tprocesado.fin)
                data = ET.Element('terreno')
                data.set('nombre',tprocesado.nombre)
                i = ET.SubElement(data, 'posicioninicio')
                f = ET.SubElement(data, 'posicionfin')
                x1 = ET.SubElement(i,'x')
                x1.text = str(tprocesado.inicio.x)
                y1 = ET.SubElement(i,'y')
                y1.text = str(tprocesado.inicio.y)
                x2 = ET.SubElement(f,'x')
                x2.text = str(tprocesado.fin.x)
                y2 = ET.SubElement(f,'y')
                y2.text = str(tprocesado.fin.y)
                com = ET.SubElement(data,'combustible')

                actual = camino.cabeza
                gas = 0
                while actual != None:
                    gas += actual.obtenerDato().combustible
                    actual = actual.obtenerSiguiente()

                com.text = str(gas)

                actual = camino.cabeza
                while actual != None:
                    pp = ET.SubElement(data,'posicion')
                    pp.set('x',str(actual.obtenerDato().x))
                    pp.set('y',str(actual.obtenerDato().y))
                    pp.text = str(actual.obtenerDato().combustible)
                    actual = actual.obtenerSiguiente()
               
                # create a new XML file with the results
                mydata = ET.tostring(data)
                myfile = open("ruta.xml", "wb")
                myfile.write(mydata)
                myfile.close()

                input('\n Archivo de Salida Generado Exitosamente. Presione Enter Para Continuar.')
           
        elif opcion == '4':
            print('\n--------------------- Datos ---------------------')
            print('\n> Kevin Steve Martinez Lemus ')
            print('> 202004816')
            print('> Introducción a la Programación y Computación 2 Sección "C"')
            print('> Ingenieria en Ciencias y Sistemas')
            print('> 4to Semestre')

            input('\nPresione Enter Para Continuar.')
        elif opcion == '5':
            if terrenos.tamano() == 0:
                input('\nCargue Un Archivo Con Terrenos Para Graficar. Presione Enter Para Continuar.')
            else:
                print('----------- Generar Gráfica -----------\n')
                terrenos.imprimirOpciones()
                print('\n Elija el terreno que desee graficar.\n')
                opcion2 = input()

                if opcion2.isdigit():
                    terrenos.graficarTerreno(int(opcion2))
                else:
                    input('\nElija una Opción Correcta. Presione Enter Para Continuar.')          
        elif opcion == '6':
            print('\nAdiós!\n')
            break
        else:
            input('\nElija Una Opción Válida. Presione Enter Para Continuar.')
        
