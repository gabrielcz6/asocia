db.templates.insertMany([
    {
      _id: ObjectId("64f7e98d0000000000000001"),
      nombre: "Dominio del tema",
      descripcion: "Rúbrica para evaluar el dominio del tema en exposiciones",
      fechaCreacion: new Date("2024-12-10"),
      usuarioCreadorID: ObjectId("64f7e91f0000000000000001"),
      criterios: [
        {
          _id: ObjectId("64f7e98d1000000000000001"),
          nombre: "Dominio del contenido",
          descripcion: "Evalúa el nivel de conocimiento y fluidez en el tema",
          puntajes: [
            {
              _id: ObjectId("64f7e98d2000000000000001"),
              valor: 1,
              etiqueta: "Poco dominio del tema, le faltó preparación"
            },
            {
              _id: ObjectId("64f7e98d2000000000000002"),
              valor: 2,
              etiqueta: "Muestra que leyó el contenido y sabe"
            },
            {
              _id: ObjectId("64f7e98d2000000000000003"),
              valor: 3,
              etiqueta: "Dominio total, demuestra fluidez y sabe los conceptos"
            }
          ]
        },
        {
          _id: ObjectId("64f7e98d1000000000000002"),
          nombre: "Claridad en la exposición",
          descripcion: "Evalúa la claridad al explicar conceptos",
          puntajes: [
            {
              _id: ObjectId("64f7e98d2000000000000004"),
              valor: 1,
              etiqueta: "Poca claridad al exponer"
            },
            {
              _id: ObjectId("64f7e98d2000000000000005"),
              valor: 2,
              etiqueta: "Explicación aceptable pero poco clara"
            },
            {
              _id: ObjectId("64f7e98d2000000000000006"),
              valor: 3,
              etiqueta: "Claridad total, conceptos bien explicados"
            }
          ]
        }
      ]
    }
  ]);
  
  db.evaluations.insertMany([
    {
      _id: ObjectId("64f7e98d3000000000000001"),
      fechaEvaluacion: new Date("2024-12-11"),
      usuarioEvaluadorID: ObjectId("67550e8e278f66cc36fe9342"),
      alumnoID: ObjectId("202400002700000000000001"),
      rubrica: {
        _id: ObjectId("64f7e98d0000000000000001"),
        nombre: "Dominio del tema",
        criterios: [
          {
            _id: ObjectId("64f7e98d1000000000000001"),
            nombre: "Dominio del contenido",
            puntajeOtorgado: {
              valor: 2,
              etiqueta: "Muestra que leyó el contenido y sabe"
            }
          },
          {
            _id: ObjectId("64f7e98d1000000000000002"),
            nombre: "Claridad en la exposición",
            puntajeOtorgado: {
              valor: 3,
              etiqueta: "Claridad total, conceptos bien explicados"
            }
          }
        ]
      }
    }
  ]);
  