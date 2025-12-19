import { LayoutProps } from "@/types/collage";
import { MagazineCoverLayout } from "./MagazineCoverLayout";

export const MagazineSpreadLayout = ({ photos, analysis }: LayoutProps) => {
    // Page 1 is Cover (reused)
    // Page 2 is Editorial

    return (
        <div className="w-full h-full overflow-y-auto bg-[#e5e5e5] flex flex-col items-center gap-8 py-8 perspective-1000">

            {/* PAGE 1: COVER */}
            <div className="w-full max-w-[50vh] aspect-[3/4] shadow-2xl bg-white origin-top transform transition-transform hover:rotate-x-2">
                <MagazineCoverLayout photos={photos} analysis={analysis} />
            </div>

            {/* PAGE 2: EDITORIAL SPREAD */}
            <div className="w-full max-w-[50vh] aspect-[3/4] shadow-xl bg-white p-8 flex flex-col">
                {/* Content Grid */}
                <div className="flex-1 grid grid-cols-2 gap-4">
                    {/* Text Column - Empty Space for balance */}
                    <div className="flex flex-col justify-center space-y-6">
                        <div className="w-12 h-1 bg-black"></div>
                    </div>

                    {/* Image Column */}
                    <div className="flex flex-col gap-4">
                        {photos.slice(1, 3).map((p, i) => (
                            <img key={i} src={p} className="w-full h-40 object-cover grayscale contrast-125" />
                        ))}
                    </div>
                </div>
            </div>

            {/* PAGE 3: FULL BLEED (If enough photos) */}
            {photos.length > 3 && (
                <div className="w-full max-w-[50vh] aspect-[3/4] shadow-xl bg-black relative group">
                    <img src={photos[3]} className="w-full h-full object-cover opacity-80" />
                </div>
            )}

        </div>
    );
};
