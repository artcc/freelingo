"""Brazilian Portuguese (phrasebook_a1) learning content."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="greetings",
        level="A1",
        situation="Saudações e apresentações",
        icon="👋",
        phrases=[
            PhrasebookEntry(
                text="Olá!",
                context="Saudação informal",
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
                text="Como você está?",
                context="Perguntar como está alguém (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Como está?",
                context="Perguntar como está alguém (formal)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Estou bem, obrigado. E você?",
                context="Responder e retribuir (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Estou bem, obrigado. E o senhor?",
                context="Responder e retribuir (formal)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Prazer em conhecer você.",
                context="No primeiro encontro (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Muito prazer em conhecê-lo.",
                context="No primeiro encontro (formal)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Eu me chamo João.",
                context="Apresentar-se",
                register="neutral",
            ),
            PhrasebookEntry(
                text="De onde você é?",
                context="Perguntar a proveniência (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Sou brasileiro / brasileira.",
                context="Indicar a nacionalidade",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Tchau!",
                context="Despedida comum",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Até logo!",
                context="Despedida informal",
                register="informal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="basic_requests",
        level="A1",
        situation="Pedidos básicos e cortesia",
        icon="🙏",
        phrases=[
            PhrasebookEntry(
                text="Por favor.",
                context="Pedir algo educadamente",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Obrigado.",
                context="Agradecer (masculino)",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Muito obrigado!",
                context="Agradecer com ênfase",
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
            PhrasebookEntry(
                text="Desculpe.",
                context="Pedir desculpa (formal)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Lamento.",
                context="Exprimir pesar",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Não há problema.",
                context="Tranquilizar após um pedido de desculpas",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Você pode me ajudar?",
                context="Pedir ajuda (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="O senhor pode me ajudar?",
                context="Pedir ajuda (formal)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Posso...?",
                context="Pedir autorização (ex: Posso entrar?)",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Não entendi.",
                context="Indicar que não se entende",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="numbers_time_a1",
        level="A1",
        situation="Números e horas",
        icon="🕒",
        phrases=[
            PhrasebookEntry(
                text="Que horas são?",
                context="Perguntar as horas",
                register="neutral",
            ),
            PhrasebookEntry(
                text="São três horas.",
                context="Dizer a hora exata",
                register="neutral",
            ),
            PhrasebookEntry(
                text="É uma hora.",
                context="Dizer uma hora (singular)",
                register="neutral",
            ),
            PhrasebookEntry(
                text="São três e meia.",
                context="Dizer a meia hora",
                register="neutral",
            ),
            PhrasebookEntry(
                text="São quinze para as quatro.",
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
                context="Perguntar o preço",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Custa dez reais.",
                context="Indicar o preço",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Quantos anos você tem?",
                context="Perguntar a idade (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Que horas são? — São [hora].",
                context="Perguntar e dizer as horas",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="shopping_basic_a1",
        level="A1",
        situation="Fazer compras",
        icon="🛍️",
        phrases=[
            PhrasebookEntry(
                text="Quanto custa?",
                context="Perguntar o preço",
                register="neutral",
            ),
            PhrasebookEntry(
                text="É muito caro.",
                context="Dizer que algo é caro",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Tem algo mais barato?",
                context="Pedir uma alternativa mais barata",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Posso pagar com cartão?",
                context="Perguntar se aceitam cartão",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Pago em dinheiro.",
                context="Indicar pagamento em dinheiro",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Poderia me dar um recibo, por favor?",
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
                context="Pedir para experimentar uma peça",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Tem isso em outra cor?",
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
        situation="Pedir informações",
        icon="🗺️",
        phrases=[
            PhrasebookEntry(
                text="Desculpe, onde fica a estação?",
                context="Perguntar onde fica um lugar",
                register="formal",
            ),
            PhrasebookEntry(
                text="Fica longe?",
                context="Perguntar se um lugar é distante",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Fica aqui perto.",
                context="Responder que é perto",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Vire à direita.",
                context="Dar indicação: direita",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Vire à esquerda.",
                context="Dar indicação: esquerda",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Siga sempre em frente.",
                context="Dar indicação: em frente",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Fica na esquina.",
                context="Indicar a posição na esquina",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Onde fica o banheiro?",
                context="Perguntar pelo banheiro",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Há uma farmácia aqui perto?",
                context="Perguntar por um serviço específico",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Estou perdido / perdida.",
                context="Dizer que se está perdido",
                register="neutral",
            ),
        ],
    ),
]
