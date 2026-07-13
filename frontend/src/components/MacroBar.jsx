import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

function MacroBar({ protein, carbs, fat, sugar }) {
  const proteinNum = parseFloat(protein) || 0;
  const carbsNum = parseFloat(carbs) || 0;
  const fatNum = parseFloat(fat) || 0;
  const total = proteinNum + carbsNum + fatNum;

  const data = {
    labels: [""],
    datasets: [
      {
        label: "Białko",
        data: [proteinNum],
        backgroundColor: "#F97316",
        barPercentage: 1.0,
        categoryPercentage: 1.0,
      },
      {
        label: "Węglowodany",
        data: [carbsNum],
        backgroundColor: "#FBBF24",
        barPercentage: 1.0,
        categoryPercentage: 1.0,
      },
      {
        label: "Tłuszcze",
        data: [fatNum],
        backgroundColor: "#60A5FA",
        barPercentage: 1.0,
        categoryPercentage: 1.0,
      },
    ],
  };
  const options = {
    indexAxis: "y",
    maintainAspectRatio: false,
    scales: {
      x: { stacked: true, display: false, max: total },
      y: { stacked: true, display: false },
    },
    plugins: {
      legend: { display: false },
      tooltip: { enabled: false },
    },
  };
  return (
    <>
      <div className="recipe-card-macrobar">
        <Bar data={data} options={options} />
      </div>
      <div className="macro-legend">
        <div className="macro-item">
          <span className="macro-dot macro-dot--protein" />
          Białko <div className="macro-value">{protein}</div>
        </div>
        <div className="macro-item">
          <span className="macro-dot macro-dot--carbs" />
          Węglowodany <div className="macro-value">{carbs}</div>
          <div className="macro-sugar">w tym {sugar} cukru</div>
        </div>
        <div className="macro-item">
          <span className="macro-dot macro-dot--fat" />
          Tłuszcze <div className="macro-value">{fat}</div>
        </div>
      </div>
    </>
  );
}

export default MacroBar;
