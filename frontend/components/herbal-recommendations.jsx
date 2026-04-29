"use client"

import { Leaf, Sparkles, Droplets } from "lucide-react"

export function HerbalRecommendations({ herbs, doshas }) {
  if (!herbs || herbs.length === 0) return null;

  return (
    <div className="backdrop-blur-xl bg-gradient-to-br from-sage/20 to-parchment border border-border/80 rounded-2xl p-8 shadow-xl relative overflow-hidden group hover:shadow-2xl transition-all duration-500">
      {/* Decorative background elements */}
      <div className="absolute -right-12 -top-12 w-40 h-40 bg-sage/30 rounded-full blur-3xl group-hover:bg-sage/40 transition-all duration-500" />
      <div className="absolute -left-12 -bottom-12 w-40 h-40 bg-forest/10 rounded-full blur-3xl group-hover:bg-forest/20 transition-all duration-500" />

      <div className="relative z-10">
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-6 mb-8">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-forest/10 flex items-center justify-center border border-forest/20 shadow-inner">
              <Leaf className="w-6 h-6 text-forest drop-shadow-md" />
            </div>
            <div>
              <p className="text-[11px] uppercase tracking-[0.2em] text-forest-light/70 mb-1 font-semibold">Personalized Suggestion</p>
              <h4 className="font-serif text-2xl font-bold text-forest tracking-tight">Recommended Herbs</h4>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {herbs.map((herb, index) => (
            <div
              key={index}
              className="flex items-center gap-4 bg-card/60 hover:bg-card/90 transition-colors duration-300 p-4 rounded-xl border border-sage/30 shadow-sm group/item"
            >
              <div className="w-8 h-8 rounded-full bg-forest/5 flex items-center justify-center group-hover/item:bg-forest/10 transition-colors">
                <Sparkles className="w-4 h-4 text-forest/70" />
              </div>
              <span className="text-sm font-medium text-forest-light tracking-wide">{herb}</span>
            </div>
          ))}
        </div>

        <div className="mt-6 pt-6 border-t border-forest/10 flex items-start gap-3">
          <div className="mt-0.5">
            <svg className="w-4 h-4 text-forest-light/60" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p className="text-xs text-forest-light/70 leading-relaxed italic">
            These herbal remedies were precisely predicted by the ML model based on your specific disease and reported symptom severity, age and Gender. <b>Always consult an Ayurvedic doctor before starting new herbs</b>.
          </p>
        </div>
      </div>
    </div>
  )
}
