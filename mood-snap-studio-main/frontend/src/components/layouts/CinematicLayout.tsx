import { LayoutProps } from "@/types/collage";

export const CinematicLayout = ({ photos }: LayoutProps) => {
    return (
        <div className="relative w-full h-full flex flex-col items-center justify-center p-8 overflow-hidden bg-black">
            {/* Grain Overlay */}
            <div className="absolute inset-0 opacity-[0.15] pointer-events-none z-10 mix-blend-overlay"
                style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")` }}>
            </div>

            {/* Main Container - Letterboxed */}
            <div className="relative z-0 w-full max-w-4xl aspect-video bg-[#1a1a1a] shadow-2xl flex flex-row items-center border-y-[60px] border-black">
                {/* Film Strip Effect */}
                <div className="flex-1 flex gap-4 px-8 overflow-hidden h-full items-center justify-center">
                    {photos.slice(0, 3).map((photo, i) => (
                        <div key={i} className={`relative flex-shrink-0 transition-all duration-500
                    ${i === 1 ? 'w-[45%] z-20 scale-105 shadow-[0_0_30px_rgba(0,0,0,0.5)]' : 'w-[25%] opacity-60 hover:opacity-100 grayscale hover:grayscale-0'}`}>
                            <img src={photo} className="w-full h-full object-cover border-[1px] border-white/20" alt="Cinematic" />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};
