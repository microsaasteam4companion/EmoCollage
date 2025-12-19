import { LayoutProps } from "@/types/collage";

const scatteredPositions = [
    { top: 5, left: 10, rotate: -8, scale: 1, zIndex: 1 },
    { top: 2, left: 35, rotate: 3, scale: 0.9, zIndex: 2 },
    { top: 8, left: 60, rotate: -5, scale: 1.1, zIndex: 3 },
    { top: 0, left: 80, rotate: 6, scale: 0.85, zIndex: 1 },
    { top: 25, left: 5, rotate: 5, scale: 0.95, zIndex: 4 },
    { top: 22, left: 28, rotate: -3, scale: 1.05, zIndex: 5 },
    { top: 28, left: 52, rotate: 7, scale: 0.9, zIndex: 2 },
    { top: 20, left: 75, rotate: -6, scale: 1, zIndex: 3 },
    { top: 48, left: 8, rotate: -4, scale: 1.1, zIndex: 6 },
];

export const ScrapbookLayout = ({ photos, analysis }: LayoutProps) => {
    const getBackground = () => {
        if (analysis.colorPalette && analysis.colorPalette.length >= 2) {
            return `linear-gradient(135deg, ${analysis.colorPalette[0]}40 0%, ${analysis.colorPalette[1]}40 100%)`;
        }
        return "linear-gradient(135deg, #F5F5F5 0%, #E0E0E0 100%)";
    };

    return (
        <div
            className="relative w-full h-full rounded-2xl overflow-hidden"
            style={{
                background: getBackground(),
            }}
        >
            {/* Paper Texture Overlay */}
            <div className="absolute inset-0 opacity-20 pointer-events-none"
                style={{ backgroundImage: `url("https://www.transparenttextures.com/patterns/paper.png")` }}>
            </div>

            {photos.map((photo, index) => {
                const pos = scatteredPositions[index % scatteredPositions.length];
                return (
                    <div
                        key={index}
                        className="absolute rounded-xl overflow-hidden shadow-xl transition-transform hover:scale-105 hover:z-50"
                        style={{
                            top: `${pos.top}%`,
                            left: `${pos.left}%`,
                            transform: `rotate(${pos.rotate}deg) scale(${pos.scale})`,
                            zIndex: pos.zIndex,
                            width: "22%",
                            maxWidth: "180px",
                        }}
                    >
                        <div
                            className="bg-white p-2 rounded-sm shadow-md"
                            style={{ transform: `rotate(${Math.random() * 2 - 1}deg)` }}
                        >
                            <img
                                src={photo}
                                alt={`Photo ${index + 1}`}
                                className="w-full aspect-square object-cover"
                            />
                        </div>
                        {/* Tape Effect */}
                        <div className="absolute -top-3 left-[40%] w-8 h-4 bg-white/40 rotate-12 backdrop-blur-sm"></div>
                    </div>
                );
            })}

        </div>
    );
};
