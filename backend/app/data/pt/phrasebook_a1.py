"""Portuguese phrasebook — A1 categories."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="greetings",
        level="A1",
        situation="Sauda\u00e7\u00f5es e apresenta\u00e7\u00f5es",
        icon="\U0001f44b",
        phrases=[
            PhrasebookEntry(
                text="Ol\u00e1!",
                context="Sauda\u00e7\u00e3o informal",
                register="informal",
            ),
            PhrasebookEntry(
                text="Bom dia.",
                context="Saudação durante a manhã, em situações formais e informais",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Boa tarde.",
                context="Saudação durante a tarde",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Boa noite.",
                context="Saudação ou despedida à noite",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Como est\u00e1s?",
                context="Perguntar como est\u00e1 algu\u00e9m (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Como est\u00e1?",
                context="Perguntar como est\u00e1 algu\u00e9m (formal)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Estou bem, obrigado. E tu?",
                context="Responder e retribuir (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Estou bem, obrigado. E o senhor?",
                context="Responder e retribuir (formal)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Muito prazer em conhecer-te.",
                context="No primeiro encontro (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Muito prazer em conhec\u00ea-lo.",
                context="No primeiro encontro (formal)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Chamo-me Jo\u00e3o.", context="Apresentar-se", register="neutral"
            ),
            PhrasebookEntry(
                text="De onde \u00e9s?",
                context="Perguntar a proveni\u00eancia (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Sou portugu\u00eas / portuguesa.",
                context="Indicar a nacionalidade",
                register="neutral",
            ),
            PhrasebookEntry(text="Adeus!", context="Despedida comum", register="neutral"),
            PhrasebookEntry(
                text="At\u00e9 logo!", context="Despedida informal", register="informal"
            ),
        ],
    ),
    PhrasebookCategory(
        id="basic_requests",
        level="A1",
        situation="Pedidos b\u00e1sicos e cortesia",
        icon="\U0001f64f",
        phrases=[
            PhrasebookEntry(
                text="Por favor.", context="Pedir algo educadamente", register="neutral"
            ),
            PhrasebookEntry(text="Obrigado.", context="Agradecer (masculino)", register="neutral"),
            PhrasebookEntry(
                text="Muito obrigado!",
                context="Agradecer com \u00eanfase",
                register="neutral",
            ),
            PhrasebookEntry(
                text="De nada.",
                context="Responder a um agradecimento",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Desculpa.",
                context="Pedir desculpa (informal)",
                register="informal",
            ),
            PhrasebookEntry(text="Desculpe.", context="Pedir desculpa (formal)", register="formal"),
            PhrasebookEntry(text="Lamento.", context="Exprimir pesar", register="neutral"),
            PhrasebookEntry(
                text="N\u00e3o h\u00e1 problema.",
                context="Tranquilizar ap\u00f3s um pedido de desculpas",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Podes ajudar-me?",
                context="Pedir ajuda (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Pode ajudar-me?",
                context="Pedir ajuda (formal)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Posso...?",
                context="Pedir autoriza\u00e7\u00e3o (ex: Posso entrar?)",
                register="neutral",
            ),
            PhrasebookEntry(
                text="N\u00e3o percebo.",
                context="Indicar que n\u00e3o se entende",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="numbers_time_a1",
        level="A1",
        situation="N\u00fameros e horas",
        icon="\U0001f552",
        phrases=[
            PhrasebookEntry(
                text="Que horas s\u00e3o?",
                context="Perguntar as horas",
                register="neutral",
            ),
            PhrasebookEntry(
                text="S\u00e3o tr\u00eas horas.",
                context="Dizer a hora exata",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00c9 uma hora.",
                context="Dizer uma hora (singular)",
                register="neutral",
            ),
            PhrasebookEntry(
                text="S\u00e3o tr\u00eas e meia.",
                context="Dizer a meia hora",
                register="neutral",
            ),
            PhrasebookEntry(
                text="S\u00e3o quinze para as quatro.",
                context='Dizer a hora com "para"',
                register="neutral",
            ),
            PhrasebookEntry(
                text="A que horas parte?",
                context="Perguntar a hora de partida",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Quanto custa?",
                context="Perguntar o pre\u00e7o",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Custa dez euros.",
                context="Indicar o pre\u00e7o",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Quantos anos tens?",
                context="Perguntar a idade (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Que horas s\u00e3o? \u2014 S\u00e3o [hora].",
                context="Perguntar e dizer as horas",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="shopping_basic_a1",
        level="A1",
        situation="Fazer compras",
        icon="\U0001f6cd\ufe0f",
        phrases=[
            PhrasebookEntry(
                text="Quanto custa?",
                context="Perguntar o pre\u00e7o",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00c9 muito caro.",
                context="Dizer que algo \u00e9 caro",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Tem algo mais barato?",
                context="Pedir uma alternativa mais barata",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Posso pagar com cart\u00e3o?",
                context="Perguntar se aceitam cart\u00e3o",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Pago em dinheiro.",
                context="Indicar pagamento em dinheiro",
                register="neutral",
            ),
            PhrasebookEntry(
                text="D\u00e1-me um recibo, por favor?",
                context="Pedir o recibo",
                register="formal",
            ),
            PhrasebookEntry(
                text="Que tamanho usa?",
                context="Perguntar o tamanho (loja de roupa)",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Posso experimentar?",
                context="Pedir para experimentar uma pe\u00e7a",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Tem isto noutra cor?",
                context="Perguntar por variantes de cor",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Levo este, obrigado.",
                context="Confirmar a compra (masculino)",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="asking_directions_a1",
        level="A1",
        situation="Pedir informa\u00e7\u00f5es",
        icon="\U0001f5fa\ufe0f",
        phrases=[
            PhrasebookEntry(
                text="Desculpe, onde fica a esta\u00e7\u00e3o?",
                context="Perguntar onde fica um lugar",
                register="formal",
            ),
            PhrasebookEntry(
                text="Fica longe?",
                context="Perguntar se um lugar \u00e9 distante",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Fica aqui perto.",
                context="Responder que \u00e9 perto",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Vire \u00e0 direita.",
                context="Dar indica\u00e7\u00e3o: direita",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Vire \u00e0 esquerda.",
                context="Dar indica\u00e7\u00e3o: esquerda",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Siga sempre em frente.",
                context="Dar indica\u00e7\u00e3o: em frente",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Fica na esquina.",
                context="Indicar a posi\u00e7\u00e3o na esquina",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Onde fica a casa de banho?",
                context="Perguntar pela casa de banho",
                register="neutral",
            ),
            PhrasebookEntry(
                text="H\u00e1 uma farm\u00e1cia aqui perto?",
                context="Perguntar por um servi\u00e7o espec\u00edfico",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Estou perdido / perdida.",
                context="Dizer que se est\u00e1 perdido",
                register="neutral",
            ),
        ],
    ),
]
