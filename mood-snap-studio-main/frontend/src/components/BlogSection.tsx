import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

const blogPosts = [
  {
    title: "How AI Understands Emotions in Photos",
    excerpt: "Email marketing remains one of the most powerful tools for businesses to connect with their audience and drive conversions.",
    category: "Technology",
    image: "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=600&h=400&fit=crop",
    bgColor: "gradient-peach",
  },
  {
    title: "Top Aesthetic Collage Trends for 2025",
    excerpt: "SEO and contextual advertising are two of the most powerful digital marketing tools that are used to attract visitors (traffic) to the site. But which are...",
    category: "Design",
    image: "https://images.unsplash.com/photo-1558655146-9f40138edfeb?w=600&h=400&fit=crop",
    bgColor: "gradient-hero",
  },
];

const BlogSection = () => {
  return (
    <section id="blog" className="py-24 bg-background">
      <div className="container mx-auto px-6">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-12">
          <div>
            <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
              Blog
            </h2>
            <p className="text-muted-foreground max-w-xl">
              In our blogs you can read articles written by experts in the field of marketing and business.
            </p>
          </div>
          <Button variant="outline" className="mt-4 md:mt-0">
            More articles
            <ArrowRight className="ml-2 w-4 h-4" />
          </Button>
        </div>

        {/* Blog Cards */}
        <div className="grid md:grid-cols-2 gap-8">
          {blogPosts.map((post, index) => (
            <div
              key={index}
              className={`group rounded-2xl overflow-hidden ${post.bgColor} p-8 card-hover cursor-pointer min-h-[320px] flex flex-col justify-between`}
            >
              <div>
                <span className="inline-block px-3 py-1 bg-background/20 rounded-full text-sm font-medium text-foreground/80 mb-4">
                  {post.category}
                </span>
                <h3 className="text-2xl font-bold text-foreground mb-4 group-hover:underline">
                  {post.title}
                </h3>
                <p className="text-foreground/70 line-clamp-3">
                  {post.excerpt}
                </p>
              </div>
              
              {/* Decorative Element */}
              <div className="flex justify-end mt-6">
                <div className="w-24 h-24 bg-background/10 rounded-xl flex items-center justify-center">
                  <svg width="48" height="48" viewBox="0 0 48 48" fill="none" className="text-foreground/50">
                    <rect x="8" y="8" width="32" height="24" rx="2" stroke="currentColor" strokeWidth="2"/>
                    <path d="M8 16H40" stroke="currentColor" strokeWidth="2"/>
                    <circle cx="12" cy="12" r="1" fill="currentColor"/>
                    <circle cx="16" cy="12" r="1" fill="currentColor"/>
                    <circle cx="20" cy="12" r="1" fill="currentColor"/>
                  </svg>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default BlogSection;
