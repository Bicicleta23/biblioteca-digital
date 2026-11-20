
const express = require("express");
const cors = require("cors");
const swaggerUi = require("swagger-ui-express");

const app = express();
const PORT = process.env.PORT || 3000;

const OLLAMA_URL =
  process.env.OLLAMA_URL || "http://localhost:11434";

const OLLAMA_MODEL =
  process.env.OLLAMA_MODEL || "llama3.2:3b";

app.use(cors());
app.use(express.json());

const swaggerDocument = {
  openapi: "3.0.0",
  info: {
    title: "API Biblioteca Digital con IA",
    version: "2.0.0",
    description:
      "Microservicio Node.js integrado con Django y Ollama"
  },
  paths: {
    "/api/saludo": {
      get: {
        summary: "Comprobar funcionamiento de Node.js",
        responses: {
          200: { description: "Servicio funcionando" }
        }
      }
    },
    "/api/libros/recomendacion": {
      post: {
        summary: "Generar recomendación de libros con IA",
        requestBody: {
          required: true,
          content: {
            "application/json": {
              schema: {
                type: "object",
                required: ["genero"],
                properties: {
                  genero: {
                    type: "string",
                    example: "misterio"
                  }
                }
              }
            }
          }
        },
        responses: {
          200: { description: "Recomendación generada por IA" },
          400: { description: "Género inválido" },
          502: { description: "Error de comunicación con Ollama" }
        }
      }
    }
  }
};

app.use(
  "/api-docs",
  swaggerUi.serve,
  swaggerUi.setup(swaggerDocument)
);

app.get("/api/saludo", (req, res) => {
  res.json({
    mensaje: "Microservicio Node.js funcionando correctamente",
    ia: "Ollama"
  });
});

app.post("/api/libros/recomendacion", async (req, res) => {
  const { genero } = req.body;

  if (
    typeof genero !== "string" ||
    !genero.trim() ||
    genero.length > 100
  ) {
    return res.status(400).json({
      error: "Debes proporcionar un género válido"
    });
  }

  try {
    const respuesta = await fetch(`${OLLAMA_URL}/api/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: OLLAMA_MODEL,
        prompt:
          `Recomienda un libro real del género ${genero}. ` +
          "Indica título, autor y una breve explicación. " +
          "Responde en español. No inventes títulos.",
        stream: false
      }),
      signal: AbortSignal.timeout(120000)
    });

    if (!respuesta.ok) {
      throw new Error(`Ollama respondió HTTP ${respuesta.status}`);
    }

    const datos = await respuesta.json();

    res.json({
      genero,
      modelo: OLLAMA_MODEL,
      recomendacion: datos.response
    });

  } catch (error) {
    console.error("Error de Ollama:", error.message);

    res.status(502).json({
      error: "No se pudo generar la recomendación con IA",
      detalle: "Verifica que Ollama esté funcionando y el modelo esté descargado."
    });
  }
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Node.js funcionando en puerto ${PORT}`);
});
