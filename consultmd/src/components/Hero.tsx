import { motion } from "motion/react";

const VIDEO_URL =
  "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260603_132049_036591b8-6e92-4760-b94c-a7ea6eef315c.mp4";

function EyePill() {
  return (
    <span
      aria-hidden="true"
      className="w-[16px] md:w-[42px] lg:w-[62px] h-[16px] md:h-[32px] lg:h-[42px] border-[2px] border-[#1a1a1a] rounded-full inline-flex items-center justify-center align-middle mx-1 md:mx-2"
    >
      <span className="w-2 h-2 rounded-full bg-[#1a1a1a]" />
    </span>
  );
}

export default function Hero() {
  return (
    <section className="relative min-h-[110vh] sm:min-h-[140vh] w-full flex flex-col items-center justify-start overflow-hidden bg-bg-base">
      {/* Background video, blended into the #EDEEF5 base */}
      <div className="absolute top-[15vh] sm:top-[20vh] left-0 w-full h-[95vh] sm:h-[120vh] z-0 pointer-events-none">
        {/* Soft atmosphere shown wherever the video hasn't painted */}
        <div className="absolute inset-0 bg-[radial-gradient(55%_45%_at_28%_38%,rgba(159,255,0,0.20),transparent_70%),radial-gradient(45%_55%_at_74%_62%,rgba(26,26,26,0.07),transparent_72%),radial-gradient(70%_60%_at_50%_95%,rgba(159,255,0,0.10),transparent_75%)]" />
        <video
          autoPlay
          loop
          muted
          playsInline
          className="w-full h-full object-cover opacity-100"
          src={VIDEO_URL}
        />
        <div className="absolute top-0 left-0 w-full h-24 sm:h-32 bg-gradient-to-b from-bg-base to-transparent"></div>
      </div>

      {/* Hero content */}
      <div className="max-w-7xl w-full mx-auto px-8 md:px-16 lg:px-20 relative z-10 grid grid-cols-12 gap-x-4 md:gap-x-8 pt-32 md:pt-44">
        <div className="col-span-12 md:col-span-10 md:col-start-2">
          <motion.h1
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="font-display font-medium tracking-[-0.02em] leading-[1.12] text-[2.1rem] sm:text-[2.6rem] lg:text-[3.25rem] xl:text-[3.75rem]"
          >
            <span className="text-[#1a1a1a]">ConsultMD offers</span>{" "}
            <span className="text-[#8e8e8e]">online care</span>
            <br />
            <span className="text-[#8e8e8e]">and treatment to help you manage</span>
            <br />
            <span className="text-[#8e8e8e]">
              your <EyePill /> health and wellbeing.
            </span>
          </motion.h1>

          {/* Search pill */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.15 }}
            className="mt-8 md:mt-10 max-w-md"
          >
            <form
              onSubmit={(e) => e.preventDefault()}
              className="bg-white rounded-[6px] border border-black/[0.05] p-1 pl-4 flex items-center shadow-sm"
            >
              <label htmlFor="hero-search" className="sr-only">
                Ask me anything
              </label>
              <input
                id="hero-search"
                type="text"
                placeholder="Ask me anything..."
                className="flex-1 bg-transparent outline-none text-sm text-zinc-900 placeholder:text-zinc-400 py-2.5"
              />
              <button
                type="submit"
                aria-label="Submit question"
                className="bg-[#1a1a1a] text-white w-9 h-9 rounded-full relative shrink-0 hover:bg-black hover:scale-105 active:scale-95 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1a1a1a] transition-all"
              >
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="w-4 h-4 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
                  aria-hidden="true"
                >
                  <path d="M5 12h14" />
                  <path d="m13 6 6 6-6 6" />
                </svg>
              </button>
            </form>
          </motion.div>
        </div>
      </div>

      {/* Architectural edge anchors */}
      <button
        type="button"
        className="absolute right-4 md:right-8 top-1/2 -translate-y-1/2 z-20 backdrop-blur-md bg-white/30 border border-white/50 rounded-full px-4 py-2 text-xs tracking-wide text-[#1a1a1a] shadow-sm hover:bg-white/50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1a1a1a] transition-colors"
        aria-label="Switch language, English selected"
      >
        <span className="text-[#1a1a1a]/50">pl</span>
        <span className="mx-1.5 text-[#1a1a1a]/40" aria-hidden="true">
          —
        </span>
        <span className="font-medium">en</span>
      </button>

      <span className="absolute bottom-6 left-6 md:left-8 z-20 text-xs tracking-wide text-[#1a1a1a]/70">
        2024
      </span>
      <span className="absolute bottom-6 right-6 md:right-8 z-20 text-xs tracking-wide text-[#1a1a1a]/70">
        telehealth tools
      </span>
    </section>
  );
}
