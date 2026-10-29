"""Spanish phrasebook — A1 categories."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="greetings",
        level="A1",
        situation="Saludos y presentaciones",
        icon="\U0001f44b",
        phrases=[
            PhrasebookEntry(text="\u00a1Hola!", context="Saludo informal", register="informal"),
            PhrasebookEntry(
                text="Buenos d\u00edas.",
                context="Saludo por la ma\u00f1ana",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Buenas tardes.",
                context="Saludo desde el mediod\u00eda hasta el anochecer",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Buenas noches.", context="Saludo o despedida por la noche", register="neutral"
            ),
            PhrasebookEntry(
                text="\u00bfQu\u00e9 tal?",
                context="Preguntar c\u00f3mo est\u00e1 alguien",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfC\u00f3mo est\u00e1s?",
                context="Preguntar por el estado de alguien (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="\u00bfC\u00f3mo est\u00e1?",
                context="Preguntar por el estado de alguien (formal)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Bien, gracias. \u00bfY t\u00fa?",
                context="Responder y devolver la pregunta (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Muy bien, \u00bfy usted?",
                context="Responder y devolver la pregunta (formal)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Mucho gusto.", context="Al conocer a alguien", register="neutral"
            ),
            PhrasebookEntry(
                text="Encantado/a.",
                context="Al conocer a alguien",
                register="neutral",
            ),
            PhrasebookEntry(text="Me llamo [nombre].", context="Presentarse", register="neutral"),
            PhrasebookEntry(
                text="Soy de [pa\u00eds/ciudad].",
                context="Decir de d\u00f3nde eres",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00a1Hasta luego!",
                context="Despedida cotidiana",
                register="neutral",
            ),
            PhrasebookEntry(text="Adi\u00f3s.", context="Despedida general", register="neutral"),
            PhrasebookEntry(
                text="\u00a1Chao!",
                context="Despedida muy informal (com\u00fan en Latinoam\u00e9rica)",
                register="informal",
            ),
            PhrasebookEntry(
                text="\u00a1Nos vemos!",
                context="Despedida informal",
                register="informal",
            ),
            PhrasebookEntry(
                text="Cu\u00eddate.", context="Despedida afectuosa", register="neutral"
            ),
            PhrasebookEntry(
                text="Que tengas buen d\u00eda.",
                context="Despedida cordial",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfDe d\u00f3nde eres?",
                context="Preguntar el origen de alguien",
                register="informal",
            ),
            PhrasebookEntry(
                text="Perdona, \u00bfc\u00f3mo te llamas?",
                context="Preguntar el nombre a alguien",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="basic_requests",
        level="A1",
        situation="Peticiones b\u00e1sicas y cortes\u00eda",
        icon="\U0001f64f",
        phrases=[
            PhrasebookEntry(
                text="\u00bfMe puedes ayudar, por favor?",
                context="Pedir ayuda",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfPuedes repetir, por favor?",
                context="Cuando no has entendido",
                register="neutral",
            ),
            PhrasebookEntry(
                text="No entiendo.",
                context="Decir que no entiendes",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfPuedes hablar m\u00e1s despacio?",
                context="Cuando alguien habla muy r\u00e1pido",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfC\u00f3mo se dice [palabra] en espa\u00f1ol?",
                context="Preguntar por una traducci\u00f3n",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfQu\u00e9 significa [palabra]?",
                context="Preguntar por una definici\u00f3n",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Perdona, no lo s\u00e9.",
                context="Decir que no sabes algo",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Disculpa / Disculpe.",
                context="Llamar la atenci\u00f3n de alguien",
                register="neutral",
            ),
            PhrasebookEntry(text="Lo siento.", context="Disculparse", register="neutral"),
            PhrasebookEntry(
                text="No pasa nada.", context="Aceptar una disculpa", register="neutral"
            ),
            PhrasebookEntry(
                text="Muchas gracias.", context="Expresar gratitud", register="neutral"
            ),
            PhrasebookEntry(text="De nada.", context="Responder a las gracias", register="neutral"),
            PhrasebookEntry(
                text="No hay de qu\u00e9.",
                context="Responder a las gracias (m\u00e1s cordial)",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Por favor.",
                context="A\u00f1adir cortes\u00eda a una petici\u00f3n",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Gracias de antemano.",
                context="Agradecer por adelantado",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Con permiso.",
                context="Pasar entre personas o pedir paso",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="numbers_time_a1",
        level="A1",
        situation="N\u00fameros y la hora",
        icon="\U0001f552",
        phrases=[
            PhrasebookEntry(
                text="\u00bfQu\u00e9 hora es?",
                context="Preguntar la hora",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Es la una.",
                context="Decir la hora en punto (1)",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Son las [hora].",
                context="Decir la hora en punto",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Son las [hora] y media.",
                context="Decir la hora y media",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Son las [hora] y cuarto.",
                context="Decir la hora y cuarto",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Son las [hora] menos cuarto.",
                context="Decir la hora menos cuarto",
                register="neutral",
            ),
            PhrasebookEntry(
                text="La reuni\u00f3n es a las [hora].",
                context="Indicar una hora programada",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfCu\u00e1nto cuesta?",
                context="Preguntar el precio",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Cuesta [cantidad] euros.",
                context="Decir un precio",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfMe trae la cuenta, por favor?",
                context="Pedir la cuenta en un bar o restaurante",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Son [cantidad] euros con [c\u00e9ntimos].",
                context="Dar un precio exacto",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfAceptan tarjeta?",
                context="Preguntar si se puede pagar con tarjeta",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="shopping_basic_a1",
        level="A1",
        situation="De compras (b\u00e1sico)",
        icon="\U0001f6cd\ufe0f",
        phrases=[
            PhrasebookEntry(
                text="Quer\u00eda [producto], por favor.",
                context="Pedir algo en una tienda",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfCu\u00e1nto cuesta esto?",
                context="Preguntar el precio",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfTienen esto en [color/talla]?",
                context="Preguntar por disponibilidad",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Me lo llevo.", context="Decidir comprar algo", register="neutral"
            ),
            PhrasebookEntry(
                text="Solo estoy mirando, gracias.",
                context="Decir al dependiente que solo miras",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfMe lo puedo probar?",
                context="Preguntar para probarse ropa",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Me queda grande / peque\u00f1o.",
                context="Explicar un problema de talla",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Es demasiado caro.",
                context="Decir que algo es caro",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfPuedo pagar con tarjeta?",
                context="Preguntar por m\u00e9todos de pago",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfMe da una bolsa, por favor?",
                context="Pedir una bolsa",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfMe puede dar un recibo?",
                context="Pedir un recibo",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfTienen m\u00e1s modelos?",
                context="Preguntar por m\u00e1s opciones",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Prefiero el azul.",
                context="Indicar preferencia de color",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="asking_directions_a1",
        level="A1",
        situation="Pedir y dar direcciones",
        icon="\U0001f5fa\ufe0f",
        phrases=[
            PhrasebookEntry(
                text="Disculpe, \u00bfd\u00f3nde est\u00e1 [lugar]?",
                context="Preguntar por una ubicaci\u00f3n",
                register="formal",
            ),
            PhrasebookEntry(
                text="\u00bfC\u00f3mo se va a [lugar]?",
                context="Preguntar por una direcci\u00f3n",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00bfEst\u00e1 lejos de aqu\u00ed?",
                context="Preguntar por la distancia",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Gira a la derecha.",
                context="Dar una indicaci\u00f3n",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Gira a la izquierda.",
                context="Dar una indicaci\u00f3n",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Sigue todo recto.",
                context="Dar una indicaci\u00f3n",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Est\u00e1 a la derecha.",
                context="Describir una ubicaci\u00f3n",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Est\u00e1 a la izquierda.",
                context="Describir una ubicaci\u00f3n",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Est\u00e1 al lado de [lugar].",
                context="Describir ubicaci\u00f3n relativa",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Est\u00e1 enfrente de [lugar].",
                context="Describir ubicaci\u00f3n relativa",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Est\u00e1 cerca de [lugar].",
                context="Describir proximidad",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Cruza la calle.",
                context="Dar una indicaci\u00f3n",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Toma la primera a la derecha.",
                context="Dar una indicaci\u00f3n precisa",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Est\u00e1 a cinco minutos andando.",
                context="Indicar distancia en tiempo",
                register="neutral",
            ),
        ],
    ),
]
