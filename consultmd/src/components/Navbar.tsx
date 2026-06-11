import { useState } from "react";
import { AnimatePresence, motion } from "motion/react";

const NAV_LINKS = ["services", "patient resources", "about us", "education center"];

export function BrandMark({
  size = 26,
  variant = "gradient",
}: {
  size?: number;
  variant?: "gradient" | "onyx" | "pearl";
}) {
  return (
    <img
      src={`/brand/mark-${variant}.svg`}
      width={size}
      height={size}
      alt=""
      aria-hidden="true"
    />
  );
}

export function Wordmark({ className = "" }: { className?: string }) {
  return (
    <span className={`font-bold tracking-[-0.035em] ${className}`}>
      consultMD
    </span>
  );
}

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 w-full z-50 bg-gradient-to-b from-[#edeef3]/80 to-transparent backdrop-blur-[2px]">
      <nav
        aria-label="Primary"
        className="max-w-[1320px] mx-auto flex items-center justify-between px-6 sm:px-12 py-5 md:py-[30px]"
      >
        <a href="/" className="flex items-center gap-2 text-ink">
          <BrandMark />
          <Wordmark className="text-[21px]" />
        </a>

        <ul className="hidden md:flex items-center gap-8">
          {NAV_LINKS.map((link) => (
            <li key={link}>
              <a
                href={`#${link.replace(/\s+/g, "-")}`}
                className="text-[14.5px] lowercase text-[#3a3a42] hover:text-ink focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-ink transition-colors"
              >
                {link}
              </a>
            </li>
          ))}
        </ul>

        <div className="flex items-center gap-4 md:gap-6">
          <a
            href="#find-help"
            className="hidden sm:block text-[14.5px] lowercase text-[#3a3a42] hover:text-ink focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-ink transition-colors"
          >
            find help
          </a>
          <a
            href="#get-started"
            className="inline-flex items-center gap-1.5 whitespace-nowrap bg-ink-button text-white text-[14.5px] font-medium lowercase rounded-3xl px-5 py-3 hover:bg-black hover:scale-[1.02] active:scale-[0.98] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink transition-all"
          >
            get started <span className="text-[13px]" aria-hidden="true">→</span>
          </a>
          <button
            type="button"
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
            aria-controls="mobile-drawer"
            aria-label={open ? "Close menu" : "Open menu"}
            className="md:hidden relative w-11 h-11 -mr-2 flex flex-col items-center justify-center gap-[5px] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink rounded-full"
          >
            <motion.span
              animate={open ? { rotate: 45, y: 3.5 } : { rotate: 0, y: 0 }}
              transition={{ duration: 0.25, ease: "easeOut" }}
              className="block w-5 h-[1.5px] bg-ink origin-center"
            />
            <motion.span
              animate={open ? { rotate: -45, y: -3.5 } : { rotate: 0, y: 0 }}
              transition={{ duration: 0.25, ease: "easeOut" }}
              className="block w-5 h-[1.5px] bg-ink origin-center"
            />
          </button>
        </div>
      </nav>

      <AnimatePresence>
        {open && (
          <motion.div
            id="mobile-drawer"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className="md:hidden overflow-hidden"
          >
            <ul className="mt-2 mx-4 rounded-2xl bg-white/80 backdrop-blur-md border border-[#b4b4be]/40 shadow-sm px-6 py-5 flex flex-col gap-4">
              {[...NAV_LINKS, "find help"].map((link) => (
                <li key={link}>
                  <a
                    href={`#${link.replace(/\s+/g, "-")}`}
                    onClick={() => setOpen(false)}
                    className="block py-1 text-sm lowercase text-[#3a3a42] hover:text-ink"
                  >
                    {link}
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
