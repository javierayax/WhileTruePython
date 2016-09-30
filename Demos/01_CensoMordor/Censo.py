#-------------------------------------------------------------------------------
# Name:        Censo de Mordor
# Purpose:
#
# Author:      jescudero
#
# Created:     11/08/2016
# Copyright:   (c) jescudero 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy, time

t1 = time.clock()
# Carpeta de salidas
salidas = r"C:\Users\jescudero\Desktop\Python\Demos\01_CensoMordor\Salidas"
escala = 325000

# Identificar el mapa actual
mxd = arcpy.mapping.MapDocument("current")

# Cambiar la vista activa a Layout
mxd.activeView = u'PAGE_LAYOUT'

# Identificar los dataframes
main = arcpy.mapping.ListDataFrames(mxd)[0]
overview = arcpy.mapping.ListDataFrames(mxd, "Overview")[0]

# Identificar layers mapa de referencia
cuadranteActual = arcpy.mapping.ListLayers(mxd, "cuadranteActual", overview)[0]
grilla = arcpy.mapping.ListLayers(mxd, "Grilla", overview)[0]

# Identificar los rótulos del mapa
a1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "a1")[0]
a2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "a2")[0]

with arcpy.da.SearchCursor("Grilla", ["SHAPE@", "PageName", "PageNumber"]) as cursor:
    for row in cursor:
        # Establecer el extent
        main.extent = row[0].extent

        # Cambiar la escala
        main.scale = escala

        # Apagar los layers
        cuadranteActual.visible = 1

        # Cambiar textos del layout
        a1.text = row[1]
        a2.text = row[2]

        # Establecer el filtro para el mapa de referencia y resaltar el cuadrante actual
        cuadranteActual.definitionQuery = "PageName = '%s'" % row[1]
        grilla.definitionQuery = "PageName <> '%s'" % row[1]

        # Exportar el mapa
        arcpy.mapping.ExportToPDF(mxd, r"%s\plano_%s.pdf" % (salidas, row[1]), "PAGE_LAYOUT", resolution = 90)

t2 = time.clock()
print (str(t2-t1) + " s")
