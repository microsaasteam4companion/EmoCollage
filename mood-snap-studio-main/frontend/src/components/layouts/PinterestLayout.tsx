import { LayoutProps } from "@/types/collage";
import { useMemo } from "react";

// Minimal Doodles for Pinterest Style
const SparkleIcon = ({ color }: { color: string }) => (
    <svg viewBox="0 0 24 24" className="w-6 h-6" style={{ color }}>
        <path fill="currentColor" d="M12 2l2.4 7.6L22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4z" />
    </svg>
);

export const PinterestLayout = ({ photos, analysis }: LayoutProps) => {
    const offsets = useMemo(() => photos.map(() => ({
        x: Math.random() * 20 - 10,
        y: Math.random() * 20 - 10,
        rotate: Math.random() * 6 - 3,
        scale: 0.95 + Math.random() * 0.1
    })), [photos]);

    const palette = analysis?.colorPalette || ["#faf9f6", "#e5e5e5"];
    const bgColor = palette[0] + "10"; // Very subtle tint

    return (
        <div className="relative w-full h-full p-4 md:p-8 overflow-hidden flex flex-col items-center transition-all duration-1000"
            style={{ backgroundColor: palette[0] === "#ffffff" ? "#faf9f6" : bgColor }}>

            <div className="absolute inset-0 opacity-[0.03] pointer-events-none"
                style={{ backgroundImage: `url("https://www.transparenttextures.com/patterns/paper.png")` }}></div>

            <div className="relative w-full max-w-5xl h-full flex flex-col gap-6 md:gap-12 justify-center">

                {/* HERO SHOT */}
                <div className="relative self-center w-full max-w-2xl aspect-[4/5] z-10 group">
                    <div
                        className="w-full h-full bg-white p-3 shadow-[0_30px_60px_rgba(0,0,0,0.12)] transition-all duration-700 group-hover:scale-[1.01]"
                        style={{
                            transform: `translate(${offsets[0]?.x}px, ${offsets[0]?.y}px) rotate(${offsets[0]?.rotate}deg)`,
                        }}
                    >
                        <img src={photos[0]} className="w-full h-full object-cover" alt="Hero" />

                        {/* Polaroid Label (Minimal) */}
                        <div className="absolute bottom-2 right-4">
                            <span className="font-serif italic text-[10px] text-black/40 tracking-widest uppercase">
                                {analysis?.dominantEmotion}
                            </span>
                        </div>
                    </div>
                </div>

                {/* SECONDARY OVERLAP */}
                <div className="flex justify-center items-start gap-8 -mt-32 md:-mt-56 px-4">
                    {photos.slice(1, 3).map((photo, i) => (
                        <div
                            key={i}
                            className="relative w-[40%] max-w-[280px] aspect-[3/4] z-20 transition-all duration-500 hover:z-30 hover:scale-105"
                            style={{
                                marginTop: i === 0 ? '60px' : '20px',
                                transform: `translate(${offsets[i + 1]?.x}px, ${offsets[i + 1]?.y}px) rotate(${offsets[i + 1]?.rotate}deg) scale(${offsets[i + 1]?.scale})`,
                            }}
                        >
                            <div className="w-full h-full bg-white p-2 shadow-[0_20px_40px_rgba(0,0,0,0.1)]">
                                <img src={photo} className="w-full h-full object-cover" alt={`Gallery ${i}`} />
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* AESTHETIC DOODLES (The "Doodling Touch") */}
            <div className="absolute top-12 left-12 opacity-40 rotate-12">
                <SparkleIcon color={palette[1 % palette.length]} />
            </div>
            <div className="absolute bottom-24 right-16 opacity-30 -rotate-12 scale-150">
                <SparkleIcon color={palette[0 % palette.length]} />
            </div>

            {/* Color Swatches */}
            <div className="absolute bottom-6 left-6 flex gap-2 p-2 bg-white/50 backdrop-blur-sm rounded-full">
                {palette.map((c, i) => (
                    <div key={i} className="w-3 h-3 rounded-full border border-black/5 shadow-inner" style={{ backgroundColor: c }}></div>
                ))}
            </div>

            {/* Corners */}
            <div className="absolute top-6 right-6 w-16 h-16 border-t border-r border-black/5 opacity-50"></div>
            <div className="absolute bottom-6 right-6 w-16 h-16 border-b border-l border-black/5 opacity-50"></div>
        </div>
    );
};
