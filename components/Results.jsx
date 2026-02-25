const transformations = [
  {
    phase: 'До курса',
    items: [
      'Живот выпирает даже при нормальном весе, пресс «не чувствуется» после обычных упражнений.',
      'Поясница или таз ноют после тренировок, долго сидеть или стоять некомфортно.',
      'Есть стеснение из-за недержания, дискомфорта или ощущения «что что-то не так».',
      'Дыхание сбивается при нагрузке, кор не включается осознанно.',
    ],
  },
  {
    phase: 'После курса',
    items: [
      'Живот подтягивается за счёт работы глубоких мышц и тазового дна, а не только кубиков.',
      'Спина и таз стабильнее: меньше болей, проще держать осанку в быту и на тренировках.',
      'Самочувствие «по-женски» улучшается: меньше дискомфорта, больше контроля и уверенности.',
      'Дыхание и кор работают согласованно — нагрузка переносится легче, движения точнее.',
    ],
  },
]

const testimonial = {
  quote:
    'Считаю великолепным ваш 360° подход к женскому организму! Я честно не верила, что что-то изменится за такой срок — но живот реально подтянулся, а главное, ушла эта постоянная тяжесть и неуверенность. Теперь понимаю, почему раньше „просто пресс" не помогал.',
  author: 'Участница курса «VERA YOGA: PRO тазовое дно»',
}

export default function Results() {
  return (
    <section id="results" className="py-16 md:py-24">
      <div className="relative mb-12 text-center">
        <h2 className="relative text-3xl md:text-4xl lg:text-5xl font-serif font-semibold text-gray-900">
          Ваши результаты после курса
        </h2>
      </div>

      <div className="grid md:grid-cols-2 gap-6 md:gap-8 mb-12">
        {transformations.map((block, idx) => (
          <div
            key={block.phase}
            className="rounded-3xl bg-white border border-gray-100 p-8 md:p-10 shadow-soft"
          >
            <h3 className="text-xl md:text-2xl font-serif font-semibold text-gray-900 mb-6 flex items-center gap-3">
              <span
                className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold ${
                  block.phase === 'До курса'
                    ? 'bg-gray-200 text-gray-600'
                    : 'bg-brand/10 text-brand'
                }`}
              >
                {idx + 1}
              </span>
              {block.phase}
            </h3>
            <ul className="space-y-4">
              {block.items.map((item) => (
                <li key={item} className="flex gap-3 text-gray-700 text-base leading-relaxed">
                  <span className="text-brand mt-0.5 font-bold">—</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <blockquote className="rounded-3xl md:rounded-4xl bg-surface-blue p-8 md:p-12 shadow-soft">
        <p className="text-gray-700 text-lg md:text-xl leading-relaxed italic mb-6">
          «{testimonial.quote}»
        </p>
        <footer className="text-gray-600 font-medium">
          — {testimonial.author}
        </footer>
      </blockquote>
    </section>
  )
}
