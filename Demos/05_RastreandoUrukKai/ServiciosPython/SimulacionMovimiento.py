#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jescudero
#
# Created:     28/04/2015
# Copyright:   (c) jescudero 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, time

log = ""

def inventariarCampo(Tabla, Campo):
    lista = []
    with arcpy.da.SearchCursor(Tabla, (Campo)) as cursor:
        for row in cursor:
            if row[0] not in lista:
                lista.append(row[0])
    lista.sort()
    return lista


class FlotaVehiculos():
    def __init__(self, pathPrincipal, campoIdVehiculo, pathGeometria, campoIdVehiculoGeom, campoMomentoTiempoGeom):

        self.path = pathPrincipal
        self.campoIdVehiculo = campoIdVehiculo

        self.pathGeom = pathGeometria
        self.campoIdVehiculoGeom = campoIdVehiculoGeom
        self.campoMomentoTiempoGeom= campoMomentoTiempoGeom

        self.campoMomentoTiempoObj = arcpy.ListFields(pathGeometria, campoMomentoTiempoGeom)[0]

        return

    def obtenerGeometrias(self, momentoTiempo):

        self.whereClause = "%s = %s" % (self.campoMomentoTiempoGeom, momentoTiempo)

        dicGeoms = {}

        with arcpy.da.SearchCursor(self.pathGeom, [self.campoIdVehiculoGeom,"SHAPE@XY"], self.whereClause) as cursor:
            for row in cursor:
                idVehiculo, geom = row
                dicGeoms[idVehiculo] = geom

        self.dicGeoms = dicGeoms

        return


    def actualizarLocalizacionVehiculos(self):
        with arcpy.da.UpdateCursor(self.path, [self.campoIdVehiculo, "SHAPE@XY"]) as cursor:
            for row in cursor:
                try:
                    idVehiculo = row[0]
                    geom = self.dicGeoms[idVehiculo]
                    row[1] = geom
                    cursor.updateRow(row)
                except:
                    pass
        return

capaVehiculos = arcpy.GetParameterAsText(0)
campoIdVehiculo = arcpy.GetParameterAsText(1)

capaGeomVehiculos = arcpy.GetParameterAsText(2)
campoIdGeomVehiculos = arcpy.GetParameterAsText(3)
campoMomentoTiempo = arcpy.GetParameterAsText(4)# debe ser numerico

intervaloActualizacion = int(arcpy.GetParameterAsText(5))

flota = FlotaVehiculos(capaVehiculos, campoIdVehiculo, capaGeomVehiculos, campoIdGeomVehiculos, campoMomentoTiempo)

momentos = inventariarCampo(capaGeomVehiculos, campoMomentoTiempo)

i = -1
while True:
    i = i+1
    try:
        momento = momentos[i]
    except:
        i = 0
        momento = momentos[i]
    time.sleep(intervaloActualizacion)
    flota.obtenerGeometrias(momento)
    flota.actualizarLocalizacionVehiculos()






