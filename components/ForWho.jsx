export default function ForWho() {
  const items = [
    {
      title: 'Подтянутый живот',
      text: 'Комплексная работа с дыханием и тазовым дном, а не только пресс.',
      emoji: '🧘‍♀️',
      bg: 'bg-surface-pink',
    },
    {
      title: 'Укрепление тазового дна',
      text: 'Тонус, согласованность с дыханием, улучшение самочувствия.',
      emoji: '💪',
      bg: 'bg-surface-blue',
    },
    {
      title: 'Забота о себе',
      text: 'Время на себя и привычка заниматься здоровьем.',
      emoji: '🌸',
      bg: 'bg-surface-peach',
    },
  ]

  return (
    <section id="about" className="py-16 md:py-24">
      <h2 className="text-3xl md:text-4xl lg:text-5xl font-serif font-semibold text-gray-900 mb-10 md:mb-16 text-center">
        Результат который вы получите за 30 дней
      </h2>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
        {items.map((item) => (
          <div
            key={item.title}
            className="p-0 rounded-3xl bg-white border border-gray-100 shadow-soft hover:shadow-card transition-shadow overflow-hidden"
          >
            <div className={`w-full aspect-[400/280] ${item.bg} flex items-center justify-center`}>
              <span className="text-7xl">{item.emoji}</span>
            </div>
            <div className="p-8 md:p-10">
              <h3 className="font-serif text-xl md:text-2xl font-semibold text-gray-900 mb-3">{item.title}</h3>
              <p className="text-base text-gray-600 leading-relaxed">{item.text}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
