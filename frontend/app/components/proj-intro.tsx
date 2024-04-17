export default function TeamIntroduction() {
    return (
      <div className="flex flex-col justify-center items-center h-1/2screen text-center">
        {/* Project Introduction Section */}
        <section className="project-introduction px-4">
          <h2 className="text-5xl font-thin">
            Get insight on your financial reports. Analyse your <span className="text-customHighlight">balance sheet</span>, <span className="text-customHighlight">cash flow</span> and <span className="text-customHighlight">income statement</span>
          </h2>
          <p className="mt-4">
            Welcome to our project! Here, we are creating an RAG system for financial analysis.
          </p>
        </section>
      </div>
    );
  }
  