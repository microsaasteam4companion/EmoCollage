
import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Upload, X, Loader2, Wand2, BookOpen, Smartphone, Layers, Brush, Camera, Images, Sparkles } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import CollageDisplay from "./CollageDisplay";
import { EmotionAnalysis } from "@/types/collage";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent } from "@/components/ui/card";

// V4: Elite Modes
const MODES = [
  { id: "pinterest", label: "Pinterest Style", icon: Sparkles, desc: "Aesthetic, text-free, layered mood boards." },
  { id: "magazine", label: "Editorial", icon: BookOpen, desc: "Clean, photo-focused spreads (Text-Free)." },
  { id: "portrait", label: "Cinematic", icon: Camera, desc: "Studio-grade lighting & framing." },
  { id: "doodle", label: "Scrapbook", icon: Brush, desc: "Washi tape & paper textures." },
];

const PhotoUploader = () => {
  const [selectedPhotos, setSelectedPhotos] = useState<string[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState<EmotionAnalysis | null>(null);

  // State
  const [activeTab, setActiveTab] = useState("magazine");
  const [userPrompt, setUserPrompt] = useState("");

  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files) return;
    Array.from(files).forEach((file) => {
      const reader = new FileReader();
      reader.onload = (e) => setSelectedPhotos((prev) => [...prev, e.target?.result as string]);
      reader.readAsDataURL(file);
    });
  };

  // Helper to compress image for faster AI analysis
  const compressImage = (dataUrl: string): Promise<Blob> => {
    return new Promise((resolve) => {
      const img = new Image();
      img.src = dataUrl;
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const maximize_size = 1024; // Resize to max 1024px (plenty for AI)
        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > maximize_size) {
            height *= maximize_size / width;
            width = maximize_size;
          }
        } else {
          if (height > maximize_size) {
            width *= maximize_size / height;
            height = maximize_size;
          }
        }

        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        ctx?.drawImage(img, 0, 0, width, height);

        canvas.toBlob((blob) => {
          if (blob) resolve(blob);
        }, 'image/jpeg', 0.8); // 80% quality JPEG
      };
    });
  };

  const analyzeAndCreateCollage = async () => {
    if (selectedPhotos.length < 1) return;
    setIsAnalyzing(true);
    try {
      const formData = new FormData();

      // Send ALL selected photos to backend
      for (let i = 0; i < selectedPhotos.length; i++) {
        const compressedBlob = await compressImage(selectedPhotos[i]);
        formData.append("files", compressedBlob, `photo${i}.jpg`);
      }

      // Pass the selected specific mode as 'theme'
      formData.append("theme", activeTab);

      // User prompt
      formData.append("user_prompt", userPrompt);

      const apiResponse = await fetch("http://localhost:8000/analyze-emotion", {
        method: "POST",
        body: formData,
      });

      if (!apiResponse.ok) throw new Error("Studio requires a reliable connection. Please try again.");

      const data = await apiResponse.json();

      // 1. UPDATE ANALYSIS
      setAnalysis(data.analysis);

      // 2. The backend now returns a complete collage image
      if (data.collage_image) {
        // Store the collage as the first "photo" for display
        setSelectedPhotos([data.collage_image]);
        toast({
          title: "Collage Created! 🎨",
          description: `${data.analysis.collageStyle} style with ${data.analysis.dominantEmotion} vibes`,
        });
      } else {
        toast({ title: "Analysis Complete", description: "Your story is ready." });
      }
    } catch (error: any) {
      console.error(error);
      toast({
        title: "Connection Error",
        description: error.message || "Make sure the Python backend is running! (Check terminal)",
        variant: "destructive"
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  if (analysis) {
    return <CollageDisplay photos={selectedPhotos} analysis={analysis} onReset={() => setAnalysis(null)} />;
  }

  return (
    <div className="fixed inset-0 bg-zinc-950 text-white z-50 flex flex-col overflow-hidden font-sans selection:bg-pink-500/30">

      {/* Studio Header */}
      <div className="h-16 border-b border-white/10 flex items-center justify-between px-8 bg-zinc-900/50 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-gradient-to-tr from-pink-500 to-violet-600 rounded-full flex items-center justify-center">
            <Wand2 className="w-4 h-4 text-white" />
          </div>
          <div>
            <h2 className="text-lg font-bold tracking-tight">MOOD SNAP STUDIO</h2>
            <p className="text-[10px] text-zinc-400 uppercase tracking-[0.2em]">Visual Storytelling Engine</p>
          </div>
        </div>
        <div className="text-xs text-zinc-500 font-mono hidden md:block">V4.0 // ELITE EDITION</div>
      </div>

      <div className="flex-1 flex overflow-hidden">

        {/* Left: Interactive Workspace */}
        <div className="flex-1 relative bg-zinc-900/30 flex flex-col items-center justify-center p-8">
          {selectedPhotos.length === 0 ? (
            <div
              onClick={() => fileInputRef.current?.click()}
              className="group relative cursor-pointer"
            >
              <div className="w-64 h-80 border border-white/10 rounded-xl flex flex-col items-center justify-center bg-zinc-900/50 hover:bg-zinc-800/50 transition-all duration-500 group-hover:scale-105 group-hover:shadow-2xl group-hover:shadow-pink-500/10">
                <Upload className="w-8 h-8 text-zinc-600 group-hover:text-pink-400 transition-colors mb-4" />
                <span className="text-sm font-medium text-zinc-400 group-hover:text-white tracking-widest uppercase">Start Project</span>
              </div>
              <div className="absolute -inset-4 border border-dashed border-white/5 rounded-2xl group-hover:border-pink-500/20 transition-colors pointer-events-none"></div>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 max-w-2xl w-full max-h-full overflow-y-auto p-4 scrollbar-hide">
              {selectedPhotos.map((p, i) => (
                <div key={i} className="aspect-[3/4] relative overflow-hidden rounded-lg group">
                  <img src={p} className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity" />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-2">
                    <span className="text-[10px] font-mono text-zinc-300">IMG_00{i + 1}.RAW</span>
                  </div>
                </div>
              ))}
              <div onClick={() => fileInputRef.current?.click()} className="aspect-[3/4] border border-dashed border-white/20 rounded-lg flex items-center justify-center cursor-pointer hover:bg-white/5 text-zinc-500 hover:text-white transition-colors">
                <Upload className="w-6 h-6" />
              </div>
            </div>
          )}
          <input ref={fileInputRef} type="file" multiple className="hidden" onChange={handleFileSelect} />
        </div>

        {/* Right: The Control Deck */}
        <div className="w-[400px] border-l border-white/10 bg-zinc-950 flex flex-col">
          <div className="p-6 border-b border-white/5">
            <h3 className="text-sm font-medium text-zinc-400 uppercase tracking-widest mb-4">Select Output Mode</h3>

            <div className="grid grid-cols-2 gap-2">
              {MODES.map((mode) => (
                <div
                  key={mode.id}
                  onClick={() => setActiveTab(mode.id)}
                  className={`p - 3 rounded - xl border cursor - pointer transition - all duration - 300 ${activeTab === mode.id
                    ? "bg-white text-black border-white shadow-lg shadow-white/5"
                    : "bg-zinc-900/50 border-white/5 text-zinc-400 hover:border-white/20 hover:text-zinc-200"
                    } `}
                >
                  <mode.icon className="w-5 h-5 mb-2" />
                  <div className="text-xs font-bold uppercase">{mode.label}</div>
                  <div className="text-[10px] opacity-60 leading-tight mt-1 truncate">{mode.desc}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="p-6 flex-1 flex flex-col gap-6">
            <div className="space-y-3">
              <label className="text-xs font-medium text-zinc-500 uppercase tracking-widest">Creative Direction</label>
              <Textarea
                placeholder="Describe the mood, lighting, and story you want to tell..."
                value={userPrompt}
                onChange={e => setUserPrompt(e.target.value)}
                className="bg-zinc-900 border-white/10 focus:border-white/30 text-sm min-h-[120px] resize-none"
              />
              <p className="text-[10px] text-zinc-600 pl-1">
                Tip: "Dark high-contrast moody editorial" or "Soft pastel dreamscape"
              </p>
            </div>

            <Button
              size="lg"
              className="mt-auto w-full h-16 bg-white text-black hover:bg-zinc-200 text-sm font-bold tracking-widest uppercase transition-all"
              onClick={analyzeAndCreateCollage}
              disabled={isAnalyzing || selectedPhotos.length === 0}
            >
              {isAnalyzing ? (
                <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Processing...</>
              ) : (
                <div className="flex flex-col items-center">
                  <span>Generate Visual Story</span>
                  <span className="text-[10px] font-normal opacity-50 capitalize">Using Gemini 1.5 Flash</span>
                </div>
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PhotoUploader;

