# Контент курсов

Здесь хранятся материалы курсов для бота и лендинга.

## Структура курса

```
course_<slug>/
├── schedule.json    # Расписание выдачи уроков (день → урок)
├── description.md   # Описание для лендинга и бота
├── lessons/         # Файлы уроков или ссылки (видео, PDF)
└── homework/        # Тексты заданий по урокам
```

## schedule.json

Формат:

```json
{
  "course_id": "tazovoe_dno",
  "course_name": "Название курса",
  "duration_days": 21,
  "lessons": [
    {
      "day": 1,
      "lesson_id": "lesson_01",
      "title": "Название урока",
      "type": "video",
      "url": "https://...",
      "description": "Краткое описание"
    }
  ]
}
```
