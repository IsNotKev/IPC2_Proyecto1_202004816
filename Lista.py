from tkinter import Label
from tkinter.constants import ACTIVE, TRUE
from Nodo import Nodo
from graphviz import Digraph,Graph

class Lista:
    def __init__(self):
        self.cabeza = None

    def apilar(self,item):
        temp = Nodo(item)
        temp.asignarSiguiente(self.cabeza)
        self.cabeza = temp

    def agregar(self, item):
        if not self.cabeza:
            self.cabeza = Nodo(item)
            return
        curr = self.cabeza
        while curr.siguiente:
            curr = curr.siguiente
        curr.siguiente=Nodo(item)
        

    def tamano(self):
        actual = self.cabeza
        contador = 0
        if actual != None:
            while actual != None:
                contador = contador + 1
                actual = actual.obtenerSiguiente()

        return contador

    def remover(self,item):
        actual = self.cabeza
        previo = None
        encontrado = False
        while not encontrado:
            if actual.obtenerDato() == item:
                encontrado = True
            else:
                previo = actual
                actual = actual.obtenerSiguiente()

        if previo == None:
            self.cabeza = actual.obtenerSiguiente()
        else:
            previo.asignarSiguiente(actual.obtenerSiguiente())

    def imprimirCelda(self):
        actual = self.cabeza
        t = ''
        while actual != None:
            t += '|'
            t += str(actual.obtenerDato().combustible)
            t += '|'
            actual = actual.obtenerSiguiente()
        print(t)

    def imprimirMatriz(self): 
        actual = self.cabeza
        while actual != None:
            actual.obtenerDato().imprimirCelda()
            actual = actual.obtenerSiguiente()


    def imprimirLista(self): 
        actual = self.cabeza
        while actual != None:
            print(actual.obtenerDato())
            actual = actual.obtenerSiguiente()

    def graficarMatriz(self,nombre):
        dot = Graph(comment='Grafica de la pila...!!')
        dot.attr(rankdir='LR')
        
        actual = self.cabeza
        contador = 0
        while actual != None:
            aux = actual.obtenerDato().cabeza
            contador2 = 0
            while aux != None:
                contador += 1
                contador2 += 1
                dot.node(str(contador), str(aux.obtenerDato().combustible))
                aux = aux.obtenerSiguiente()    
                if(contador2 >1):
                    dot.edge(str(contador-1), str(contador))
                    
                if contador > (actual.obtenerDato().tamano()):
                    a = contador-(actual.obtenerDato().tamano())
                    dot.edge(str(contador), str(a), constraint = 'false')
            actual = actual.obtenerSiguiente()
            dot.node('titulo',nombre + ' :',shape="plaintext",align="center")              
        dot.render(nombre, format="pdf", view=True) 
    
    def graficarTerreno(self,no):
        actual = self.cabeza
        c = 1
        while actual != None:
            if c == no:
                actual.obtenerDato().celdas.graficarMatriz(actual.obtenerDato().nombre)
                input('\nGráfica Generada Exitosamente. Presione Enter Para Continuar.')
                return
            c += 1
            actual = actual.obtenerSiguiente()
        input('\nElija una Opción Correcta. Presione Enter Para Continuar.') 

    def imprimirOpciones(self):
        actual = self.cabeza
        c=1
        while actual != None:
            print(str(c)+'. '+actual.obtenerDato().nombre)
            c += 1
            actual = actual.obtenerSiguiente()

    def procesar(self, name):
        actual = self.cabeza
        print('\n> Buscando Terreno.')
        while actual != None:
            if (actual.obtenerDato()).nombre == name:
                print('> Terreno Encontrado.')
                i = actual.obtenerDato().inicio
                f = actual.obtenerDato().fin
                actual.obtenerDato().celdas.procesarCamino(i,f)
                return
            actual = actual.obtenerSiguiente()
        print('> Terreno No Encontrado.')
        return

    def encontrarTerreno(self,name):
        actual = self.cabeza
        while actual != None:
            if (actual.obtenerDato()).nombre == name:
                return actual.obtenerDato()
            actual = actual.obtenerSiguiente()
        return None

    def procesarCamino(self,inicio,fin):
        print('> Procesando Datos.')
        print('Inicio: ' + str(inicio.x )+ ',' + str(inicio.y))
        print('Fin: ' + str(fin.x )+ ',' + str(fin.y))
        actual = self.cabeza   
        filas = self.tamano()
        columnas = actual.obtenerDato().tamano()
        print('Cantidad de Nodos : ' + str(filas * columnas))

        camino = Lista()
        termino = False      

        if inicio.x < fin.x:
            movx = 1
        elif inicio.x > fin.x:
            movx = -1
        else:
            movx = 0

        if inicio.y < fin.y:
            movy = 1
        elif inicio.y > fin.y:
            movy = -1
        else:
            movy = 0

        i = inicio.x
        j = inicio.y

        ncelda = self.buscarCelda(i,j)
        camino.agregar(ncelda)

        print('> Encontrando Mejor Ruta.')

        while not termino:

            if i == fin.x and j == fin.y:
                termino = True
            elif i == fin.x:
                celda1 = self.buscarCelda(i,j+movy)
                j += movy
                camino.agregar(celda1)
            elif j == fin.y:
                celda1 = self.buscarCelda(i+movx,j)
                i += movx
                camino.agregar(celda1)
            else:
                celda1 = self.buscarCelda(i+movx,j)
                celda2 = self.buscarCelda(i,j+movy)
                if celda1.combustible < celda2.combustible:
                    camino.agregar(celda1)
                    i += movx
                else:
                    camino.agregar(celda2)
                    j +=movy
        
        print('> Ruta Encontrada:\n')
        camino.imprimirCamino(filas,columnas)

                
    def imprimirCamino(self,filas,columnas):
        gas = 0
        for i in range(1,filas+1):
            t = ''
            for j in range(1,columnas+1):
                encontrado = False
                actual = self.cabeza
                while actual != None:
                    aux = actual.obtenerDato()
                    if aux.x == i and aux.y == j:
                        t += '|'
                        t += str(aux.combustible)
                        t += '|'
                        gas += aux.combustible
                        encontrado = True
                    actual = actual.obtenerSiguiente()
                if not encontrado:
                    t += '|0|'
            print(t)

        print('\n> Combustible Consumido: ' + str(gas))
        input('> Proceso Terminado. Presione Enter Para Continuar.')

    def buscarCelda(self,x,y):
        actual  = self.cabeza
        contador = 0
        while actual != None:  
            contador += 1         
            contador2 = 0
            aux = (actual.obtenerDato()).cabeza            
            while aux != None:                
                contador2 += 1
                if contador == x and contador2 == y:
                    return aux.obtenerDato()               
                aux = aux.obtenerSiguiente()        
            actual = actual.obtenerSiguiente()
        return
            
    def devolverCamino(self,inicio,fin):
        camino = Lista()
        termino = False      

        if inicio.x < fin.x:
            movx = 1
        elif inicio.x > fin.x:
            movx = -1
        else:
            movx = 0

        if inicio.y < fin.y:
            movy = 1
        elif inicio.y > fin.y:
            movy = -1
        else:
            movy = 0

        i = inicio.x
        j = inicio.y

        ncelda = self.buscarCelda(i,j)
        camino.agregar(ncelda)

        while not termino:

            if i == fin.x and j == fin.y:
                termino = True
            elif i == fin.x:
                celda1 = self.buscarCelda(i,j+movy)
                j += movy
                camino.agregar(celda1)
            elif j == fin.y:
                celda1 = self.buscarCelda(i+movx,j)
                i += movx
                camino.agregar(celda1)
            else:
                celda1 = self.buscarCelda(i+movx,j)
                celda2 = self.buscarCelda(i,j+movy)
                if celda1.combustible < celda2.combustible:
                    camino.agregar(celda1)
                    i += movx
                else:
                    camino.agregar(celda2)
                    j +=movy
        return camino


        
        
    
    
            
