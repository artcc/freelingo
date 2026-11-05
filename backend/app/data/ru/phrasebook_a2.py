"""Russian A2 phrases for everyday interaction and communication repair."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="ru_housing_requests_a2",
        level="A2",
        situation="В квартире и у соседей",
        icon="🏠",
        phrases=[
            PhrasebookEntry(
                "У вас есть запасной ключ от квартиры?",
                "Уточнить у хозяина жилья, где взять дополнительный ключ.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "В ванной нет горячей воды.",
                "Сообщить хозяину о бытовой проблеме.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Сколько стоит эта квартира в месяц?",
                "Узнать стоимость аренды.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Я ваш новый сосед, меня зовут Антон.",
                "Представиться при первом разговоре в подъезде.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Это ключи моей сестры.",
                "Объяснить, кому принадлежит найденная вещь.",
                "neutral",
                "a2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru_buying_a2",
        level="A2",
        situation="Выбор и оплата покупки",
        icon="🛍️",
        phrases=[
            PhrasebookEntry(
                "У вас есть эта куртка другого размера?",
                "Найти подходящую одежду в магазине.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Мне нужно полкилограмма яблок.",
                "Назвать количество продукта на рынке.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Где здесь примерочная?",
                "Узнать, где можно проверить размер одежды.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Можно оплатить картой?",
                "Уточнить способ оплаты на кассе.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Я хочу обменять эту рубашку. Вот чек.",
                "Обратиться в магазин после покупки неподходящей вещи.",
                "neutral",
                "a2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru_medical_help_a2",
        level="A2",
        situation="У врача и в аптеке",
        icon="🩺",
        phrases=[
            PhrasebookEntry(
                "Мне нужно записаться к врачу.",
                "Обратиться в регистратуру поликлиники.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "У меня второй день болит горло.",
                "Назвать симптом и его длительность.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "У меня аллергия на это лекарство.",
                "Сообщить врачу важную информацию до назначения лечения.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Как часто нужно принимать эти таблетки?",
                "Уточнить у специалиста порядок приёма назначенного лекарства.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Мне плохо. Вы можете вызвать помощь?",
                "Попросить другого человека о помощи при плохом самочувствии.",
                "neutral",
                "a2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru_daily_updates_a2",
        level="A2",
        situation="Рассказываем о делах",
        icon="📝",
        phrases=[
            PhrasebookEntry(
                "Вчера весь вечер я занимался русским языком.",
                "Рассказать о занятии в течение вечера.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Я уже приготовила ужин. Можно есть.",
                "Сообщить дома о готовом результате.",
                "informal",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Завтра я буду работать дома.",
                "Рассказать коллеге о плане на следующий день.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Вечером я напишу тебе адрес.",
                "Пообещать знакомому нужную информацию.",
                "informal",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Я ещё собираюсь, буду готов через десять минут.",
                "Объяснить знакомому, сколько времени нужно до выхода.",
                "informal",
                "a2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru_travel_help_a2",
        level="A2",
        situation="В дороге",
        icon="🚋",
        phrases=[
            PhrasebookEntry(
                "Этот автобус идёт до вокзала?",
                "Проверить маршрут автобуса перед посадкой.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Мне нужно делать пересадку?",
                "Уточнить, можно ли доехать до нужного места без перехода на другой автобус, поезд или другой транспорт.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Сколько времени идти отсюда пешком?",
                "Оценить длительность пути без транспорта.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Обычно я езжу на метро, а сегодня иду пешком.",
                "Сравнить привычный маршрут с сегодняшним способом передвижения.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Мне нужен билет туда и обратно.",
                "Уточнить вид билета в кассе.",
                "neutral",
                "a2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru_arrangements_a2",
        level="A2",
        situation="Встречи и просьбы",
        icon="📅",
        phrases=[
            PhrasebookEntry(
                "Вам удобно встретиться третьего апреля?",
                "Вежливо предложить дату встречи.",
                "formal",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Давайте перенесём встречу на пятницу.",
                "Предложить другой день вместо назначенного.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Повторите, пожалуйста, время приёма.",
                "Попросить уточнить плохо расслышанную информацию.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Не забудь взять паспорт.",
                "Напомнить знакомому о нужном документе.",
                "informal",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Я опаздываю на десять минут. Извините.",
                "Предупредить собеседника о задержке.",
                "neutral",
                "a2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru_leisure_choices_a2",
        level="A2",
        situation="Совместный отдых",
        icon="🎭",
        phrases=[
            PhrasebookEntry(
                "Этот парк ближе, чем другой.",
                "Сравнить два места для прогулки.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Мне кажется, что этот фильм интереснее.",
                "Предложить свой вариант совместного просмотра.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Давай выберем это кафе, потому что там тише.",
                "Объяснить другу выбор места для разговора.",
                "informal",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Когда закончишь работу, позвони мне.",
                "Договориться с другом о звонке перед встречей.",
                "informal",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Что тебе больше понравилось на выставке?",
                "Спросить знакомого о впечатлениях после посещения выставки.",
                "informal",
                "a2-unit-7",
            ),
        ],
    ),
    PhrasebookCategory(
        id="ru_everyday_repair_a2",
        level="A2",
        situation="Уточняем и решаем проблему",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                "Я правильно понял: встреча завтра в шесть?",
                "Проверить дату и время после разговора.",
                "neutral",
                "a2-unit-8",
            ),
            PhrasebookEntry(
                "Напишите адрес, пожалуйста. Я плохо расслышал.",
                "Попросить письменную информацию после неясного ответа.",
                "neutral",
                "a2-unit-8",
            ),
            PhrasebookEntry(
                "Я купила билет, но выбрала другую дату. Можно его обменять?",
                "Объяснить ошибку при покупке и попросить конкретное решение.",
                "neutral",
                "a2-unit-8",
            ),
            PhrasebookEntry(
                "Сегодня я не могу, потому что работаю. Давайте завтра.",
                "Отклонить предложение и предложить доступный день.",
                "neutral",
                "a2-unit-8",
            ),
            PhrasebookEntry(
                "Спасибо, теперь я понимаю, что нужно сделать.",
                "Подтвердить, что объяснение помогло разобраться в ситуации.",
                "neutral",
                "a2-unit-8",
            ),
        ],
    ),
]
