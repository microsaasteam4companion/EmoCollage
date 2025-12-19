import { LayoutProps } from "@/types/collage";

export const MixedMediaLayout = ({ photos, analysis }: LayoutProps) => {
    // Use a mix of photos for different 'layers'
    // Background images, torn paper effects, etc.

    return (
        <div className="relative w-full h-full overflow-hidden flex items-center justify-center">
            {/* Dynamic Gradient Background based on Palette */}
            <div
                className="absolute inset-0 z-0 opacity-80"
                style={{
                    background: `linear-gradient(135deg, ${analysis.colorPalette[0]} 0%, ${analysis.colorPalette[1]} 50%, ${analysis.colorPalette[2]} 100%)`,
                    filter: 'contrast(1.2) brightness(0.9)'
                }}
            />

            {/* Texture Overlay (Noise/Paper) */}
            <div className="absolute inset-0 z-0 opacity-40 mix-blend-overlay pointer-events-none"
                style={{ backgroundImage: `url("https://www.transparenttextures.com/patterns/stardust.png")` }}>
            </div>

            {/* "Ripped" Text Layer */}
            <div className="absolute top-[10%] left-[5%] z-20 mix-blend-difference">
                <h2 className="text-[4rem] font-black tracking-tighter uppercase leading-none opacity-80 rotate-[-2deg]"
                    style={{ fontFamily: 'Impact, sans-serif' }}>
                    {analysis.dominantEmotion}
                </h2>
                <div className="bg-black text-white px-2 py-1 text-xl font-bold inline-block transform -rotate-1 skew-x-12 mt-2">
                    #{analysis.emotions[0]}
                </div>
            </div>

            {/* Scattered Mix of Photos */}
            <div className="relative w-full h-full z-10 p-8">
                {photos.map((photo, index) => {
                    // Randomize positions slightly for that "messy" look
                    const randomRotate = (index % 2 === 0 ? 1 : -1) * (Math.random() * 15 + 5);
                    const randomX = (index % 3 - 1) * 20 + Math.random() * 10;
                    const randomY = (index % 3 - 1) * 10 + Math.random() * 10;

                    const isHero = index === 0;

                    return (
                        <div
                            key={index}
                            className={`absolute transition-all duration-500 hover:z-50 hover:scale-110
                            ${isHero ? 'w-[40%] top-[25%] left-[30%] z-20 grayscale-0' : 'w-[25%] opacity-90 z-10 grayscale hover:grayscale-0'}`}
                            style={{
                                transform: `translate(${randomX}%, ${randomY}%) rotate(${randomRotate}deg)`,
                                top: isHero ? '20%' : `${Math.random() * 60 + 10}%`,
                                left: isHero ? '30%' : `${Math.random() * 60 + 10}%`,
                                boxShadow: '10px 10px 30px rgba(0,0,0,0.3)'
                            }}
                        >
                            {/* Tape Effect */}
                            <div className="absolute -top-4 left-1/2 -translate-x-1/2 w-16 h-8 bg-white/30 backdrop-blur-sm rotate-3 shadow-sm z-30"></div>

                            <div className="bg-white p-2 pb-8 shadow-xl">
                                <div className="relative overflow-hidden aspect-[4/5] filter sepia-[0.2]">
                                    <img src={photo} className="w-full h-full object-cover" alt="Collage Item" />
                                    <div className="absolute inset-0 ring-1 ring-inset ring-black/10"></div>
                                </div>
                                {/* Scribble/Annotation */}
                                {index === 1 && (
                                    <div className="absolute bottom-2 right-2 text-black font-handwriting text-xs rotate-[-5deg] opacity-70">
                                        {analysis.vibeDescription.split(" ")[0]}...
                                    </div>
                                )}
                            </div>
                        </div>
                    )
                })}
            </div>

            {/* Foreground Elements */}
            <div className="absolute bottom-10 right-10 z-30 flex flex-col items-end pointer-events-none">
                <div className="text-[5rem] leading-none text-white font-bold opacity-20 mix-blend-overlay">
                    {new Date().getFullYear()}
                </div>
            </div>
        </div>
    );
};
