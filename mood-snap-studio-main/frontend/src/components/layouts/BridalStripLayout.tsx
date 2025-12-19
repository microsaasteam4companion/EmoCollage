import { LayoutProps } from "@/types/collage";

export const BridalStripLayout = ({ photos, analysis }: LayoutProps) => {
    // We need at least 3-4 photos for this effect to look good
    const displayPhotos = photos.slice(0, 5);
    const colCount = displayPhotos.length;

    return (
        <div className="relative w-full h-full bg-black flex overflow-hidden">
            {/* Vertical Strips */}
            {displayPhotos.map((photo, index) => (
                <div
                    key={index}
                    className="relative h-full transition-all duration-700 hover:w-[150%] grayscale hover:grayscale-0 group border-r border-white/20 last:border-0"
                    style={{ flex: 1 }}
                >
                    <img src={photo} className="w-full h-full object-cover opacity-80 group-hover:opacity-100" alt="" />
                    <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/90"></div>
                </div>
            ))}
        </div>
    );
};
