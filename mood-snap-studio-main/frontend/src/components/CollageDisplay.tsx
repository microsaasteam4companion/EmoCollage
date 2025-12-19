import { Button } from "@/components/ui/button";
import { Download, RefreshCw, Sparkles } from "lucide-react";
import { useRef, useState } from "react";
import { EmotionAnalysis } from "@/types/collage";

interface CollageDisplayProps {
  photos: string[];
  analysis: EmotionAnalysis;
  onReset: () => void;
}

const CollageDisplay = ({ photos, analysis, onReset }: CollageDisplayProps) => {
  const collageRef = useRef<HTMLDivElement>(null);
  const [isDownloading, setIsDownloading] = useState(false);

  const downloadCollage = async () => {
    if (!collageRef.current) return;
    setIsDownloading(true);

    try {
      // The collage is already a complete image from the backend
      // Just download it directly
      const collageImage = photos[0]; // Backend returns the collage as first "photo"

      const link = document.createElement("a");
      link.download = `mood-snap-${analysis.dominantEmotion.toLowerCase().replace(/\s+/g, "-")}.png`;
      link.href = collageImage;
      link.click();
    } catch (err) {
      console.error("Download error:", err);
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-background/95 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-card rounded-3xl shadow-2xl max-w-6xl w-full max-h-[95vh] overflow-auto p-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
          <div>
            <h2 className="text-xl font-bold text-foreground flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-pink" />
              Your Collage
            </h2>
            <p className="text-sm text-muted-foreground mt-1">
              AI Detected: <span className="font-medium text-foreground">{analysis?.dominantEmotion || "Detected"}</span> • Style: <span className="capitalize">{analysis?.collageStyle || "Magazine"}</span>
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={onReset}>
              <RefreshCw className="w-4 h-4 mr-2" />
              Start Over
            </Button>
            <Button variant="hero" size="sm" onClick={downloadCollage} disabled={isDownloading}>
              <Download className="w-4 h-4 mr-2" />
              {isDownloading ? "Saving..." : "Download"}
            </Button>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          {analysis?.emotions?.slice(0, 5).map((emotion, index) => (
            <span
              key={index}
              className="px-3 py-1 rounded-full text-xs font-medium"
              style={{
                backgroundColor: (analysis?.colorPalette?.[index % (analysis.colorPalette?.length || 1)] || "#000") + "30",
                color: analysis?.colorPalette?.[index % (analysis.colorPalette?.length || 1)] || "#000",
                border: `1px solid ${(analysis?.colorPalette?.[index % (analysis.colorPalette?.length || 1)] || "#000")}40`,
              }}
            >
              {emotion}
            </span>
          ))}
        </div>

        {/* Display the backend-generated collage */}
        <div
          ref={collageRef}
          className="relative w-full rounded-2xl overflow-hidden shadow-2xl bg-gray-100"
        >
          <img
            src={photos[0]}
            alt="Generated Collage"
            className="w-full h-auto"
            style={{ maxHeight: '70vh', objectFit: 'contain' }}
          />
        </div>

        <div className="flex items-center gap-3 mt-4">
          <span className="text-xs text-muted-foreground">Palette:</span>
          <div className="flex gap-1.5">
            {analysis?.colorPalette?.map((color, index) => (
              <div
                key={index}
                className="w-6 h-6 rounded-full border-2 border-white shadow-sm"
                style={{ backgroundColor: color }}
                title={color}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CollageDisplay;