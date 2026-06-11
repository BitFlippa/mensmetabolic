import { motion } from "motion/react";
import { QuatrefoilMark } from "./Navbar";

function InlinePill() {
  return (
    <span
      aria-hidden="true"
      className="inline-flex items-center justify-center align-middle mx-1.5 sm:mx-2 w-[46px] h-[27px] sm:w-[64px] sm:h-[36px] border-[1.6px] border-ink rounded-[22px]"
    >
      <span className="w-[6px] h-[6px] rounded-full bg-ink" />
    </span>
  );
}

function PhonePreview() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay: 0.3 }}
      className="relative mx-auto mt-20 lg:mt-0 lg:mx-0 lg:absolute lg:right-10 lg:top-[118px] z-[2] w-[300px] h-[606px] rounded-[44px] bg-ink p-[11px] shadow-[0_50px_90px_-34px_rgba(30,30,45,0.55)] -rotate-4"
      aria-hidden="true"
    >
      <div className="w-full h-full rounded-[34px] bg-[#f3f3f7] overflow-hidden flex flex-col">
        <div className="flex items-center gap-2 px-5 pt-5 pb-3 text-ink">
          <QuatrefoilMark size={16} />
          <span className="text-[14.5px] font-bold">consultmd</span>
        </div>
        <div className="flex-1 px-4 py-2 flex flex-col gap-3">
          <div className="self-end max-w-[78%] bg-ink-button text-white text-[13px] leading-[1.45] px-3.5 py-[11px] rounded-[18px_18px_6px_18px]">
            I've had a sore throat and fever for 3 days.
          </div>
          <div className="self-start max-w-[86%] bg-white text-[#2a2a30] text-[13px] leading-[1.45] px-3.5 py-[11px] rounded-[18px_18px_18px_6px] shadow-[0_2px_10px_-4px_rgba(40,40,60,0.18)]">
            That can be strep or a viral infection. A clinician can review your
            symptoms and prescribe if needed.
          </div>
          <div className="self-start inline-flex items-center gap-1.5 bg-[#eef2e3] text-[#2f3a1c] text-xs font-semibold px-3.5 py-[9px] rounded-2xl">
            Start a visit →
          </div>
        </div>
        <div className="mx-3.5 mb-4 flex items-center gap-2 bg-white rounded-[14px] h-12 pl-3.5 pr-1.5 shadow-[0_4px_14px_-6px_rgba(40,40,60,0.2)]">
          <span className="flex-1 text-[13px] text-[#b6b6be]">Ask me anything...</span>
          <span className="w-[34px] h-[34px] rounded-[10px] bg-ink-button text-white flex items-center justify-center text-[15px]">
            →
          </span>
        </div>
      </div>
    </motion.div>
  );
}

export default function Hero() {
  return (
    <section className="relative w-full min-h-screen overflow-hidden bg-[linear-gradient(180deg,#edeef3_0%,#e6e6ee_100%)]">
      {/* aurora — the brand's signature soft gradient, lower-left */}
      <div
        aria-hidden="true"
        className="absolute inset-0 z-0 blur-[8px] bg-[radial-gradient(95%_70%_at_14%_100%,rgba(196,228,128,0.6),rgba(196,228,128,0)_52%),radial-gradient(70%_65%_at_2%_80%,rgba(205,201,238,0.5),transparent_58%),radial-gradient(60%_55%_at_26%_110%,rgba(214,236,170,0.46),transparent_60%)]"
      />

      <div className="relative max-w-[1320px] mx-auto min-h-screen px-6 sm:px-12 pb-28 lg:pb-0">
        {/* anatomical watermark — keep faint: calm, not clinical */}
        <img
          src="/anatomia-ink.png"
          alt=""
          width={752}
          height={1344}
          className="hidden lg:block absolute right-[300px] top-[20px] h-[780px] w-auto opacity-[0.11] z-[1] pointer-events-none"
        />

        {/* copy block — offset clears the fixed nav (~84px) + 96px design gap */}
        <div className="relative z-[2] pt-[150px] md:pt-[180px] max-w-[640px]">
          <motion.h1
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="font-extrabold leading-[1.16] tracking-[-0.02em] text-[clamp(32px,6vw,50px)]"
          >
            <span className="text-ink">ConsultMD offers</span>{" "}
            <span className="text-[#a6a6ae]">
              online care and treatment to help you manage your
            </span>
            <InlinePill />
            <span className="text-[#a6a6ae]">health and wellbeing.</span>
          </motion.h1>

          <motion.form
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.15 }}
            onSubmit={(e) => e.preventDefault()}
            className="mt-[42px] flex items-center gap-2.5 w-full max-w-[440px] h-[62px] bg-white rounded-[14px] shadow-[0_12px_34px_-16px_rgba(40,40,60,0.32)] pl-[22px] pr-2"
          >
            <label htmlFor="hero-search" className="sr-only">
              Ask me anything
            </label>
            <input
              id="hero-search"
              type="text"
              placeholder="Ask me anything..."
              className="flex-1 min-w-0 bg-transparent outline-none text-base text-ink placeholder:text-[#b6b6be]"
            />
            <button
              type="submit"
              aria-label="Send"
              className="w-[46px] h-[46px] shrink-0 rounded-[11px] bg-ink-button text-white text-lg flex items-center justify-center hover:bg-black hover:scale-105 active:scale-95 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink transition-all"
            >
              →
            </button>
          </motion.form>
        </div>

        {/* phone chat preview — illustrative product demo */}
        <PhonePreview />

        {/* language toggle */}
        <button
          type="button"
          aria-label="Switch language, English selected"
          className="absolute bottom-[34px] right-6 sm:right-12 z-[3] inline-flex items-center gap-2 bg-white/70 border border-[#b4b4be]/50 rounded-[20px] px-[15px] py-[7px] text-[13px] text-[#6b6b74] hover:bg-white/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink transition-colors"
        >
          pl <span className="text-[#c0c0c8]" aria-hidden="true">—</span>{" "}
          <span className="text-ink font-semibold">en</span>
        </button>
      </div>
    </section>
  );
}
