import Header from '@/components/Header'
import Hero from '@/components/Hero'
import ForWho from '@/components/ForWho'
import WhyClassicWorkouts from '@/components/WhyClassicWorkouts'
import CourseCards from '@/components/CourseCards'
import Results from '@/components/Results'
import Testimonials from '@/components/Testimonials'
import OfferStrip from '@/components/OfferStrip'
import CtaFixed from '@/components/CtaFixed'

export default function Home() {
  return (
    <>
      <Header />
      <main className="max-w-7xl mx-auto px-4 md:px-6">
        <Hero />
        <ForWho />
        <WhyClassicWorkouts />
        <CourseCards />
        <Results />
        <Testimonials />
        <OfferStrip />
      </main>
      <CtaFixed />
    </>
  )
}
