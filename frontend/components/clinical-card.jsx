"use client"

import { ConfidenceGauge } from "./confidence-gauge"
import { HerbalRecommendations } from "./herbal-recommendations"

export function ClinicalCard({ result }) {
  return (
    <div className="space-y-6 animate-in fade-in-0 slide-in-from-bottom-4 duration-700">
      {/* Prescription Header */}
      <div className="backdrop-blur-xl bg-card/70 border border-border rounded-2xl p-8 shadow-xl relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-forest via-sage to-forest" />
        <div className="flex items-center justify-between mb-6">
          <div>
            <p className="text-[10px] uppercase tracking-[0.2em] text-forest-light/60 mb-1">Ayurvedic Consultation</p>
            <h3 className="font-serif text-2xl font-semibold text-forest">Clinical Assessment</h3>
          </div>
          <div className="text-right">
            <p className="text-[10px] uppercase tracking-wider text-forest-light/60">Date</p>
            <p className="text-sm text-forest font-medium">{new Date().toLocaleDateString('en-US', {
              month: 'long',
              day: 'numeric',
              year: 'numeric'
            })}</p>
          </div>
        </div>
      </div>

      {/* Diagnosis Card - Now full width for better emphasis */}
      <div className="backdrop-blur-xl bg-card/60 border border-border rounded-2xl p-6 shadow-lg relative overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 bg-forest/5 rounded-bl-full" />
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div>
            <p className="text-[10px] uppercase tracking-[0.15em] text-forest-light/60 mb-2">Possible Disease Type</p>
            <h4 className="font-serif text-3xl font-bold text-forest mb-1">{result.diagnosis}</h4>
            {result.sanskritName && result.sanskritName !== result.diagnosis && (
              <p className="text-lg font-serif text-forest-light italic opacity-90">{result.sanskritName}</p>
            )}
            <p className="text-sm text-forest-light/70 leading-relaxed mt-4 max-w-xl">
              Based on your symptoms and constitution, our Machine Learning model indicates a strong correlation with this type of condition.
            </p>
          </div>
          <div className="flex-shrink-0">
            <ConfidenceGauge value={result.confidence} size={100} />
          </div>
        </div>
      </div>


      {/* Results Grid - Yoga & Diet */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Yogic Path Card */}
        <div className="backdrop-blur-xl bg-card/60 border border-border rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-full bg-sage/30 flex items-center justify-center">
              <svg className="w-4 h-4 text-forest" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <div>
              <p className="text-[10px] uppercase tracking-[0.15em] text-forest-light/60">Practice</p>
              <h4 className="font-serif text-lg font-medium text-forest">Yogic Path</h4>
            </div>
          </div>
          <ul className="space-y-3">
            {result.yogicPath.map((practice, index) => (
              <li key={index} className="flex items-start gap-3 text-sm text-forest-light">
                <span className="w-1.5 h-1.5 rounded-full bg-forest/60 mt-1.5 flex-shrink-0" />
                <span className="leading-relaxed">{practice}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Dietary Wisdom Card */}
        <div className="backdrop-blur-xl bg-card/60 border border-border rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-full bg-sage/30 flex items-center justify-center">
              <svg className="w-4 h-4 text-forest" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div>
              <p className="text-[10px] uppercase tracking-[0.15em] text-forest-light/60">Nutrition</p>
              <h4 className="font-serif text-lg font-medium text-forest">Dietary Wisdom</h4>
            </div>
          </div>
          <ul className="space-y-3">
            {result.dietaryWisdom.map((food, index) => (
              <li key={index} className="flex items-start gap-3 text-sm text-forest-light">
                <span className="w-1.5 h-1.5 rounded-full bg-forest/60 mt-1.5 flex-shrink-0" />
                <span className="leading-relaxed">{food}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* NEW: Extracted Herbal Component */}
      <HerbalRecommendations herbs={result.herbs} doshas={result.doshas} />

      {/* Footer Note */}
      <div className="backdrop-blur-xl bg-sage/20 border border-border/50 rounded-xl p-4 text-center">
        <p className="text-xs text-forest-light/70 italic">
          This assessment is powered by Advanced AI and traditional Ayurvedic principles. Please consult with a qualified practitioner for personalized guidance.
        </p>
      </div>
    </div>
  )
}
