from tkinter import *
from tkinter import ttk, messagebox
import requests

class Aplicacion():
    __ventana = None
    __pesos = None
    __dolares = None

    def __init__(self):
        self.__ventana = Tk()
        self.__ventana.geometry('290x115')
        self.__ventana.title('Conversor de Moneda')
        mainframe = ttk.Frame(self.__ventana, padding='5 0 12 5')
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        self.__pesos = StringVar()
        self.__dolares = StringVar()
        self.__dolares.trace('w', self.calcular)
        self.dolaresEntry = ttk.Entry(mainframe, width=7, textvariable=self.__dolares)
        self.dolaresEntry.grid(column=2, row=1, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.__pesos).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(mainframe, text='Salir', command=self.__ventana.destroy).grid(column=3, row=3, sticky=W)
        ttk.Label(mainframe, text="dolares").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="es equivalente a").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="pesos").grid(column=3, row=2, sticky=W)
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.dolaresEntry.focus()
        self.__ventana.mainloop()

    def obtener_cotizacion_el_dolar(self):

        url = 'https://www.dolarsi.com/api/api.php?type=dolar'
        response = requests.get(url)
        data = response.json()
        cotizacion_dolar = None
        for casa in data:
            if 'casa' in casa and 'nombre' in casa['casa'] and casa['casa']['nombre'] == 'Oficial':
                cotizacion_dolar = casa['casa']['venta']
        if cotizacion_dolar:
            return cotizacion_dolar

    def calcular(self, *args):
        if self.dolaresEntry.get() != '':
            try:
                dolares = int(self.dolaresEntry.get())
                cotizacion_dolar = self.obtener_cotizacion_el_dolar()
                if cotizacion_dolar:
                    cotizacion_dolar = float(cotizacion_dolar.replace(',', '.'))
                    pesos = dolares * cotizacion_dolar
                    self.__pesos.set(pesos)
                else:
                    self.__pesos.set("Error: No se pudo obtener la cotización del dólar")

            except ValueError:
                messagebox.showerror(title='Error de tipo', message='Debe ingresar un valor numérico')
                self.__dolares.set('')
                self.__pesos.set('')
                self.dolaresEntry.focus()


def testapp():
    mi_app= Aplicacion()


if __name__ == '__main__':
    testapp()


