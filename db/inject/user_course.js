db.user_course.insertMany([
    {
      "_id": ObjectId("78550e8e278f66cc36fe9341"),
      "user_id": ObjectId("67550e8e278f66cc36fe9342"), // profesor1
      "course_id": "101045", // Gerencia y Consultoría Informática
      "year": 2024,
      "section": "A"
    },
    {
      "_id": ObjectId("78550e8e278f66cc36fe9342"),
      "user_id": ObjectId("67550e8e278f66cc36fe9343"), // profesor2
      "course_id": "101046", // Ingeniería del Conocimiento
      "year": 2024,
      "section": "B"
    },
    {
      "_id": ObjectId("78550e8e278f66cc36fe9343"),
      "user_id": ObjectId("67550e8e278f66cc36fe9342"), // profesor1
      "course_id": "101047", // Seguridad y Auditoría Informática
      "year": 2025,
      "section": "A"
    },
    {
      "_id": ObjectId("78550e8e278f66cc36fe9344"),
      "user_id": ObjectId("67550e8e278f66cc36fe9343"), // profesor2
      "course_id": "101048", // Tecnologías Emergentes
      "year": 2025,
      "section": "B"
    },
    {
      "_id": ObjectId("78550e8e278f66cc36fe9345"),
      "user_id": ObjectId("67550e8e278f66cc36fe9342"), // profesor1
      "course_id": "101049", // Tecnología E-Business
      "year": 2024,
      "section": "A"
    }
  ]);
  