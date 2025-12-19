import { LayoutProps } from "@/types/collage";
import { useMemo } from "react";

// --- SVG STICKERS ---
const StarDoodle = ({ color = "white", className }: { color?: string, className?: string }) => (
    <svg viewBox="0 0 100 100" className={className} style={{ width: '40px', height: '40px', color }}>
        <path fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"
            d="M50 5 L63 35 L95 35 L68 55 L78 85 L50 65 L22 85 L32 55 L5 35 L37 35 Z" />
    </svg>
);

const HeartDoodle = ({ color = "white", className }: { color?: string, className?: string }) => (
    <svg viewBox="0 0 100 100" className={className} style={{ width: '50px', height: '50px', color }}>
        <path fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round"
            d="M50 30 C 20 0, 0 40, 50 90 C 100 40, 80 0, 50 30" />
        <path fill="none" stroke="currentColor" strokeWidth="2" strokeOpacity="0.5"
            d="M30 40 L70 50 M40 60 L60 30" />
    </svg>
);

const SwiggleLine = ({ color = "white", className }: { color?: string, className?: string }) => (
    <svg viewBox="0 0 200 20" className={className} style={{ width: '100px', height: '10px', color }}>
        <path fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round"
            d="M5 10 Q 25 0, 45 10 T 85 10 T 125 10 T 165 10" />
    </svg>
);

export const DoodleLayout = ({ photos, analysis }: LayoutProps) => {
    const rotations = useMemo(() => photos.map(() => Math.random() * 20 - 10), [photos]);
    const stickerPositions = useMemo(() => [...Array(12)].map(() => ({
        top: `${Math.random() * 90}%`,
        left: `${Math.random() * 90}%`,
        rotate: Math.random() * 360,
        type: Math.floor(Math.random() * 3)
    })), []);

    // Pick colors from AI palette or defaults
    const palette = analysis?.colorPalette || ["#FF6B6B", "#4ECDC4", "#FFEEAD", "#FFCC00"];
    const bgColor = palette[0] + "20"; // Subtle 20% opacity of dominant color

    return (
        <div className="relative w-full h-full overflow-hidden flex items-center justify-center p-4 md:p-8 transition-colors duration-1000"
            style={{ backgroundColor: bgColor }}>

            {/* Texture */}
            <div className="absolute inset-0 opacity-10 pointer-events-none"
                style={{ backgroundImage: 'radial-gradient(circle, #000 1px, transparent 1px)', backgroundSize: '30px 30px' }}>
            </div>

            {/* Main Collage Grid */}
            <div className="relative w-full max-w-5xl h-full grid grid-cols-2 md:grid-cols-3 gap-4 md:gap-8 items-center justify-center content-center z-10">
                {photos.slice(0, 6).map((photo, index) => (
                    <div
                        key={index}
                        className="relative bg-white p-2 pb-6 shadow-2xl transition-transform hover:scale-110 hover:z-50 duration-500 group"
                        style={{
                            transform: `rotate(${rotations[index]}deg)`,
                        }}
                    >
                        <div className="overflow-hidden bg-gray-100 aspect-square">
                            <img src={photo} className="w-full h-full object-cover grayscale-[0.2] group-hover:grayscale-0 transition-all" />
                        </div>
                        {/* Washi Tape */}
                        <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-16 h-5 opacity-40 bg-white/60 -rotate-2 backdrop-blur-sm border-x border-white/20"></div>

                        {/* Minimal Label */}
                        {index === 0 && (
                            <div className="absolute -bottom-1 left-2">
                                <span className="font-['Indie_Flower'] text-sm text-black/60 italic">
                                    {analysis?.dominantEmotion || "Vibes"}
                                </span>
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {/* Doodles Layer */}
            <div className="absolute inset-0 pointer-events-none z-20 overflow-hidden">
                {stickerPositions.map((pos, i) => (
                    <div
                        key={i}
                        className="absolute opacity-40"
                        style={{ top: pos.top, left: pos.left, transform: `rotate(${pos.rotate}deg)` }}
                    >
                        {pos.type === 0 ? <StarDoodle color={palette[i % palette.length]} /> :
                            pos.type === 1 ? <HeartDoodle color={palette[(i + 1) % palette.length]} /> :
                                <SwiggleLine color={palette[(i + 2) % palette.length]} />}
                    </div>
                ))}
            </div>

            {/* Brand Logo / Accent */}
            <div className="absolute bottom-6 right-6 opacity-30 flex flex-col items-end">
                <span className="font-mono text-[8px] tracking-[0.4em] uppercase">Mood Snap Studio</span>
                <div className="flex gap-1 mt-1">
                    {palette.map((c, i) => <div key={i} className="w-2 h-2 rounded-full" style={{ backgroundColor: c }} />)}
                </div>
            </div>
        </div>
    );
};
