import { LayoutProps } from "@/types/collage";

export const VogueLayout = ({ photos, analysis }: LayoutProps) => {
    // Use first photo as cover, others as insets if available
    const coverPhoto = photos[0];
    const insetPhoto = photos[1];

    return (
        <div className="relative w-full h-full bg-white flex items-center justify-center p-4">
            <div className="relative w-full max-w-[500px] aspect-[3/4] bg-white shadow-xl overflow-hidden flex flex-col">
                {/* Main Image */}
                <div className="flex-1 w-full h-full relative">
                    <img src={coverPhoto} className="w-full h-full object-cover" alt="Cover" />
                </div>

                {/* Floating Inset (if 2nd photo exists) */}
                {insetPhoto && (
                    <div className="absolute top-[30%] right-[-10px] w-24 h-32 border-4 border-white shadow-lg rotate-6 z-10">
                        <img src={insetPhoto} className="w-full h-full object-cover" alt="Detail" />
                    </div>
                )}
            </div>
        </div>
    );
};
