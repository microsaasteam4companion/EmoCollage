import { LayoutProps } from "@/types/collage";

export const MagazineCoverLayout = ({ photos, analysis }: LayoutProps) => {
    const mainPhoto = photos[0]; // Hero image

    // SAFE ACCESS to all AI data
    const dominantEmotion = analysis?.dominantEmotion || "VIBRANCE";
    const vibeDesc = analysis?.vibeDescription || "The Art of Living";
    const emotions = analysis?.emotions || ["Style", "Grace", "Future"];
    const color = analysis?.colorPalette?.[0] || "#ffffff";

    const month = new Date().toLocaleString('default', { month: 'long' }).toUpperCase();
    const year = new Date().getFullYear();

    return (
        <div className="relative w-full h-full bg-black overflow-hidden flex flex-col shadow-2xl group">

            {/* 1. HERO IMAGE (Absolute Full Screen) with 'Photography Principles' */}
            <div className="absolute inset-0 z-0">
                <img
                    src={mainPhoto}
                    className="w-full h-full object-cover transition-transform duration-700 ease-in-out group-hover:scale-105 filter contrast-[1.15] saturate-[1.1] brightness-[0.95]"
                    alt="Cover Model"
                />
                {/* 2. CINEMATIC GRADIENT (Crucial for text readability - darker at bottom) */}
                <div className="absolute inset-y-0 w-full bg-gradient-to-b from-black/20 via-transparent to-black/60"></div>

                {/* 3. MINIMAL TEXT (Emotional tag) */}
                <div className="absolute bottom-10 left-8 z-20">
                    <h2 className="text-white font-serif italic text-4xl drop-shadow-xl opacity-80 uppercase tracking-tighter">
                        {dominantEmotion}
                    </h2>
                </div>
            </div>

            {/* 7. NOISE OVERLAY (The "Film" Look) */}
            <div className="absolute inset-0 z-40 pointer-events-none opacity-[0.03]"
                style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")` }}>
            </div>
        </div>
    );
};
