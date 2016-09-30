import arcpy, multiprocessing

# Carpeta de salidas
salidas = r"C:\Users\jescudero\Desktop\Python\Demos\01_CensoMordor\Salidas"


def exportarMapa(row):
    # Identificar el mapa actual
    mxd = arcpy.mapping.MapDocument(r"C:\Users\jescudero\Desktop\Python\Demos\01_CensoMordor\MiddlearthClassic.mxd")

    # Identificar los dataframes
    main = arcpy.mapping.ListDataFrames(mxd)[0]
    overview = arcpy.mapping.ListDataFrames(mxd, "Overview")[0]

    # Identificar layers mapa de referencia
    cuadranteActual = arcpy.mapping.ListLayers(mxd, "cuadranteActual", overview)[0]
    grilla = arcpy.mapping.ListLayers(mxd, "Grilla", overview)[0]

    # Identificar los rótulos del mapa
    a1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "a1")[0]
    a2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "a2")[0]

    # Establecer el extent
    main.extent = row[0].extent

    # Cambiar la escala
    main.scale = 1000000

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

    print row

    return


if __name__ == '__main__':
    # Se genera las geometrias para procesamineto por bloques
    rows = [row for row in arcpy.da.SearchCursor(r"C:\Users\jescudero\Documents\ArcGIS\Default.gdb\GridIndexFeatures", ["SHAPE@", "PageName", "PageNumber"])]

    # Se estable el numero de procesos
    #NUM_PROCESSES = multiprocessing.cpu_count()
    NUM_PROCESSES = 4
    pool = multiprocessing.Pool(NUM_PROCESSES)

    # se invoca la funcion de analisis para cada geometria
    pool.map(exportarMapa, rows)

    pool.close()
    pool.join()