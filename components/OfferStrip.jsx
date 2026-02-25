export default function OfferStrip() {
  return (
    <section id="contacts" className="py-16 md:py-24">
      <div className="bg-surface-blue rounded-3xl md:rounded-4xl p-8 md:p-12 shadow-soft flex flex-col md:flex-row md:items-center md:justify-between gap-8">
        <div>
          <h2 className="text-2xl md:text-3xl lg:text-4xl font-serif font-semibold text-gray-900 mb-3">
            Запишитесь сейчас — начните в любой день
          </h2>
          <p className="text-gray-700 text-base md:text-lg">
            Курс без куратора · 4 990 ₽ / 3 недели
          </p>
        </div>
        <a
          href={process.env.NEXT_PUBLIC_BOT_LINK || '#cta'}
          id="cta"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center justify-center px-8 py-4 rounded-2xl font-semibold text-white bg-brand hover:bg-brand-dark transition-all shadow-soft hover:shadow-card shrink-0 text-center"
        >
          Начать восстановление
        </a>
      </div>
    </section>
  )
}
