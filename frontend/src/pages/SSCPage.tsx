import { Link } from "react-router-dom";

export default function SSCPage() {
  return (
    <div
      className="flex min-h-[55vh] items-center justify-center bg-[#F8F9FA] px-4 py-12 text-[#2D3436] sm:px-6"
      style={{ fontFamily: "Inter, 'Noto Sans Devanagari', sans-serif" }}
    >
      <section
        aria-labelledby="ssc-heading"
        className="w-full max-w-2xl rounded-lg border border-[#2D3436]/10 bg-white p-6 text-center shadow-sm sm:p-10"
      >
        <span className="inline-flex rounded-full bg-[#FF6B35]/10 px-3 py-1 text-sm font-semibold text-[#c2410c]">
          Coming in the next stage
        </span>
        <h1 id="ssc-heading" className="mt-5 text-3xl font-bold sm:text-4xl">
          SSC Practice
        </h1>
        <p className="mt-4 text-lg text-[#2D3436]/80">
          Your SSC preparation journey starts here.
        </p>
        <p className="mt-2 text-[#2D3436]/70">
          Subject selection will be available in the next stage.
        </p>
        <div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row">
          <button
            type="button"
            disabled
            className="inline-flex cursor-not-allowed items-center justify-center rounded-md bg-[#007BFF]/60 px-6 py-3 text-base font-semibold text-white"
          >
            Start Preparing · Coming Soon
          </button>
          <Link
            to="/dashboard"
            className="inline-flex items-center justify-center rounded-md border border-[#2D3436]/25 bg-white px-6 py-3 text-base font-semibold text-[#2D3436] transition-colors hover:border-[#007BFF] hover:text-[#007BFF] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] focus-visible:ring-offset-2"
          >
            Back to Dashboard
          </Link>
        </div>
      </section>
    </div>
  );
}
