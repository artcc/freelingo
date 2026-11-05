"""Russian A1 placement: eight grammar, eight vocabulary and four reading items."""

from app.data._types import AssessmentQuestion

A1_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        id="ru-g-a1-001",
        skill="grammar",
        difficulty="A1",
        question="Анна показывает одну комнату: «Это моя ___ комната». Выберите форму слова.",
        options=["новый", "новое", "новая", "новые"],
        correct="новая",
        grammar_slug="ru-adjective-agreement",
    ),
    AssessmentQuestion(
        id="ru-g-a1-002",
        skill="grammar",
        difficulty="A1",
        question="Олег и Анна учат русский язык: «Мы каждый день ___ по-русски». Дополните фразу.",
        options=["говорим", "говоришь", "говорит", "говорят"],
        correct="говорим",
        grammar_slug="ru-present-second",
    ),
    AssessmentQuestion(
        id="ru-g-a1-003",
        skill="grammar",
        difficulty="A1",
        question="Анна хочет кофе, но молоко закончилось. Она говорит: «У нас нет ___».",
        options=["молоком", "молоке", "молоко", "молока"],
        correct="молока",
        grammar_slug="ru-genitive-basics",
    ),
    AssessmentQuestion(
        id="ru-g-a1-004",
        skill="grammar",
        difficulty="A1",
        question="Маша уже на уроке. Она пишет маме: «Я сейчас в ___». Выберите форму слова школа.",
        options=["школу", "школе", "школой", "школа"],
        correct="школе",
        grammar_slug="ru-location",
    ),
    AssessmentQuestion(
        id="ru-g-a1-005",
        skill="grammar",
        difficulty="A1",
        question="Иван выходит из дома. Куда он идёт? «Я иду в ___ за лекарством».",
        options=["аптеке", "аптеку", "аптекой", "аптека"],
        correct="аптеку",
        grammar_slug="ru-direction",
    ),
    AssessmentQuestion(
        id="ru-g-a1-006",
        skill="grammar",
        difficulty="A1",
        question="Анна рассказывает о себе: «___ двадцать два года». Выберите правильную форму.",
        options=["Меня", "Я", "Мной", "Мне"],
        correct="Мне",
        grammar_slug="ru-dative-age-likes",
    ),
    AssessmentQuestion(
        id="ru-g-a1-007",
        skill="grammar",
        difficulty="A1",
        question="Олег спрашивает сестру о вчерашнем вечере. Она отвечает: «Вчера я ___ книгу дома».",
        options=["читала", "читало", "читал", "читали"],
        correct="читала",
        grammar_slug="ru-past",
    ),
    AssessmentQuestion(
        id="ru-g-a1-008",
        skill="grammar",
        difficulty="A1",
        question="Завтра у Ивана выходной. Он говорит: «Я буду ___ в парке».",
        options=["гуляю", "гуляет", "гулять", "гулял"],
        correct="гулять",
        grammar_slug="ru-future",
    ),
    AssessmentQuestion(
        id="ru-v-a1-001",
        skill="vocabulary",
        difficulty="A1",
        question="Врач сказал Анне купить лекарство. Куда ей нужно идти за покупкой?",
        options=["В школу.", "В аптеку.", "В музей.", "В гостиницу."],
        correct="В аптеку.",
    ),
    AssessmentQuestion(
        id="ru-v-a1-002",
        skill="vocabulary",
        difficulty="A1",
        question="На фотографии мама Ирины и маленькая дочь Ирины. Кто мама Ирины для этой девочки?",
        options=["Сестра.", "Дочь.", "Жена.", "Бабушка."],
        correct="Бабушка.",
    ),
    AssessmentQuestion(
        id="ru-v-a1-003",
        skill="vocabulary",
        difficulty="A1",
        question="Суп совсем не солёный. Что можно добавить, чтобы изменить это?",
        options=["Соль.", "Сахар.", "Воду.", "Молоко."],
        correct="Соль.",
    ),
    AssessmentQuestion(
        id="ru-v-a1-004",
        skill="vocabulary",
        difficulty="A1",
        question="Сегодня четверг. Урок будет завтра. В какой день урок?",
        options=["В среду.", "В субботу.", "В пятницу.", "Во вторник."],
        correct="В пятницу.",
    ),
    AssessmentQuestion(
        id="ru-v-a1-005",
        skill="vocabulary",
        difficulty="A1",
        question="На улице холодно. С неба падают белые хлопья. Что это?",
        options=["Дождь.", "Солнце.", "Снег.", "Ветер."],
        correct="Снег.",
    ),
    AssessmentQuestion(
        id="ru-v-a1-006",
        skill="vocabulary",
        difficulty="A1",
        question="Вы впервые видите нового преподавателя. Как вежливо спросить его имя, обращаясь на вы?",
        options=["Как вас зовут?", "Как тебя зовут?", "Где вы работаете?", "Что это значит?"],
        correct="Как вас зовут?",
    ),
    AssessmentQuestion(
        id="ru-v-a1-007",
        skill="vocabulary",
        difficulty="A1",
        question="В сумку Анны не помещаются все вещи для поездки. Ей нужна сумка другого размера. Какая?",
        options=["Маленькая.", "Зелёная.", "Старая.", "Большая."],
        correct="Большая.",
    ),
    AssessmentQuestion(
        id="ru-v-a1-008",
        skill="vocabulary",
        difficulty="A1",
        question="Анна стоит у двери номера в гостинице. Чем она может открыть замок?",
        options=["Билетом.", "Ключом.", "Паспортом.", "Картой города."],
        correct="Ключом.",
    ),
    AssessmentQuestion(
        id="ru-r-a1-001",
        skill="reading",
        difficulty="A1",
        question=(
            "Прочитайте сообщение: «Олег, я уже в кафе. У нас дома нет хлеба. "
            "Купи его в магазине, пожалуйста, а потом приходи сюда. Анна». "
            "Что Олегу нужно сделать сначала?"
        ),
        options=[
            "Прийти к Анне в кафе.",
            "Пойти на работу.",
            "Отнести хлеб домой.",
            "Купить хлеб в магазине.",
        ],
        correct="Купить хлеб в магазине.",
    ),
    AssessmentQuestion(
        id="ru-r-a1-002",
        skill="reading",
        difficulty="A1",
        question=(
            "Прочитайте: «Сегодня суббота. Обычно я работаю в субботу, но сегодня у меня "
            "выходной. Утром я гуляю с сестрой, а вечером мы идём в кино». "
            "Что необычного в сегодняшнем дне автора?"
        ),
        options=[
            "Он работает вечером.",
            "Ему не нужно работать.",
            "Сестра идёт в кино одна.",
            "Он гуляет ночью.",
        ],
        correct="Ему не нужно работать.",
    ),
    AssessmentQuestion(
        id="ru-r-a1-003",
        skill="reading",
        difficulty="A1",
        question=(
            "Прочитайте сообщение: «Маша, встречаемся у музея в три часа. "
            "Урок заканчивается в два. До музея идти десять минут. Не спеши! Ира». "
            "Что Маша может понять из сообщения?"
        ),
        options=[
            "На дорогу до музея нужен час.",
            "Ира ждёт её у музея в два часа.",
            "После урока есть время на отдых.",
            "Урок заканчивается после встречи.",
        ],
        correct="После урока есть время на отдых.",
    ),
    AssessmentQuestion(
        id="ru-r-a1-004",
        skill="reading",
        difficulty="A1",
        question=(
            "Прочитайте: «Вчера Анна была в музее, а Иван работал дома. "
            "Завтра они вместе будут гулять в парке. После прогулки Иван будет читать, "
            "а Анна — слушать музыку». Что они планируют делать вместе?"
        ),
        options=[
            "Проводить время на улице.",
            "Работать дома.",
            "Читать одну книгу.",
            "Слушать песни.",
        ],
        correct="Проводить время на улице.",
    ),
]
