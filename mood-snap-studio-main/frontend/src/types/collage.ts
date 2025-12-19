export interface EmotionAnalysis {
    dominantEmotion: string;
    emotions: string[];
    vibeDescription: string;
    colorPalette: string[];
    collageStyle: "Cinematic" | "Vogue" | "Scrapbook" | "Minimalist" | string;
    layoutSuggestion: string;
    caption: string;
    filterPreset?: string;
    confidence?: number;
}

export interface LayoutProps {
    photos: string[];
    analysis: EmotionAnalysis;
    onDownload?: () => void;
}
