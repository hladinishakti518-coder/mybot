export default function Header() {
  return (
    <header className="sticky top-0 z-40 bg-white border-b border-gray-100 backdrop-blur-sm bg-white/95">
      <div className="max-w-7xl mx-auto px-4 md:px-6 flex items-center justify-between h-16 md:h-20">
        <a href="/" className="font-serif text-xl md:text-2xl font-semibold text-gray-900">
          SABIN TAG
        </a>
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium">
          <a href="#about" className="text-gray-700 hover:text-gray-900 transition">О программе</a>
          <a href="#course" className="text-gray-700 hover:text-gray-900 transition">Курс</a>
          <a href="#contacts" className="text-gray-700 hover:text-gray-900 transition">Контакты</a>
        </nav>
        <a href="tel:88003501489" className="text-sm font-medium text-gray-900 whitespace-nowrap">
          8 800 350-14-89
        </a>
      </div>
    </header>
  )
}
