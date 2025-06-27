import { useEffect, useState } from "react";

const App = () => {
  const [formData, setFormData] = useState({
    application_month: "",
    customer_age: 30,
    employment_type: "Salaried",
    monthly_income: 50000,
    credit_score: 720,
    time_in_job_months: 24,
    loan_amount: 300000,
    loan_term_months: 60,
    loan_type: "Personal",
    loan_purpose: "Business",
    existing_loan_count: 1,
    existing_emi_total: 8000,
    prev_defaults_count: 0,
  });

  const [dtiRatio, setDtiRatio] = useState(0.0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const month = new Date().toISOString().slice(0, 7);
    setFormData((prev) => ({ ...prev, application_month: month }));
  }, []);

  useEffect(() => {
    const { existing_emi_total, monthly_income } = formData;
    if (monthly_income > 0) {
      setDtiRatio((existing_emi_total / monthly_income).toFixed(3));
    }
  }, [formData.existing_emi_total, formData.monthly_income]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: isNaN(value) ? value : Number(value),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    const payload = { ...formData, dti_ratio: Number(dtiRatio) };

    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("Prediction failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-black via-[#0a0a0a] to-[#111] text-white px-6 py-12">
      <h1 className="text-4xl md:text-5xl text-center font-bold gradient-text mb-12 tracking-wide">
        Loan Approval Predictor
      </h1>

      <form
        onSubmit={handleSubmit}
        className="w-full max-w-7xl mx-auto p-8 md:p-12 bg-[#111827]/70 border border-cyan-500/30 rounded-2xl shadow-xl space-y-14"
      >
        <Section title="Loan Applicant Profile">
          <Field label="Customer Age" name="customer_age" value={formData.customer_age} onChange={handleChange} />
          <Select label="Employment Type" name="employment_type" value={formData.employment_type} onChange={handleChange} options={["Salaried", "Self-Employed"]} />
          <Field label="Monthly Income" name="monthly_income" value={formData.monthly_income} onChange={handleChange} />
          <Field label="Credit Score" name="credit_score" value={formData.credit_score} onChange={handleChange} />
          <Field label="Time in Job (months)" name="time_in_job_months" value={formData.time_in_job_months} onChange={handleChange} />
        </Section>

        <Section title="Loan Request Information">
          <Field label="Loan Amount" name="loan_amount" value={formData.loan_amount} onChange={handleChange} />
          <Field label="Loan Term (months)" name="loan_term_months" value={formData.loan_term_months} onChange={handleChange} />
          <Select label="Loan Type" name="loan_type" value={formData.loan_type} onChange={handleChange} options={["Personal", "Education", "Business", "Home", "Auto"]} />
          <Select label="Loan Purpose" name="loan_purpose" value={formData.loan_purpose} onChange={handleChange} options={["Business", "Education", "Medical Emergency", "Home Improvement", "Business Expansion", "Wedding", "Vehicle Purchase"]} />
        </Section>

        <Section title="Existing Financial Commitments">
          <Field label="Existing Loan Count" name="existing_loan_count" value={formData.existing_loan_count} onChange={handleChange} />
          <Field label="Existing EMI Total" name="existing_emi_total" value={formData.existing_emi_total} onChange={handleChange} />
          <Field label="Previous Defaults Count" name="prev_defaults_count" value={formData.prev_defaults_count} onChange={handleChange} />
          <div className="md:col-span-2 text-sm text-cyan-400 mt-2">
          DTI Ratio : <span className="font-semibold">{dtiRatio}</span>
          </div>
        </Section>

        <div className="text-center">
          <button
            type="submit"
            className="bg-gradient-to-r from-pink-500 via-fuchsia-500 to-blue-500 hover:from-pink-600 hover:to-cyan-400 text-white px-10 py-3 rounded-full font-semibold text-lg transition-all duration-300 hover:scale-105 shadow-md"
          >
            {loading ? "Predicting..." : "Predict Loan Approval"}
          </button>
        </div>
      </form>

      {result && (
        <div className="mt-14 p-6 max-w-2xl mx-auto bg-[#0b0b0b]/80 border border-cyan-600 rounded-xl text-center shadow-lg">
          <h2 className="text-xl font-bold gradient-text mb-2">🔍 Prediction Result</h2>
          <p className="text-lg">
            Status:{" "}
            <span className={result.loan_approved ? "text-green-400" : "text-red-400"}>
              {result.loan_approved ? "Approved ✅" : "Rejected ❌"}
            </span>
          </p>
          <p className="mt-2 text-cyan-400">Confidence: {Math.round(result.confidence * 100)}%</p>
          <p className="text-sm text-gray-500 mt-1">Model: {result.model_used}</p>
        </div>
      )}
    </div>
  );
};

const Section = ({ title, children }) => (
  <div>
    <h3 className="text-xl md:text-2xl font-bold gradient-text mb-6 border-b border-cyan-700 pb-1">{title}</h3>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">{children}</div>
  </div>
);

const Field = ({ label, name, value, onChange }) => (
  <div className="flex flex-col">
    <label className="text-sm text-gray-300 mb-1">{label}</label>
    <input
      type="text"
      name={name}
      value={value}
      onChange={onChange}
      className="bg-black text-white border border-cyan-700 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
    />
  </div>
);

const Select = ({ label, name, value, options, onChange }) => (
  <div className="flex flex-col">
    <label className="text-sm text-gray-300 mb-1">{label}</label>
    <select
      name={name}
      value={value}
      onChange={onChange}
      className="bg-black text-white border border-cyan-700 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
    >
      {options.map((opt) => (
        <option key={opt} value={opt}>
          {opt}
        </option>
      ))}
    </select>
  </div>
);

export default App;
