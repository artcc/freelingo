"""Brazilian Portuguese (phrasebook_a2) learning content."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="restaurant_a2",
        level="A2",
        situation="No restaurante",
        icon="🍽️",
        phrases=[
            PhrasebookEntry(
                text="Tem uma mesa para dois?",
                context="Pedir uma mesa",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Reservei em nome Silva.",
                context="Dizer que se reservou",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Posso ver o cardápio?",
                context="Pedir o cardápio",
                register="neutral",
            ),
            PhrasebookEntry(
                text="O que me recomenda?",
                context="Pedir um conselho ao empregado",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Quero a moqueca, por favor.",
                context="Pedir um prato",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Para beber quero uma água sem gás.",
                context="Pedir uma bebida",
                register="neutral",
            ),
            PhrasebookEntry(
                text="A conta, por favor.",
                context="Pedir a conta",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Está tudo ótimo!",
                context="Fazer um elogio ao cozinheiro",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Sou alérgico/a a...",
                context="Avisar de uma alergia",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Poderia me trazer mais pão?",
                context="Pedir algo mais",
                register="formal",
            ),
            PhrasebookEntry(
                text="Vocês têm pratos vegetarianos?",
                context="Perguntar por opções vegetarianas",
                register="neutral",
            ),
            PhrasebookEntry(
                text="O couvert está incluído?",
                context="Perguntar sobre o couvert",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Podemos dividir a conta?",
                context="Pedir para dividir a conta",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="transport_booking_a2",
        level="A2",
        situation="Viagens e transportes",
        icon="🚆",
        phrases=[
            PhrasebookEntry(
                text="Uma passagem para Recife, por favor.",
                context="Comprar uma passagem de trem",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Só ida ou ida e volta?",
                context="Perguntar o tipo de passagem",
                register="neutral",
            ),
            PhrasebookEntry(
                text="De que linha parte?",
                context="Perguntar a linha",
                register="neutral",
            ),
            PhrasebookEntry(
                text="O trem está atrasado.",
                context="Informar de um atraso",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Onde fica o ponto do ônibus?",
                context="Perguntar pelo ponto",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Quanto tempo demora?",
                context="Perguntar a duração da viagem",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Gostaria de alugar um carro.",
                context="Alugar um carro",
                register="formal",
            ),
            PhrasebookEntry(
                text="Há um ônibus para o aeroporto?",
                context="Perguntar transporte para o aeroporto",
                register="neutral",
            ),
            PhrasebookEntry(
                text="A que horas parte o próximo trem?",
                context="Perguntar horário do próximo trem",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Preciso fazer baldeação?",
                context="Perguntar por transbordos",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Onde posso comprar as passagens?",
                context="Perguntar onde comprar passagens",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="weather_talk_a2",
        level="A2",
        situation="Falar do tempo",
        icon="🌤️",
        phrases=[
            PhrasebookEntry(
                text="Como está o tempo hoje?",
                context="Perguntar sobre o tempo",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Está fazendo sol.",
                context="Dizer que está sol",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Está chovendo.",
                context="Dizer que está a chover",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Está muito calor hoje.",
                context="Comentar o calor",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Que frio que está!",
                context="Comentar o frio",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Está nublado.",
                context="Descrever céu nublado",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Que dia tão bonito!",
                context="Comentar um dia bonito",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Amanhã deve nevar.",
                context="Previsão de neve",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Está ventando hoje.",
                context="Dizer que está vento",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Como vai estar o tempo amanhã?",
                context="Perguntar a previsão do tempo",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="making_plans_a2",
        level="A2",
        situation="Fazer planos",
        icon="📅",
        phrases=[
            PhrasebookEntry(
                text="Você está livre esta noite?",
                context="Perguntar disponibilidade (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Você está a fim de ir ao cinema?",
                context="Convidar alguém (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="A que horas nos encontramos?",
                context="Combinar a hora",
                register="neutral",
            ),
            PhrasebookEntry(
                text="A gente se encontra na praça às oito.",
                context="Combinar lugar e hora",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Lamento, não posso.",
                context="Recusar um convite",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Com certeza! / Com muito gosto!",
                context="Aceitar um convite",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Que tal irmos tomar um café?",
                context="Propor uma atividade",
                register="informal",
            ),
            PhrasebookEntry(
                text="Podemos adiar para amanhã?",
                context="Pedir para adiar",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Até logo!",
                context="Despedir-se marcando encontro",
                register="informal",
            ),
            PhrasebookEntry(
                text="Passo para buscar você às sete.",
                context="Oferecer boleia",
                register="informal",
            ),
            PhrasebookEntry(
                text="Onde nos encontramos?",
                context="Perguntar o lugar do encontro",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="feelings_a2",
        level="A2",
        situation="Exprimir emoções",
        icon="😊",
        phrases=[
            PhrasebookEntry(
                text="Estou feliz.",
                context="Exprimir felicidade",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Estou triste.",
                context="Exprimir tristeza",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Estou cansado / cansada.",
                context="Exprimir cansaço",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Tenho fome.",
                context="Exprimir fome",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Tenho sede.",
                context="Exprimir sede",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Tenho medo.",
                context="Exprimir medo",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Estou bravo / brava.",
                context="Exprimir raiva",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Estou preocupado / preocupada.",
                context="Exprimir preocupação",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Estou entusiasmado / entusiasmada!",
                context="Exprimir entusiasmo",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Estou aborrecido / aborrecida.",
                context="Exprimir aborrecimento",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Que stress!",
                context="Exprimir stress",
                register="informal",
            ),
        ],
    ),
]
