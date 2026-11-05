"""Russian A1 phrasebook: short, reusable exchanges in everyday situations."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="ru-greetings_a1",
        level="A1",
        situation="Знакомство и приветствие",
        icon="👋",
        phrases=[
            PhrasebookEntry(
                "Здравствуйте!",
                "Вежливое приветствие взрослому или группе людей.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Привет!",
                "Приветствие другу или человеку, с которым вы на ты.",
                "informal",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Меня зовут Анна.",
                "Назвать своё имя; вместо Анна скажите своё имя.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Как вас зовут?",
                "Узнать имя нового взрослого собеседника на вы.",
                "formal",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Очень приятно.",
                "Короткий ответ после знакомства.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "До свидания!",
                "Вежливо попрощаться после урока или встречи.",
                "neutral",
                "a1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru-understanding_a1",
        level="A1",
        situation="Когда трудно понять",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                "Повторите, пожалуйста.",
                "Попросить ещё раз произнести слово или фразу.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Говорите, пожалуйста, медленнее.",
                "Попросить собеседника снизить скорость речи.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Я пока плохо говорю по-русски.",
                "Объяснить, что вы только начинаете учить язык.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Что значит это слово?",
                "Уточнить значение незнакомого слова.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Как это пишется?",
                "Узнать написание имени или слова.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Напишите, пожалуйста.",
                "Попросить записать адрес, имя или другое сообщение.",
                "neutral",
                "a1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru-family-things_a1",
        level="A1",
        situation="Люди и личные вещи",
        icon="🏠",
        phrases=[
            PhrasebookEntry(
                "Это моя семья.",
                "Показать близких людей на фотографии.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "А это мой брат.",
                "Продолжить знакомить собеседника с членами семьи.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Кто это на фотографии?",
                "Спросить о незнакомом человеке на снимке.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Это ваш телефон?",
                "Уточнить владельца найденного телефона, обращаясь на вы.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Нет, это не моё.",
                "Ответить, что показанная вещь вам не принадлежит.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Спасибо за помощь.",
                "Поблагодарить человека, который помог найти вещь.",
                "neutral",
                "a1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru-daily-time_a1",
        level="A1",
        situation="День и расписание",
        icon="🕒",
        phrases=[
            PhrasebookEntry(
                "Который час?",
                "Узнать текущее время.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Во сколько начинается урок?",
                "Уточнить время начала занятия.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Урок в пять часов.",
                "Сообщить время занятия в целых часах.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Сегодня я не работаю.",
                "Сообщить, что сегодня нет рабочих обязанностей.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Что ты сейчас делаешь?",
                "Спросить друга о его занятии в этот момент.",
                "informal",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Вечером я обычно отдыхаю.",
                "Коротко рассказать о привычном распорядке дня.",
                "neutral",
                "a1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru-cafe-shopping_a1",
        level="A1",
        situation="В кафе и у кассы",
        icon="☕",
        phrases=[
            PhrasebookEntry(
                "Мне, пожалуйста, чай без сахара.",
                "Заказать напиток; фразу можно учить целиком.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "У вас есть суп?",
                "Проверить наличие блюда перед заказом.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Я не ем мясо.",
                "Сообщить о своём питании при выборе блюда.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Сколько это стоит?",
                "Узнать цену выбранного продукта или вещи.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Можно оплатить картой?",
                "Уточнить, принимают ли банковскую карту.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Счёт, пожалуйста.",
                "Попросить сумму к оплате после еды в кафе.",
                "neutral",
                "a1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru-city-help_a1",
        level="A1",
        situation="Дорога и помощь в городе",
        icon="🧭",
        phrases=[
            PhrasebookEntry(
                "Извините, где здесь метро?",
                "Вежливо остановить прохожего и спросить дорогу.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Это далеко?",
                "Уточнить расстояние до нужного места.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Идите прямо, потом направо.",
                "Дать простое указание человеку на вы.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Этот автобус идёт в центр?",
                "Проверить маршрут перед посадкой.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Мне нужна помощь.",
                "Коротко сообщить прохожему или сотруднику, что нужна поддержка.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Вызовите скорую, пожалуйста.",
                "Попросить другого человека вызвать медицинскую помощь.",
                "neutral",
                "a1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru-meeting_a1",
        level="A1",
        situation="Интересы и приглашения",
        icon="🎬",
        phrases=[
            PhrasebookEntry(
                "Мне двадцать пять лет.",
                "Назвать свой возраст в разговоре о себе.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Тебе нравится эта музыка?",
                "Узнать мнение друга о том, что вы слушаете.",
                "informal",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Пойдём в кино?",
                "Пригласить друга; готовая форма приглашения.",
                "informal",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Да, с удовольствием!",
                "Принять приглашение и показать интерес.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Спасибо, но сегодня не могу.",
                "Вежливо отказаться от встречи сегодня.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Где и во сколько встречаемся?",
                "Уточнить место и время уже согласованной встречи.",
                "neutral",
                "a1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru-trip_a1",
        level="A1",
        situation="Билеты, гостиница и планы",
        icon="🧳",
        phrases=[
            PhrasebookEntry(
                "Один билет до Казани, пожалуйста.",
                "Купить билет. После до нужен родительный падеж: Казань — до Казани, "
                "Москва — до Москвы, Санкт-Петербург — до Санкт-Петербурга. "
                "Готовые варианты: один билет до Москвы; один билет до Санкт-Петербурга.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Когда отправляется поезд?",
                "Уточнить время отправления перед поездкой.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "У меня есть бронь.",
                "Сообщить сотруднику гостиницы о предварительном заказе номера.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Во сколько завтрак?",
                "Уточнить время еды в гостинице.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Вчера мы были в музее.",
                "Рассказать об одном месте, которое вы посетили вместе.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Завтра я буду гулять по городу.",
                "Сообщить простой план на следующий день.",
                "neutral",
                "a1-unit-7",
            ),
        ],
    ),
]
