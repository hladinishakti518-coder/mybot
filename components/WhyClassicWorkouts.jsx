export default function WhyClassicWorkouts() {
  const pains = [
    'Выпирающий «беременный» живот, который не уходит от скручиваний и планки',
    'Недержание, частые воспаления, опущение органов, дискомфорт «оттуда»',
    'Боли в пояснице и тазу, которые усиливаются после обычного фитнеса',
    'Отёчность лица и дряблость бёдер при внешне «нормальном» весе',
    'Желание восстановиться после родов, но страх навредить себе нагрузками',
    'Сутулость, слабый кор и неготовность тела к нагрузкам без боли',
  ]

  return (
    <section id="why-not-classic" className="py-16 md:py-24">
      <div className="relative mb-12">
        <h2 className="relative text-3xl md:text-4xl lg:text-5xl font-serif font-semibold text-gray-900 text-center">
          Почему классические тренировки не работают
        </h2>
      </div>
      <div className="relative rounded-3xl md:rounded-4xl bg-surface-peach p-8 md:p-12 lg:p-16 shadow-soft">
        <p className="text-gray-700 text-lg md:text-xl leading-relaxed mb-8 max-w-4xl">
          Классический фитнес часто бьёт по симптомам, а не по причине: качает пресс,
          но не восстанавливает глубокие мышцы и тазовое дно. В итоге нагрузка ложится
          на поверхностные мышцы, дыхание сбивается, внутрибрюшное давление растёт —
          и проблемы только закрепляются. Научный подход строится на биомеханике,
          физиологии и связи дыхания с тонусом тазового дна: сначала стабилизация и
          правильный паттерн движения, потом усиление нагрузки.
        </p>
        <p className="text-gray-800 text-base md:text-lg font-semibold mb-5">
          Знакомо ли вам что-то из этого:
        </p>
        <ul className="space-y-4 max-w-4xl">
          {pains.map((pain) => (
            <li key={pain} className="flex items-start gap-4 text-gray-700 text-base md:text-lg leading-relaxed">
              <span className="mt-1.5 w-6 h-6 rounded-full bg-accent-coral/20 flex items-center justify-center shrink-0">
                <span className="text-accent-coral text-sm font-bold">✓</span>
              </span>
              <span>{pain}</span>
            </li>
          ))}
        </ul>
        <p className="mt-10 text-gray-600 text-base md:text-lg leading-relaxed max-w-4xl">
          Если да — курс выстроен так, чтобы работать с причиной: дыхание, тазовое дно,
          кор и только затем силовые элементы. Без перегрузки и без вреда.
        </p>
      </div>
    </section>
  )
}
