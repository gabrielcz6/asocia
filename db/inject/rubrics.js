db.rubricas.insertMany([
    {
      _id: ObjectId("64f7e98d0000000000000001"),
      nombre: "Dominio del tema",
      descripcion: "Rúbrica para evaluar el dominio del tema en exposiciones",
      fechaCreacion: new Date("2024-12-10"),
      usuarioCreadorID: ObjectId("64f7e91f0000000000000001")
    }
  ]);
  
  db.criterios.insertMany([
    {
      _id: ObjectId("64f7e98d1000000000000001"),
      nombre: "Dominio del contenido",
      descripcion: "Evalúa el nivel de conocimiento y fluidez en el tema",
      rubricaID: ObjectId("64f7e98d0000000000000001")
    },
    {
      _id: ObjectId("64f7e98d1000000000000002"),
      nombre: "Claridad en la exposición",
      descripcion: "Evalúa la claridad al explicar conceptos",
      rubricaID: ObjectId("64f7e98d0000000000000001")
    }
  ]);
  
  db.puntajes.insertMany([
    {
      _id: ObjectId("64f7e98d2000000000000001"),
      valor: 1,
      etiqueta: "Poco dominio del tema, le faltó preparación",
      criterioID: ObjectId("64f7e98d1000000000000001")
    },
    {
      _id: ObjectId("64f7e98d2000000000000002"),
      valor: 2,
      etiqueta: "Muestra que leyó el contenido y sabe",
      criterioID: ObjectId("64f7e98d1000000000000001")
    },
    {
      _id: ObjectId("64f7e98d2000000000000003"),
      valor: 3,
      etiqueta: "Dominio total, demuestra fluidez y sabe los conceptos",
      criterioID: ObjectId("64f7e98d1000000000000001")
    }
  ]);
  
  db.evaluaciones.insertMany([
    {
      _id: ObjectId("64f7e98d3000000000000001"),
      fechaEvaluacion: new Date("2024-12-11"),
      usuarioEvaluadorID: ObjectId("67550e8e278f66cc36fe9342"),
      alumnoID: ObjectId("202400002700000000000001"),
      rubricaID: ObjectId("64f7e98d0000000000000001")
    }
  ]);
  
  db.resultados.insertMany([
    {
      _id: ObjectId("64f7e98d4000000000000001"),
      puntajeID: ObjectId("64f7e98d2000000000000002"),
      criterioID: ObjectId("64f7e98d1000000000000001"),
      evaluacionID: ObjectId("64f7e98d3000000000000001")
    },
    {
      _id: ObjectId("64f7e98d4000000000000002"),
      puntajeID: ObjectId("64f7e98d2000000000000003"),
      criterioID: ObjectId("64f7e98d1000000000000002"),
      evaluacionID: ObjectId("64f7e98d3000000000000001")
    }
  ]);
  