import os
import var
from datetime import datetime

from PyQt5 import QtSql
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import conexion


class Printer:
    @staticmethod
    def cabecera():
        """

        Módulo que carga la cabecera de todos los informes de la empresa

        :return: None
        :rtype: None

        """
        try:
            logo = ".\\img\logo.jpg"
            var.rep.setTitle('INFORMES')
            var.rep.setAuthor('Administracion Teis')
            var.rep.setFont('Helvetica', size=10)
            var.rep.line(45, 820, 525, 820)
            var.rep.line(45, 750, 525, 750)
            textcif = 'CIF: A0000000N'
            textnom = 'IMPORTACIONES Y EXPORTACIONES TEIS S.L'
            textdir = 'Avda. Galicia, 101 - Vigo C.P.: 36216'
            texttel = 'Telefono: 886 12 04 64'
            var.rep.drawString(50, 805, textcif)
            var.rep.drawString(50, 790, textnom)
            var.rep.drawString(50, 775, textdir)
            var.rep.drawString(50, 760, texttel)
            var.rep.drawImage(logo, 450, 752)
        except Exception as error:
            print('error en el cabecera de informe: %s' % str(error))

    @staticmethod
    def pie(textlistado):
        """

        Módulo que carga el pie. Igual para todos excepto el nombre del informe, que se pasa por
        la variable textlistado.

        :param textlistado: según el contenido del informe
        :type textlistado: string
        :return: None
        :rtype: None

        """
        try:
            var.rep.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d.%m.%Y %H.%M.%S')
            var.rep.setFont('Helvetica-Oblique', size=6)
            var.rep.drawString(460, 40, str(fecha))
            var.rep.drawString(270, 40, str('Página %s' % var.rep.getPageNumber()))
            var.rep.drawString(50, 40, str(textlistado))
        except Exception as error:
            print('error en el pie de informe: %s' % str(error))

    @staticmethod
    def cabeceraCli():
        """

        Módulo que carga la cabecera de página del informe del cliente

        :return: None
        :rtype: None

        """
        try:
            var.rep.setFont('Helvetica-Bold', size=9)
            textlistado = 'LISTADO DE CLIENTES'
            var.rep.drawString(255, 735, textlistado)
            var.rep.line(45, 730, 525, 730)
            itemcli = ['Cod', 'DNI', 'APELLIDOS', 'NOMBRE', 'FECHA ALTA']
            var.rep.drawString(45, 710, itemcli[0])
            var.rep.drawString(90, 710, itemcli[1])
            var.rep.drawString(180, 710, itemcli[2])
            var.rep.drawString(325, 710, itemcli[3])
            var.rep.drawString(465, 710, itemcli[4])
            var.rep.line(45, 703, 525, 703)
        except Exception as error:
            print('error en el cabecera cli de informe: %s' % str(error))

    @staticmethod
    def cabeceraPro():
        """

        Módulo que carga la cabecera de página del informe de productos

        :return: None
        :rtype: None

        """
        try:
            var.rep.setFont('Helvetica-Bold', size=9)
            textlistado = 'LISTADO DE PRODUCTOS'
            var.rep.drawString(255, 735, textlistado)
            var.rep.line(45, 730, 525, 730)
            itempro = ['Cod', 'ARTÍCULO', 'PRECIO', 'STOCK']
            var.rep.drawString(45, 710, itempro[0])
            var.rep.drawString(170, 710, itempro[1])
            var.rep.drawString(360, 710, itempro[2])
            var.rep.drawString(490, 710, itempro[3])
            var.rep.line(45, 703, 525, 703)
        except Exception as error:
            print('error en el cabecera pro de informe: %s' % str(error))

    @staticmethod
    def cabeceraFac(cod):
        """

        Módulo que carga la cabecera de página del informe de facturación

        :param cod: codigo de la factura
        :type cod: entero
        :return: None
        :rtype: None

        Toma datos de dos tablas: las del cliente, al que está asociado el código de la factura; y de la tabla factura,
        de la que toma los datos de dni y fecha.

        """
        try:
            dni = ''
            var.rep.setFont('Helvetica-Bold', size=11)
            var.rep.drawString(55, 725, 'Cliente: ')
            var.rep.setFont('Helvetica', size=10)
            var.rep.drawString(50, 650, 'Factura nº: %s' % str(cod))
            var.rep.line(45, 665, 525, 665)
            var.rep.line(45, 640, 525, 640)
            query = QtSql.QSqlQuery()
            query.prepare('select dniCliente, fechaFactura from facturas where numFactura = :cod')
            query.bindValue(':cod', int(cod))
            print(cod)
            if query.exec_():
                while query.next():
                    dni = str(query.value(0))
                    print(dni)
                    var.rep.drawString(55, 710, 'DNI: %s' % str(query.value(0)))
                    var.rep.drawString(420, 650, 'Fecha: %s' % str(query.value(1)))
            else:
                print("Error cabecera fac dni: ", query.lastError().text())
            query1 = QtSql.QSqlQuery()
            query1.prepare('select apellidos, nombre, direccion, provincia, formasPago from clientes where dni = :dni')
            query1.bindValue(':dni', str(dni))
            if query1.exec_():
                while query1.next():
                    var.rep.drawString(55, 695, str(query1.value(0)) + ', ' + str(query1.value(1)))
                    var.rep.drawString(300, 695, 'Formas de Pago: ')
                    var.rep.drawString(55, 680, str(query1.value(2)) + ' - ' + str(query1.value(3)))
                    var.rep.drawString(300, 680, str(query1.value(4).strip('[]').replace('\'', '').replace(',', ' -')))
                    # \ caracter escape indica que lo siguiente tiene un significado especial
            else:
                print("Error cabecera fac info ", query.lastError().text())
            var.rep.line(45, 615, 525, 615)
            var.rep.setFont('Helvetica-Bold', size=10)
            temven = ['CodVenta', 'Artículo', 'Cantidad', 'Precio-Unidad(€)', 'Subtotal(€)']
            var.rep.drawString(50, 625, temven[0])
            var.rep.drawString(140, 625, temven[1])
            var.rep.drawString(265, 625, temven[2])
            var.rep.drawString(360, 625, temven[3])
            var.rep.drawString(470, 625, temven[4])
            var.rep.setFont('Helvetica-Bold', size=12)
            var.rep.drawRightString(500, 160,
                                    'Subtotal:   ' + "{0:.2f}".format(float(var.ui.lblSubtotal.text())) + ' €')
            var.rep.drawRightString(500, 140, 'IVA:     ' + "{0:.2f}".format(float(var.ui.lblIva.text())) + ' €')
            var.rep.drawRightString(500, 115,
                                    'Total Factura: ' + "{0:.2f}".format(float(var.ui.lblTotal.text())) + ' €')

        except Exception as error:
            print('Error cabecera factura informe %s' % str(error))

    @staticmethod
    def cabeceraCliente(dni):
        """

        Módulo que carga la cabecera de página del informe de facturas de un cliente

        :param dni: dni del cliente
        :type dni: string
        :return: None
        :rtype: None

        Toma datos de la tabla cliente

        """
        try:
            var.rep.setFont('Helvetica-Bold', size=11)
            var.rep.drawString(55, 725, 'Cliente: ')
            var.rep.setFont('Helvetica', size=10)
            var.rep.line(45, 665, 525, 665)
            var.rep.line(45, 640, 525, 640)
            query1 = QtSql.QSqlQuery()
            query1.prepare('select apellidos, nombre, direccion, provincia, formasPago from clientes where dni = :dni')
            query1.bindValue(':dni', str(dni))
            if query1.exec_():
                while query1.next():
                    var.rep.drawString(55, 710, 'DNI: %s' % str(dni))
                    var.rep.drawString(55, 695, str(query1.value(0)) + ', ' + str(query1.value(1)))
                    var.rep.drawString(300, 695, 'Formas de Pago: ')
                    var.rep.drawString(55, 680, str(query1.value(2)) + ' - ' + str(query1.value(3)))
                    var.rep.drawString(300, 680, str(query1.value(4).strip('[]').replace('\'', '').replace(',', ' -')))
                    # \ caracter escape indica que lo siguiente tiene un significado especial
            else:
                print("Error cabecera fac info ", query1.lastError().text())
            var.rep.setFont('Helvetica-Bold', size=10)
            temven = ['NºFac', 'Fecha factura', 'Valor neto(€)', 'Valor IVA', 'Valor total(€)']
            var.rep.drawString(50, 650, temven[0])
            var.rep.drawString(130, 650, temven[1])
            var.rep.drawString(250, 650, temven[2])
            var.rep.drawString(365, 650, temven[3])
            var.rep.drawString(465, 650, temven[4])

        except Exception as error:
            print('Error cabecera factura informe %s' % str(error))

    @staticmethod
    def pieFacturasCli(subtotal, iva, total):
        """

        Módulo que imprime el pie de página del informe de facturas de un cliente

        :param subtotal: subtotal de la factura
        :type subtotal: float
        :param iva: total del IVA de las facturas
        :type iva: float
        :param total: total de las facturas
        :type total: float
        :return: None
        :rtype: None

        """
        var.rep.setFont('Helvetica-Bold', size=12)
        var.rep.drawRightString(500, 110, 'Subtotal:       ' + str("{0:.2f}".format(float(subtotal)) + ' €'))
        var.rep.drawRightString(500, 90, 'IVA:            ' + str("{0:.2f}".format(float(iva)) + ' €'))
        var.rep.drawRightString(500, 70, 'Total Facturas: ' + str("{0:.2f}".format(float(total)) + ' €'))

    @staticmethod
    def reportCli():
        """

        Módulo que llama a la base de datos, captura datos de los clientes ordenados alfabéticamente y los va mostrando
        en el informe

        :return: None
        :rtype: None

        La variable i representa los valores del eje X
        La variable j representa los valores del eje Y
        Los informes se guardan en la carpeta informe y al mismo tiempo se muestran con el lector PDF que exista
        por defecto en el sistema

        """
        try:
            textlistado = 'LISTADO DE CLIENTES'
            var.rep = canvas.Canvas('informes/listadoClientes.pdf')
            Printer.cabecera()
            Printer.cabeceraCli()
            Printer.pie(textlistado)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, dni, apellidos, nombre, fechaAlta from clientes order by apellidos, nombre')
            var.rep.setFont('Helvetica', size=10)
            if query.exec_():
                i = 50
                j = 690
                while query.next():
                    if j <= 80:
                        var.rep.drawString(440, 70, 'Página siguiente...')
                        var.rep.showPage()
                        Printer.cabecera()
                        Printer.pie(textlistado)
                        Printer.cabeceraCli()
                        i = 50
                        j = 690
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawString(i + 30, j, str(query.value(1)))
                    var.rep.drawString(i + 130, j, str(query.value(2)))
                    var.rep.drawString(i + 280, j, str(query.value(3)))
                    var.rep.drawRightString(i + 470, j, str(query.value(4)))
                    j = j - 25

            var.rep.save()
            roothPath = ".\\informes"
            cont = 0
            for file in os.listdir(roothPath):
                if file.endswith('listadoClientes.pdf'):
                    os.startfile("%s/%s" % (roothPath, file))
                cont = cont + 1

        except Exception as error:
            print('Error reportcli %s' % str(error))

    @staticmethod
    def reportPro():
        """

        Módulo que llama a la base de datos, captura datos de los productos ordenados alfabéticamente y los va mostrando
        en el informe

        :return: None
        :rtype: None

        La variable i representa los valores del eje X
        La variable j representa los valores del eje Y
        Los informes se guardan en la carpeta informe y al mismo tiempo se muestran con el lector PDF que exista
        por defecto en el sistema

        """
        try:
            textlistado = 'LISTADO DE PRODUCTOS'
            var.rep = canvas.Canvas('informes/listadoProductos.pdf')
            Printer.cabecera()
            Printer.cabeceraPro()
            Printer.pie(textlistado)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre, precio, stock from articulos order by nombre')
            var.rep.setFont('Helvetica', size=10)
            if query.exec_():
                i = 50
                j = 690
                while query.next():
                    if j <= 80:
                        var.rep.drawString(440, 70, 'Página siguiente...')
                        var.rep.showPage()
                        Printer.cabecera()
                        Printer.pie(textlistado)
                        Printer.cabeceraPro()
                        i = 50
                        j = 690
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawString(i + 100, j, str(query.value(1)))
                    var.rep.drawRightString(i + 335, j, str(query.value(2)))
                    var.rep.drawRightString(i + 470, j, str(query.value(3)))
                    j = j - 25

            var.rep.save()
            roothPath = ".\\informes"
            cont = 0
            for file in os.listdir(roothPath):
                if file.endswith('listadoProductos.pdf'):
                    os.startfile("%s/%s" % (roothPath, file))
                cont = cont + 1

        except Exception as error:
            print('Error reportpro %s' % str(error))

    @staticmethod
    def reportFac():
        """

        Módulo que carga el cuerpo del informe de la factura

        :return: None
        :rtype: None

        Selecciona todas las ventas de esa factura y las va anotando linea a linea.
        La variable i representa los valores del eje X
        La variable j representa los valores del eje Y
        Además tiene un pie de informe para mostrar los subtotales IVA y total
        Los informes se guardan en la carpeta informe y al mismo tiempo se muestran con el lector PDF que exista
        por defecto en el sistema

        """
        try:
            textlistado = 'FACTURA'
            var.rep = canvas.Canvas('informes/factura.pdf', pagesize=A4)
            Printer.cabecera()
            Printer.pie(textlistado)
            codfac = var.ui.lblCodFac.text()
            Printer.cabeceraFac(codfac)
            query = QtSql.QSqlQuery()
            query.prepare('select codVenta, codArtVenta, cantidad, precio from ventas where codFacVenta = :codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                i = 55
                j = 600
                while query.next():
                    if j <= 100:
                        var.rep.drawString(440, 110, 'Página siguiente...')
                        var.rep.showPage()
                        Printer.cabecera()
                        Printer.pie(textlistado)
                        Printer.cabeceraFac()
                        i = 50
                        j = 600
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    codArt = query.value(1)
                    nombreArticulo = conexion.Conexion.nombreProducto(int(codArt))
                    var.rep.drawString(i + 87, j, str(nombreArticulo))
                    var.rep.drawRightString(i + 245, j, str(query.value(2)))
                    var.rep.drawRightString(i + 365, j, "{0:.2f}".format(float(query.value(3))) + ' €')
                    subtotal = round(float(query.value(2)) * float(query.value(3)), 2)
                    var.rep.drawRightString(i + 455, j, "{0:.2f}".format(float(subtotal)) + ' €')
                    j = j - 20

            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('factura.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1

        except Exception as error:
            print('Error reporfac %s' % str(error))

    @staticmethod
    def reportFacturasCli():
        """

        Módulo que carga las facturas pagadas de un cliente

        :return: None
        :rtype: None

        Selecciona todas las facturas pagasas de un cliente y las va escribiendo linea a linea.
        Llama a un módulo que devuelve el valor calculado del total de las ventas, es decir, el precio de la factura.
        La variable i representa los valores del eje X
        La variable j representa los valores del eje Y
        Además tiene un pie de informe para mostrar el total neto, el iva y el total de las facturas.
        Los informes se guardan en la carpeta informe y al mismo tiempo se muestran con el lector PDF que exista
        por defecto en el sistema

        """
        try:
            subtotal = 0
            iva = 0
            total = 0
            textlistado = 'FACTURAS PAGADAS'
            cliente = var.ui.editDniFac.text()
            nombrePdf = 'facturaCliente' + str(cliente) + '.pdf'
            var.rep = canvas.Canvas('informes/' + nombrePdf, pagesize=A4)
            Printer.cabecera()
            Printer.pie(textlistado)
            Printer.cabeceraCli()
            Printer.cabeceraCliente(cliente)
            query = QtSql.QSqlQuery()
            query.prepare(
                'select numFactura, fechaFactura, apellidos, estado from facturas '
                'where dniCliente = :dniCliente and estado="Pagada"')
            query.bindValue(':dniCliente', str(cliente))
            if query.exec_():
                i = 55
                j = 625
                while query.next():
                    if j <= 130:
                        var.rep.drawString(440, 110, 'Página siguiente...')
                        var.rep.showPage()
                        Printer.cabecera()
                        Printer.pie(textlistado)
                        i = 50
                        j = 600
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawString(i + 82, j, str(query.value(1)))
                    precioFac = conexion.Conexion.totalPrecioFactura(int(query.value(0)))
                    var.rep.drawRightString(i + 250, j, "{0:.2f}".format(float(precioFac[0])) + ' €')
                    var.rep.drawRightString(i + 355, j, "{0:.2f}".format(float(precioFac[1])) + ' €')
                    var.rep.drawRightString(i + 465, j, "{0:.2f}".format(float(precioFac[2])) + ' €')

                    subtotal = float(subtotal) + float(precioFac[0])
                    iva = float(iva) + float(precioFac[1])
                    total = float(total) + float(precioFac[2])
                    j = j - 20

            Printer.pieFacturasCli(subtotal, iva, total)
            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith(nombrePdf):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1

        except Exception as error:
            print('Error reporfaccli %s' % str(error))
