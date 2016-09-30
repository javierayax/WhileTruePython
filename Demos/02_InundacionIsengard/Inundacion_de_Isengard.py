#-------------------------------------------------------------------------------
# Name:        Inundacion de Isengard
# Purpose:
#
# Author:      jescudero
#
# Created:     11/08/2016
# Copyright:   (c) jescudero 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy

# Parámetros de entrada del análisis
aoi = "aoi"
dem = "DEM30M"
tin = "TIN"
isengard = "Isengard"

# Configurar variables de ambiente
arcpy.env.extent = arcpy.da.SearchCursor(aoi, "SHAPE@").next()[0].extent
arcpy.env.mask = aoi
arcpy.env.XYTolerance = "1 meters"
arcpy.env.scratchWorkspace = "in_memory"
arcpy.env.workspace = "in_memory"
arcpy.env.overwriteOutput = 1

# Parámtetros de entrada
cotaRio = 250 # cota del rio
hCresta = 225 # altura de la cresta
areaCol = 115800 # área parabólica
velCol = 148 # m/s  (532800 m/h) velocidad de la columna de agua según la Fórmula de Chezy-Manning (rugosidad, pendiente, radio hidráulico)
zInt = 10 # ¿Cada cuánto se se generan las curvas?


"""Missión: Determinar el polígono/cota de inundación (altura alcanzada por el embalse) de acuerdo a
las condiciones de llenado definidas por el caudal neto de entrada y el tiempo de simulación.
"""

# Se establecen los parámetros de la simulación
cotaEmb = cotaRio + hCresta # 475
caudalNeto = velCol * areaCol # 17138400 m3/s caudal de la columna de agua m3/s

# Generan las curvas de nivel a partir del DEM
cNivel =  arcpy.Contour_3d(dem, "curvasNivel" , zInt, cotaEmb)

# Añadir campo longitud
arcpy.AddGeometryAttributes_management(cNivel, "LENGTH")

# Crear una lista con las curvas de nivel
listaCurvas = list(set([row[0] for row in arcpy.da.SearchCursor(cNivel, ["Contour"])]))
listaCurvas.sort()

# Realizar el análisis para cada curva
i = 0
for cotaAnalisis in listaCurvas:
    if i < 15 and i > 10:
        # Generar poligono de inundacion
        whereClause = "Contour = %s" % cotaAnalisis
        curvaAnalisis = arcpy.MakeFeatureLayer_management(cNivel, "cota_%s" % str(cotaAnalisis) , whereClause)
        lineGeom = arcpy.SearchCursor(curvaAnalisis, fields = "LENGTH;SHAPE", sort_fields="LENGTH D").next().shape
        polyGeom = arcpy.Polygon(lineGeom.getPart(0))
        polyInunda = arcpy.FeatureClassToFeatureClass_conversion(polyGeom, "in_memory", "Poly_%s" % str(cotaAnalisis).replace(".", "_"))

        # Calcular el volumen bajo el polígono
        nPolys = int(arcpy.GetCount_management(polyInunda).getOutput(0))
        if nPolys > 0:
            arcpy.PolygonVolume_3d(tin, polyInunda, "<None>", "BELOW", "Volume", "SArea", "0")
            volCal = arcpy.da.SearchCursor(polyInunda, ["Volume"]).next()[0]

    i += 1

print ("%s Minutos para ser alcanzados por la inundacion" % str(volCal/caudalNeto/60))

