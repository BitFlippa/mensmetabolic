import { useState } from "react";
import { AnimatePresence, motion } from "motion/react";

const NAV_LINKS = ["services", "patient resources", "about us", "education center"];

function CloverIcon() {
  return (
    <svg width="26" height="26" viewBox="0 0 24 24" fill="#1a1a1a" aria-hidden="true">
      <circle cx="8.2" cy="8.2" r="5.2" />
      <circle cx="15.8" cy="8.2" r="5.2" />
      <circle cx="8.2" cy="15.8" r="5.2" />
      <circle cx="15.8" cy="15.8" r="5.2" />
    </svg>
  );
}

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 w-full z-50 py-6 md:py-10 bg-gradient-to-b from-[#f1f1f1]/80 to-transparent backdrop-blur-[2px]">
      <nav
        aria-label="Primary"
        className="grid grid-cols-12 max-w-7xl mx-auto items-center gap-x-4 px-6 sm:px-8 md:px-12"
      >
        <a href="/" className="col-span-6 md:col-span-3 flex items-center gap-2.5">
          <CloverIcon />
          <span className="font-display text-xl md:text-2xl font-medium tracking-tight text-[#1a1a1a]">
            consultmd
          </span>
        </a>

        <ul className="hidden md:flex col-span-6 items-center justify-center gap-7 lg:gap-9">
          {NAV_LINKS.map((link) => (
            <li key={link}>
              <a
                href={`#${link.replace(/\s+/g, "-")}`}
                className="text-xs lowercase tracking-wide text-zinc-600 hover:text-zinc-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#1a1a1a] transition-colors"
              >
                {link}
              </a>
            </li>
          ))}
        </ul>

        <div className="col-span-6 md:col-span-3 flex items-center justify-end gap-4 md:gap-5">
          <a
            href="#find-help"
            className="hidden sm:block text-xs lowercase tracking-wide text-zinc-600 hover:text-zinc-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#1a1a1a] transition-colors"
          >
            find help
          </a>
          <a
            href="#get-started"
            className="whitespace-nowrap bg-[#1a1a1a] text-white text-xs lowercase tracking-wide rounded-full px-5 py-3 hover:bg-black hover:scale-[1.02] active:scale-[0.98] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1a1a1a] transition-all"
          >
            get started <span aria-hidden="true">→</span>
          </a>
          <button
            type="button"
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
            aria-controls="mobile-drawer"
            aria-label={open ? "Close menu" : "Open menu"}
            className="md:hidden relative w-11 h-11 -mr-2 flex flex-col items-center justify-center gap-[5px] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1a1a1a] rounded-full"
          >
            <motion.span
              animate={open ? { rotate: 45, y: 3.5 } : { rotate: 0, y: 0 }}
              transition={{ duration: 0.25, ease: "easeOut" }}
              className="block w-5 h-[1.5px] bg-[#1a1a1a] origin-center"
            />
            <motion.span
              animate={open ? { rotate: -45, y: -3.5 } : { rotate: 0, y: 0 }}
              transition={{ duration: 0.25, ease: "easeOut" }}
              className="block w-5 h-[1.5px] bg-[#1a1a1a] origin-center"
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
            <ul className="mt-4 mx-4 rounded-2xl bg-white/80 backdrop-blur-md border border-black/[0.05] shadow-sm px-6 py-5 flex flex-col gap-4">
              {[...NAV_LINKS, "find help"].map((link) => (
                <li key={link}>
                  <a
                    href={`#${link.replace(/\s+/g, "-")}`}
                    onClick={() => setOpen(false)}
                    className="block py-1 text-sm lowercase tracking-wide text-zinc-700 hover:text-zinc-900"
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
