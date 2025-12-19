import { Play, Heart, Baby, Camera, Brain, Sparkles } from "lucide-react";

const viralFeatures = [
  {
    icon: Play,
    title: "Your Year in Emotions",
    description: "Auto-generated cinematic video of your most emotional moments.",
  },
  {
    icon: Heart,
    title: "Couple Compatibility Collage",
    description: "See how your emotions align with your partner's memories.",
  },
  {
    icon: Baby,
    title: "Baby Month-by-Month",
    description: "Track growth and emotions through beautiful memory grids.",
  },
  {
    icon: Camera,
    title: "Wedding Storybook Creator",
    description: "Turn wedding photos into a cinematic emotion journey.",
  },
  {
    icon: Brain,
    title: "AI Personality Scanner",
    description: "Discover your emotional personality from your photos.",
  },
  {
    icon: Sparkles,
    title: "Dreamscape Fantasy Collage",
    description: "Transform photos into magical fantasy art collages.",
  },
];

const ViralFeaturesSection = () => {
  return (
    <section className="py-24 bg-foreground">
      <div className="container mx-auto px-6">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-background mb-4">
            Viral Features That Make Us Stand Out
          </h2>
          <p className="text-lg text-background/70 max-w-2xl mx-auto">
            Unique AI-powered features designed to make your memories go viral.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {viralFeatures.map((feature) => (
            <div
              key={feature.title}
              className="group bg-background/5 border border-background/10 rounded-2xl p-6 card-hover hover:bg-background/10 cursor-pointer"
            >
              <div className="w-12 h-12 rounded-xl bg-pink/20 flex items-center justify-center mb-4">
                <feature.icon className="w-6 h-6 text-pink" />
              </div>
              <h3 className="text-lg font-bold text-background mb-2 group-hover:text-pink transition-colors">
                {feature.title}
              </h3>
              <p className="text-background/60 text-sm">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ViralFeaturesSection;
