const testimonials = [
  {
    quote: "Their experience helped us to develop the business as a whole",
    content: "The MLab team has played an important role in providing us with forward-thinking marketing support that influences growth. When I started MLab project I had 10 employees at the start, I have 20 employees in my team and the number of sales has increased 3 times.",
    name: "Philip Lane",
    role: "Business owner",
    image: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face",
  },
  {
    quote: "The SnapCollage team is fast, savvy, and truly ahead of the curve",
    content: "The growth squad model helped us stay agile yet laser-focused in achieving our metrics and growth objectives. Their AI technology is quick and consistent in delivering top and bottom-line growth.",
    name: "Kristin Watson",
    role: "General Manager",
    image: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop&crop=face",
  },
];

const TestimonialsSection = () => {
  return (
    <section className="py-24 bg-muted/30">
      <div className="container mx-auto px-6">
        <div className="grid md:grid-cols-2 gap-8">
          {testimonials.map((testimonial, index) => (
            <div
              key={index}
              className="bg-card rounded-2xl border border-card-border p-8 shadow-card"
            >
              {/* Quote Mark */}
              <div className="text-pink text-6xl font-serif leading-none mb-4">"</div>
              
              {/* Quote Title */}
              <h3 className="text-2xl font-bold text-foreground mb-4">
                {testimonial.quote}
              </h3>
              
              {/* Quote Content */}
              <p className="text-muted-foreground mb-8 leading-relaxed">
                {testimonial.content}
              </p>
              
              {/* Author */}
              <div className="flex items-center gap-4">
                <img
                  src={testimonial.image}
                  alt={testimonial.name}
                  className="w-12 h-12 rounded-full object-cover"
                />
                <div>
                  <p className="font-semibold text-foreground">{testimonial.name}</p>
                  <p className="text-sm text-muted-foreground">{testimonial.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;
