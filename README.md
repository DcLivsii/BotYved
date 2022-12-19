# BotYved
ФИО команды:
  Цалетов Михаил Игоревич
  Стороженко Тихон Вадимович

Основными задачами бота являются:
 1)Добавление задач
 2)Отображение информации о всех заметках
 3)Отправка уведомлений пользователю в назначеный день для напоминания
 
1.Для добавления задач создан класс Sender, с ключевыми полями:
    nameOfNoti (имя заметки)
    time (время до отправки)
    content (содержание)
    date (дата отправки)
    
Далее пользователю нужно заполнить эти поля через отправку сообщений боту. Сначала пользователь нажимает на клавишу '💬 Добавить  задачу', далее по очереди бот предоставляет возможность для заполнения полей. Порядок такой: имя заметки, содержание, дата отправки, время отправки.Реализовано заполнение через сеттеры этих полей, а для получения информации непосредственно из бота созданы методы botSetName, botSetContent, botSetTime, botSetDate. С их помощью текст сообщения, введённого пользователем, передаётся в сами сеттеры и заполняется.

2.Вывод информации о всех заметках производится после нажатия клавиши '💌 Список задач' через метод класса Sender 'getInfo', в котором через цикл выводится информация о каждой заметке в массиве задач.
В будущем задачи должны выгружаться из БД, которая будет совместной с приложением.

3)Отправка уведомлений о задаче реализована через метод sendNoti, где через ключевое поле time определяется время до отправки сообщения пользователю (вызывается метод telegram.notify с задержкой на время time). В сообщении будет отображаться имя заметки.
