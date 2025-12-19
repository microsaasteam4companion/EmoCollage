import { useState } from "react";
import { Button } from "@/components/ui/button";
import PhotoUploader from "./PhotoUploader";

const HeroSection = () => {
  const [showUploader, setShowUploader] = useState(false);

  return (
    <>
      <section className="relative min-h-[70vh] pt-24 overflow-hidden">
        {/* Gradient Background */}
        <div className="absolute inset-0 gradient-hero opacity-40" />
        
        <div className="container mx-auto px-6 py-24 relative z-10">
          <div className="flex flex-col items-center justify-center text-center min-h-[50vh]">
            <div className="space-y-8 max-w-3xl">
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-foreground leading-[1.1] tracking-tight">
                Instant Collages Powered by Your{" "}
                <span className="text-pink">Emotions</span>
              </h1>
              
              <p className="text-xl text-muted-foreground leading-relaxed">
                Upload photos → AI detects emotions → creates a mood collage instantly.
              </p>
              
              <p className="text-base text-muted-foreground">
                Turn memories into aesthetic collages using emotion-aware AI.
              </p>

              <div className="flex flex-wrap justify-center gap-4 pt-4">
                <Button variant="hero" size="lg" onClick={() => setShowUploader(true)}>
                  Upload Photos
                </Button>
                <Button variant="hero-ghost" size="lg">
                  Try Demo
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {showUploader && <PhotoUploader />}
    </>
  );
};

export default HeroSection;
