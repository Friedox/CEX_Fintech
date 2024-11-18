import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale, // For X-axis category scales
  LinearScale,   // For Y-axis linear scales
  BarElement,    // For bar charts
  PointElement,  // For scatter plots
  LineElement,   // For line charts
  Title,         // For chart titles
  Tooltip,       // For tooltips
  Legend         // For legends
);

export default ChartJS;