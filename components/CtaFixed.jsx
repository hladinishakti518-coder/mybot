export default function CtaFixed() {
  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 md:hidden p-4 bg-white border-t border-gray-200 shadow-[0_-8px_30px_rgba(0,0,0,0.12)] backdrop-blur-sm bg-white/95">
      <a
        href={process.env.NEXT_PUBLIC_BOT_LINK || '#cta'}
        target="_blank"
        rel="noopener noreferrer"
        className="block w-full py-4 rounded-2xl font-semibold text-center text-white bg-brand shadow-soft"
      >
        Начать восстановление — 4 990 ₽
      </a>
    </div>
  )
}
