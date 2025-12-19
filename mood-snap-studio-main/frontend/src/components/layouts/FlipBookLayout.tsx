import { useState } from "react";
import { LayoutProps } from "@/types/collage";
import { VogueLayout } from "./VogueLayout";

export const FlipBookLayout = (props: LayoutProps) => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="relative w-full h-full flex items-center justify-center bg-[#f0f0f0] perspective-[1500px] overflow-hidden">

            {/* Interaction Hint */}
            {!isOpen && (
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 pointer-events-none animate-pulse text-center">
                    <span className="bg-black text-white px-4 py-2 rounded-full text-sm font-medium tracking-wide">
                        CLICK TO OPEN
                    </span>
                </div>
            )}

            {/* The Book Container */}
            <div
                className="relative w-[350px] aspect-[3/4] transition-transform duration-1000 transform-style-3d cursor-pointer hover:scale-105"
                onClick={() => setIsOpen(!isOpen)}
                style={{
                    transform: isOpen ? 'translateX(25%) rotateY(-20deg)' : 'translateX(0) rotateY(0deg)'
                }}
            >
                {/* Front Cover */}
                <div
                    className="absolute inset-0 origin-left transition-all duration-1000 transform-style-3d z-20 shadow-2xl"
                    style={{
                        transform: isOpen ? 'rotateY(-140deg)' : 'rotateY(0deg)',
                    }}
                >
                    {/* Front Face of Cover */}
                    <div className="absolute inset-0 backface-hidden bg-white">
                        <VogueLayout {...props} />
                    </div>

                    {/* Back Face of Cover (Inner Left Page) */}
                    <div className="absolute inset-0 backface-hidden rotate-y-180 bg-white flex items-center justify-center p-8 border-r border-[#ddd]">
                        <div className="text-center space-y-4">
                            <h3 className="font-serif text-2xl italic text-gray-800">"Everything is aesthetic."</h3>
                            <div className="w-16 h-[1px] bg-black mx-auto"></div>
                            <p className="text-xs font-mono text-gray-500 max-w-[200px] mx-auto leading-relaxed">
                                {props.analysis.vibeDescription}
                            </p>
                            {props.photos[2] && (
                                <div className="mt-8 border p-2 rotate-2 shadow-sm">
                                    <img src={props.photos[2]} className="w-32 h-32 object-cover grayscale" />
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Back Cover (Right Page - Static) */}
                <div className="absolute inset-0 bg-white z-10 shadow-lg flex flex-col">
                    {/* This is revealed when cover opens */}
                    <div className="h-[60%] w-full bg-gray-100 relative">
                        {props.photos[1] ? (
                            <img src={props.photos[1]} className="w-full h-full object-cover" />
                        ) : (
                            <div className="w-full h-full flex items-center justify-center bg-gray-200">
                                <span className="text-gray-400">No Image</span>
                            </div>
                        )}
                        <div className="absolute bottom-0 left-0 bg-white px-4 py-2 font-bold text-4xl -mb-4 ml-4">02</div>
                    </div>
                    <div className="flex-1 p-6 flex flex-col justify-end">
                        <p className="font-serif text-3xl leading-tight mb-2">
                            {props.analysis.caption.split(" ").slice(0, 3).join(" ")}
                        </p>
                        <div className="flex gap-2 mt-2">
                            {props.analysis.emotions.slice(0, 3).map(t => (
                                <span key={t} className="text-[10px] border border-black px-2 py-0.5 rounded-full uppercase tracking-wider">
                                    {t}
                                </span>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
