import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { FileCode, Brain, PhoneCall, ImageIcon, Mic } from "lucide-react";
import { Button } from "@/components/ui/button";

function Hero() {
  const [titleNumber, setTitleNumber] = useState(0);
  const titles = useMemo(
    () => [
      { label: "Whatsapp", icon: PhoneCall },
      { label: "Screenshots", icon: ImageIcon },
      { label: "Voice Messages", icon: Mic },
    ],
    []
  );

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (titleNumber === titles.length - 1) {
        setTitleNumber(0);
      } else {
        setTitleNumber(titleNumber + 1);
      }
    }, 2000);
    return () => clearTimeout(timeoutId);
  }, [titleNumber, titles]);

  return (
    <div className="w-full flex items-center justify-center">
      <div className="container mx-auto">
        <div className="flex gap-8 py-20 lg:py-40 items-center justify-center flex-col">
          <div className="flex gap-4 flex-col justify-center">
            <h1 className="text-5xl md:text-7xl max-w-2xl tracking-tighter text-center font-regular self-center">
              <span className="text-spektr-cyan-50 md:text-5xl mb-5 inline-block">
                Get a deep analysis of your conversations from
              </span>
              <span className="relative flex w-full justify-center overflow-hidden text-center md:pb-4 md:pt-1">
                &nbsp;
                {titles.map((title, index) => (
                  <motion.span
                    key={index}
                    className="absolute font-semibold md:text-6xl flex items-center gap-2 justify-center"
                    initial={{ opacity: 0, y: "-100" }}
                    transition={{ type: "spring", stiffness: 50 }}
                    animate={
                      titleNumber === index
                        ? { y: 0, opacity: 1 }
                        : { y: titleNumber > index ? -150 : 150, opacity: 0 }
                    }
                  >
                    <title.icon className="h-10 w-10 mr-" />
                    {title.label}
                  </motion.span>
                ))}
              </span>
            </h1>
            <p className="text-lg md:text-xl leading-relaxed tracking-tight text-muted-foreground max-w-3xl text-center">
              Get a truly impartial outlook on your conversations, no matter the platform.<br></br>
              Receive a grading on a variety of conversational metrics, and see how you can improve.<br></br>
              This platform is fully <a href="https://github.com" className="font-bold underline text-indigo-300">open-source</a> and stores none of your data past the session.
            </p>
          </div>
          <div className="flex flex-row gap-3">
            <a
              href="https://github.com/joey-david/py-scripts/tree/main/chatbrain"
              target="_blank"
              className="inline-block"
            >
              <Button size="lg" className="gap-4 w-full text-base" variant="secondary">
                View the code <FileCode className="h-6 w-6" />
              </Button>
            </a>
            <a href="/start-analysis" className="inline-block">
              <Button size="lg" className="gap-4 w-full text-base">
                Start a free analysis <Brain className="h-6 w-6" />
              </Button>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export { Hero };
