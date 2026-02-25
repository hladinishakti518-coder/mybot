'use client'

import { useState } from 'react'
import Image from 'next/image'

const testimonials = [
  {
    name: 'Соня Березкина',
    text: 'У меня трое малышей: 4 г, 2 г и 4 мес. Первый раз я восстанавливалась после родов и первый раз чувствую эти роскошные мышцы тазового дна. Роды были хорошими, без разрывов, но организму всё равно нужно было восстановление. У меня чувство, что я восстановилась после всех трёх родов за раз!',
    photo: '/images/testimonial-woman-1.jpg',
  },
  {
    name: 'Леся',
    text: 'Девочки, не верю просто. Считаю днями и понимаю, что прогресс реальный. 17 октября будет 5 месяцев с родов, четыре месяца были с диким ужасным геморроем с кровотечением и болью. Сейчас всё заново — курс помог мне по-настоящему.',
    photo: '/images/testimonial-woman-2.jpg',
  },
  {
    name: 'Ева Вуколова',
    text: 'Кстати, я тоже заметила, что подтекание после родов прошло и интимная жизнь наладилась, перестала быть болезненной.',
    photo: '/images/testimonial-woman-3.jpg',
  },
]

export default function Testimonials() {
  const [current, setCurrent] = useState(0)

  const prev = () => setCurrent((c) => (c === 0 ? testimonials.length - 1 : c - 1))
  const next = () => setCurrent((c) => (c === testimonials.length - 1 ? 0 : c + 1))

  return (
    <section className="py-16 md:py-24">
      <h2 className="text-3xl md:text-4xl lg:text-5xl font-serif font-semibold text-gray-900 mb-10 md:mb-16 text-center">
        Отзывы участниц прошлого потока
      </h2>
      <div className="relative max-w-4xl mx-auto">
        <div className="flex items-center justify-center gap-4 mb-6">
          <button
            type="button"
            onClick={prev}
            className="w-12 h-12 rounded-full bg-surface-pink hover:bg-surface-peach transition flex items-center justify-center text-gray-900 shadow-soft"
            aria-label="Предыдущий отзыв"
          >
            ←
          </button>
          <button
            type="button"
            onClick={next}
            className="w-12 h-12 rounded-full bg-surface-pink hover:bg-surface-peach transition flex items-center justify-center text-gray-900 shadow-soft"
            aria-label="Следующий отзыв"
          >
            →
          </button>
        </div>
        <div className="bg-surface-lavender rounded-3xl md:rounded-4xl p-8 md:p-12 shadow-soft min-h-[400px] flex flex-col items-center justify-center text-center">
          <div className="relative w-20 h-20 rounded-full overflow-hidden mb-6 ring-4 ring-white shadow-card">
            <Image
              src={testimonials[current].photo}
              alt={testimonials[current].name}
              fill
              className="object-cover"
            />
          </div>
          <p className="text-base md:text-lg text-gray-700 leading-relaxed italic mb-6 max-w-2xl">
            «{testimonials[current].text}»
          </p>
          <footer className="font-semibold text-gray-900">
            {testimonials[current].name}
          </footer>
        </div>
        <div className="flex justify-center gap-2 mt-6">
          {testimonials.map((_, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => setCurrent(idx)}
              className={`w-2 h-2 rounded-full transition ${
                idx === current ? 'bg-brand w-6' : 'bg-gray-300'
              }`}
              aria-label={`Перейти к отзыву ${idx + 1}`}
            />
          ))}
        </div>
      </div>
    </section>
  )
}
