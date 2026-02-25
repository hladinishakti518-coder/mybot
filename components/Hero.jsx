import Image from 'next/image'

export default function Hero() {
  return (
    <section className="py-16 md:py-24 lg:py-32">
      <div className="bg-surface-blue rounded-3xl md:rounded-4xl p-8 md:p-12 lg:p-16 relative overflow-hidden shadow-soft">
        <div className="grid lg:grid-cols-2 gap-10 lg:gap-16 items-center">
          <div className="relative z-10">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-serif font-semibold text-gray-900 leading-tight mb-6">
              VERA YOGA: PRO тазовое дно
            </h1>
            <p className="text-xl md:text-2xl lg:text-3xl font-semibold text-gray-800 mb-10 leading-relaxed">
              Комплексная терапия мышц тазового дна: от восстановления тонуса до коррекции опущения матки без изнурительных нагрузок за 30 дней
            </p>
            <div className="flex flex-col sm:flex-row sm:items-center gap-5">
              <div className="flex items-baseline gap-2">
                <span className="text-gray-700">Цена участия от </span>
                <span className="text-3xl md:text-4xl font-bold text-gray-900">4 990 ₽</span>
              </div>
              <a
                href={process.env.NEXT_PUBLIC_BOT_LINK || '#cta'}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center px-8 py-4 rounded-2xl font-semibold text-white bg-brand hover:bg-brand-dark transition-all shadow-soft hover:shadow-card text-base md:text-lg"
              >
                Начать восстановление
              </a>
            </div>
          </div>
          <div className="relative w-full aspect-square max-w-md mx-auto lg:max-w-none">
            <div className="absolute inset-0 rounded-full bg-gradient-to-br from-brand-light/30 to-transparent blur-3xl" />
            <Image
              src="/images/hero.png"
              alt="Женщина выполняет упражнения для тазового дна"
              fill
              className="object-cover rounded-3xl shadow-card"
              priority
            />
          </div>
        </div>
      </div>
    </section>
  )
}
