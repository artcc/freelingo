"""Brazilian Portuguese (phrasebook_b1) learning content."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="phone_calls_b1",
        level="B1",
        situation="Chamadas telefônicas",
        icon="📞",
        phrases=[
            PhrasebookEntry(
                text="Alô?",
                context="Atender o telefone",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Posso falar com o senhor Silva?",
                context="Pedir para falar com alguém (formal)",
                register="formal",
            ),
            PhrasebookEntry(
                text="A Maria está?",
                context="Perguntar por alguém (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Um momento, vou chamá-la.",
                context="Passar a chamada (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Pode ligar mais tarde?",
                context="Pedir para ligar mais tarde",
                register="formal",
            ),
            PhrasebookEntry(
                text="Não estou ouvindo direito.",
                context="Indicar problemas de linha",
                register="informal",
            ),
            PhrasebookEntry(
                text="Você está me ouvindo?",
                context="Verificar se o interlocutor ouve",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Você ligou para o número errado.",
                context="Informar que é um número errado",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Posso deixar uma mensagem?",
                context="Oferecer para deixar mensagem",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Ligo para você assim que puder.",
                context="Prometer voltar a ligar",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Quem fala?",
                context="Perguntar quem está ligando",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="job_interview_b1",
        level="B1",
        situation="Entrevistas de emprego",
        icon="💼",
        phrases=[
            PhrasebookEntry(
                text="Bom dia, tenho uma entrevista às dez.",
                context="Apresentar-se na recepção",
                register="formal",
            ),
            PhrasebookEntry(
                text="Estudei economia na universidade.",
                context="Falar do percurso acadêmico",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Tenho experiência no setor.",
                context="Falar da experiência profissional",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Falo três línguas: português, inglês e espanhol.",
                context="Listar as competências linguísticas",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Sou uma pessoa organizada e responsável.",
                context="Descrever as próprias qualidades",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Gosto de trabalhar em equipe.",
                context="Falar do trabalho em equipe",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Quais são os horários de trabalho?",
                context="Perguntar sobre o horário",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Que tipo de contrato oferecem?",
                context="Perguntar sobre o contrato",
                register="formal",
            ),
            PhrasebookEntry(
                text="Quando saberei o resultado da entrevista?",
                context="Perguntar prazos de resposta",
                register="formal",
            ),
            PhrasebookEntry(
                text="Obrigado pela oportunidade.",
                context="Agradecer no final da entrevista",
                register="formal",
            ),
            PhrasebookEntry(
                text="Como é o ambiente de trabalho aqui?",
                context="Perguntar sobre a cultura da empresa",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="giving_opinions_b1",
        level="B1",
        situation="Dar opiniões",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Na minha opinião é uma boa ideia.",
                context="Exprimir a própria opinião",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Não concordo.",
                context="Exprimir desacordo",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Você tem razão.",
                context="Dar razão a alguém",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Talvez você esteja enganado.",
                context="Exprimir desacordo suave",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Não tenho a certeza.",
                context="Exprimir incerteza",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Depende.",
                context="Evitar uma resposta categórica",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Do meu ponto de vista...",
                context="Introduzir a própria perspectiva",
                register="neutral",
            ),
            PhrasebookEntry(
                text="O que você acha?",
                context="Pedir uma opinião (informal)",
                register="informal",
            ),
            PhrasebookEntry(
                text="O que acha?",
                context="Pedir uma opinião (formal)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Discordo completamente.",
                context="Exprimir forte desacordo",
                register="formal",
            ),
            PhrasebookEntry(
                text="De fato, você tem toda a razão.",
                context="Admitir que o outro tem razão",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Permita-me discordar.",
                context="Introduzir educadamente um desacordo",
                register="formal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="health_appointments_b1",
        level="B1",
        situation="Saúde e consultas médicas",
        icon="🏥",
        phrases=[
            PhrasebookEntry(
                text="Gostaria de marcar uma consulta.",
                context="Marcar uma consulta",
                register="formal",
            ),
            PhrasebookEntry(
                text="Tenho dores de cabeça há dois dias.",
                context="Descrever um sintoma",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Está doendo aqui.",
                context="Indicar onde se sente dor",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Tenho febre.",
                context="Dizer que se tem febre",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Sou alérgico/a à penicilina.",
                context="Declarar uma alergia",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Preciso de uma receita?",
                context="Perguntar sobre a prescrição",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Tome este medicamento duas vezes ao dia.",
                context="Receber instruções sobre o medicamento",
                register="formal",
            ),
            PhrasebookEntry(
                text="Quando posso vir?",
                context="Perguntar por disponibilidade",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Preciso de um atestado médico.",
                context="Pedir um atestado",
                register="formal",
            ),
            PhrasebookEntry(
                text="É urgente.",
                context="Indicar urgência",
                register="neutral",
            ),
        ],
    ),
]
