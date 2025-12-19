import { Smile, Zap, Star, Share2 } from "lucide-react";
import { Button } from "@/components/ui/button";

const features = [
  {
    icon: Smile,
    title: "AI Emotion Detection",
    description: "Detects happiness, nostalgia, excitement, love & more.",
    color: "bg-pink/10",
    iconColor: "text-pink",
  },
  {
    icon: Zap,
    title: "Instant Collage Generator",
    description: "Smart layouts created in seconds.",
    color: "bg-yellow/30",
    iconColor: "text-foreground",
  },
  {
    icon: Star,
    title: "Smart Photo Selection",
    description: "Picks your best photos automatically.",
    color: "bg-peach/40",
    iconColor: "text-foreground",
  },
  {
    icon: Share2,
    title: "One-Tap Share Anywhere",
    description: "Share to Instagram, WhatsApp, Facebook.",
    color: "bg-pink/10",
    iconColor: "text-pink",
  },
];

const FeaturesSection = () => {
  return (
    <section id="features" className="py-24 bg-background">
      <div className="container mx-auto px-6">
        {/* Section Header */}
        <div className="max-w-2xl mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
            Our services
          </h2>
          <p className="text-lg text-muted-foreground">
            We focus on the details that are really important for making each of our 
            decisions, constantly testing, configuring and optimizing processes.
          </p>
          <Button variant="outline" className="mt-6">
            Learn more
          </Button>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 gap-6">
          {features.map((feature, index) => (
            <div
              key={feature.title}
              className="group bg-card rounded-2xl border border-card-border p-8 card-hover cursor-pointer shadow-card hover:shadow-hover"
            >
              <div className="flex items-start gap-6">
                <div className={`w-14 h-14 rounded-2xl ${feature.color} flex items-center justify-center flex-shrink-0`}>
                  <feature.icon className={`w-7 h-7 ${feature.iconColor}`} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-foreground mb-2 group-hover:text-pink transition-colors">
                    {feature.title}
                  </h3>
                  <p className="text-muted-foreground">
                    {feature.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
