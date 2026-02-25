const cards = [
  {
    icon: '🕐',
    title: 'До 20 минут в день',
    text: 'Короткие ежедневные тренировки, привычка к активности.',
  },
  {
    icon: '🏋',
    title: 'Силовые тренировки',
    text: 'Пресс, внутренняя поверхность бедра, ягодицы, кор.',
  },
  {
    icon: '〰️',
    title: 'Дыхание',
    text: 'Правильное дыхание и работа глубоких мышц.',
  },
  {
    icon: '↻',
    title: 'Подвижность позвоночника',
    text: 'Комплексы для спины и координации.',
  },
]

export default function CourseCards() {
  return (
    <section id="course" className="py-16 md:py-24">
      <h2 className="text-3xl md:text-4xl lg:text-5xl font-serif font-semibold text-gray-900 mb-10 md:mb-16 text-center">
        Программа курса
      </h2>
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 md:gap-6">
        {cards.map((card) => (
          <article
            key={card.title}
            className="p-6 md:p-8 rounded-3xl bg-white border border-gray-100 shadow-soft hover:shadow-card transition-shadow"
          >
            <div className="w-14 h-14 rounded-2xl bg-brand/10 flex items-center justify-center text-brand mb-5 text-2xl">
              {card.icon}
            </div>
            <h3 className="font-serif text-lg md:text-xl font-semibold text-gray-900 mb-3">
              {card.title}
            </h3>
            <p className="text-sm md:text-base text-gray-600 leading-relaxed">{card.text}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
