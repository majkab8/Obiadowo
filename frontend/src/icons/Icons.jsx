export function ArrowUpIcon({ size = 24 }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m5 12 7-7 7 7" />
      <path d="M12 19V5" />
    </svg>
  );
}

export function LogoIcon({ size = 24 }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="48" fill="#ff7043" />
      <rect
        x="35"
        y="55"
        width="30"
        height="18"
        rx="4"
        fill="none"
        stroke="#ffffff"
        stroke-width="3"
      />
      <path
        d="M 35 62 L 28 62 M 65 62 L 72 62"
        stroke="#ffffff"
        stroke-width="3"
        stroke-linecap="round"
      />
      <path
        d="M 33 51 Q 50 42 67 51"
        fill="none"
        stroke="#ffffff"
        stroke-width="3"
        stroke-linecap="round"
      />
      <circle cx="50" cy="44" r="2.5" fill="#ffffff" />
      <path
        d="M 43 35 Q 39 30 43 25 M 50 37 Q 46 32 50 27 M 57 35 Q 53 30 57 25"
        fill="none"
        stroke="#ffffff"
        stroke-width="2.5"
        stroke-linecap="round"
      />
      <path
        d="M 20 32 L 20 42 Q 20 48 24 48 Q 28 48 28 42 L 28 32 M 24 32 L 24 75"
        fill="none"
        stroke="#ffffff"
        stroke-width="2.5"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <path
        d="M 76 32 C 82 32 82 45 76 48 C 70 45 70 32 76 32 Z M 76 48 L 76 75"
        fill="none"
        stroke="#ffffff"
        stroke-width="2.5"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>
  );
}

export function CookingPotIcon({ size = 24 }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      className="lucide lucide-cooking-pot-icon lucide-cooking-pot"
    >
      <path d="M2 12h20" />
      <path d="M20 12v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-8" />
      <path d="m4 8 16-4" />
      <path d="m8.86 6.78-.45-1.81a2 2 0 0 1 1.45-2.43l1.94-.48a2 2 0 0 1 2.43 1.46l.45 1.8" />
    </svg>
  );
}
