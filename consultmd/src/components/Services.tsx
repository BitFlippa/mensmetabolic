import { motion } from "motion/react";
import type { ReactNode } from "react";

type Service = {
  title: string;
  description: string;
  icon: ReactNode;
};

function Icon({ children }: { children: ReactNode }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="w-6 h-6"
      aria-hidden="true"
    >
      {children}
    </svg>
  );
}

const SERVICES: Service[] = [
  {
    title: "urgent care",
    description:
      "Same-day sick visits for colds, flu, sinus and ear infections, UTIs, and more. No appointment, no waiting room.",
    icon: (
      <Icon>
        <path d="M12 4v16M4 12h16" />
        <rect x="3" y="3" width="18" height="18" rx="5" />
      </Icon>
    ),
  },
  {
    title: "primary care",
    description:
      "Ongoing management for chronic conditions like hypertension, type 2 diabetes, asthma, thyroid, and cholesterol.",
    icon: (
      <Icon>
        <path d="M3.5 12h4l2-5 3 9 2-4h5.5" />
        <path d="M12 21C7 17 3 13.5 3 9a5 5 0 0 1 9-3 5 5 0 0 1 9 3c0 4.5-4 8-9 12Z" />
      </Icon>
    ),
  },
  {
    title: "dermatology",
    description:
      "Photo-based visits for acne, eczema, psoriasis, rashes, rosacea, hair loss, and other skin concerns.",
    icon: (
      <Icon>
        <circle cx="12" cy="12" r="9" />
        <circle cx="9" cy="10" r="1" fill="currentColor" stroke="none" />
        <circle cx="14.5" cy="14.5" r="1" fill="currentColor" stroke="none" />
        <circle cx="13" cy="8" r="0.8" fill="currentColor" stroke="none" />
      </Icon>
    ),
  },
  {
    title: "women's health",
    description:
      "Birth control, UTI and yeast infection treatment, menstrual suppression, and everyday women's care.",
    icon: (
      <Icon>
        <circle cx="12" cy="9" r="5" />
        <path d="M12 14v7M9 18h6" />
      </Icon>
    ),
  },
  {
    title: "men's health",
    description:
      "Treatment for ED, premature ejaculation, hair loss, and other men's health concerns, handled discreetly.",
    icon: (
      <Icon>
        <circle cx="10" cy="14" r="5" />
        <path d="M14 10l6-6M14.5 4H20v5.5" />
      </Icon>
    ),
  },
  {
    title: "sexual health",
    description:
      "Confidential STD testing, treatment, and partner care with judgment-free, board-certified physicians.",
    icon: (
      <Icon>
        <path d="M12 3l8 3v6c0 4.5-3.5 7.5-8 9-4.5-1.5-8-4.5-8-9V6l8-3Z" />
        <path d="M9 12.5l2 2 4-4.5" />
      </Icon>
    ),
  },
  {
    title: "lab testing",
    description:
      "Doctors order the labs you need at a location near you, then review your results and next steps with you.",
    icon: (
      <Icon>
        <path d="M9 3h6M10 3v6.5L4.7 18a3 3 0 0 0 2.6 4.5h9.4a3 3 0 0 0 2.6-4.5L14 9.5V3" />
        <path d="M7.5 15h9" />
      </Icon>
    ),
  },
  {
    title: "imaging orders",
    description:
      "Physician referrals for X-rays, ultrasounds, CT scans, and MRIs, sent to an imaging center near you.",
    icon: (
      <Icon>
        <rect x="3" y="3" width="18" height="18" rx="3" />
        <path d="M12 7v10M8 9.5h8M9 12.5h6M10 15.5h4" />
      </Icon>
    ),
  },
  {
    title: "prescription refills",
    description:
      "Quick refills of your existing medications, reviewed by a licensed doctor and sent to your pharmacy.",
    icon: (
      <Icon>
        <rect x="3" y="9" width="13" height="12" rx="3" transform="rotate(-45 9.5 15)" />
        <path d="M6.5 12.5l6 6" />
        <path d="M17 3.5a3.5 3.5 0 0 1 3.5 3.5" />
      </Icon>
    ),
  },
  {
    title: "doctor's notes",
    description:
      "Legitimate work and school notes issued after a quick online evaluation, delivered the same day.",
    icon: (
      <Icon>
        <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5Z" />
        <path d="M14 3v5h5M9 13h6M9 17h4" />
      </Icon>
    ),
  },
];

const STATS = [
  ["150+", "conditions treated online"],
  ["$39.99", "flat-fee visits, no insurance needed"],
  ["~15 min", "to a prescription at your pharmacy"],
  ["365", "days a year, no appointment"],
] as const;

export default function Services() {
  return (
    <section id="services" className="relative bg-bg-base py-20 md:py-28">
      <div className="max-w-7xl w-full mx-auto px-8 md:px-16 lg:px-20">
        <div className="grid grid-cols-12 gap-x-4 md:gap-x-8">
          <div className="col-span-12 md:col-span-10 md:col-start-2">
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-80px" }}
              transition={{ duration: 0.6 }}
            >
              <p className="text-xs lowercase tracking-[0.2em] text-zinc-500 mb-4">
                what we treat
              </p>
              <h2 className="font-display font-medium tracking-[-0.02em] leading-[1.15] text-3xl sm:text-4xl lg:text-5xl max-w-3xl">
                <span className="text-[#1a1a1a]">See a doctor from your phone</span>{" "}
                <span className="text-[#8e8e8e]">
                  for the visits that fill most waiting rooms.
                </span>
              </h2>
            </motion.div>

            <dl className="mt-10 md:mt-14 grid grid-cols-2 lg:grid-cols-4 gap-y-8 gap-x-6 border-y border-black/[0.06] py-8">
              {STATS.map(([value, label]) => (
                <div key={label}>
                  <dt className="sr-only">{label}</dt>
                  <dd className="font-display text-2xl md:text-3xl font-medium text-[#1a1a1a]">
                    {value}
                  </dd>
                  <dd className="mt-1 text-xs text-zinc-500 leading-relaxed">{label}</dd>
                </div>
              ))}
            </dl>

            <ul className="mt-10 md:mt-14 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5">
              {SERVICES.map((service, i) => (
                <motion.li
                  key={service.title}
                  initial={{ opacity: 0, y: 15 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: "-40px" }}
                  transition={{ duration: 0.5, delay: (i % 3) * 0.08 }}
                  className="group bg-white rounded-2xl border border-black/[0.05] p-6 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all"
                >
                  <div className="w-11 h-11 rounded-full bg-bg-base text-[#1a1a1a] flex items-center justify-center group-hover:bg-brand-green transition-colors">
                    {service.icon}
                  </div>
                  <h3 className="mt-5 font-display text-lg font-medium lowercase tracking-tight text-[#1a1a1a]">
                    {service.title}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-zinc-500">
                    {service.description}
                  </p>
                </motion.li>
              ))}
            </ul>

            <motion.div
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.6 }}
              className="mt-12 md:mt-16 flex flex-col sm:flex-row sm:items-center gap-4"
            >
              <a
                href="#get-started"
                id="get-started"
                className="inline-flex items-center justify-center bg-[#1a1a1a] text-white text-sm lowercase tracking-wide rounded-full px-7 py-3.5 hover:bg-black hover:scale-[1.02] active:scale-[0.98] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1a1a1a] transition-all"
              >
                start a visit <span className="ml-2" aria-hidden="true">→</span>
              </a>
              <p className="text-xs text-zinc-500 max-w-xs leading-relaxed">
                Board-certified physicians. No subscription required, no surprise
                bills, available in all 50 states.
              </p>
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  );
}
