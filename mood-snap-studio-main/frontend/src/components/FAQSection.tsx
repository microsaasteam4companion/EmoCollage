import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";

const faqs = [
  {
    question: "Do you work with a small business?",
    answer: "Yes! SnapCollage is perfect for small businesses, photographers, and content creators who want to create beautiful emotion-based collages for their clients or social media presence.",
  },
  {
    question: "Do you offer ongoing support?",
    answer: "Not only do we offer the expected maintenance and security but we also offer design and marketing support. Our goal is to become an extension of your in-house marketing team and we'll build a team and offering that empowers your internal team. You can read more about MLab Mate.",
  },
  {
    question: "How long does collage generation take?",
    answer: "Our AI processes your photos in seconds! Depending on the number of images and complexity of the collage style, generation typically takes between 5-15 seconds.",
  },
  {
    question: "Can I create video reels automatically?",
    answer: "Absolutely! Our 'Year in Emotions' feature creates beautiful cinematic videos from your photos, complete with music and transitions based on detected emotions.",
  },
  {
    question: "Are there premium templates?",
    answer: "Yes, we offer both free and premium templates. Premium templates include exclusive designs, advanced customization options, and priority processing.",
  },
];

const FAQSection = () => {
  return (
    <section className="py-24 bg-background">
      <div className="container mx-auto px-6">
        <div className="grid lg:grid-cols-2 gap-16 items-start">
          {/* Left Content */}
          <div>
            <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
              FAQ
            </h2>
            <p className="text-muted-foreground mb-6">
              Can't find the answer you're looking for? Ask your question and get an answer within 24 hours
            </p>
            <Button variant="outline">
              Ask a question
            </Button>
          </div>

          {/* Right Accordion */}
          <div>
            <Accordion type="single" collapsible defaultValue="item-1" className="space-y-4">
              {faqs.map((faq, index) => (
                <AccordionItem
                  key={index}
                  value={`item-${index}`}
                  className="bg-card border border-card-border rounded-2xl px-6 overflow-hidden data-[state=open]:shadow-soft"
                >
                  <AccordionTrigger className="text-left font-semibold text-foreground py-5 hover:no-underline">
                    {faq.question}
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground pb-5">
                    {faq.answer}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FAQSection;
