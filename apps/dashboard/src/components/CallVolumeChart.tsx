import type { ReactElement } from "react";
import type { HourlyVolume } from "../mock/standbyKpi";

interface CallVolumeChartProps {
  points: readonly HourlyVolume[];
}

export function CallVolumeChart({
  points,
}: CallVolumeChartProps): ReactElement {
  const max = Math.max(...points.map((item) => item.count), 1);
  const width = 560;
  const height = 160;
  const padX = 28;
  const padY = 18;
  const innerW = width - padX * 2;
  const innerH = height - padY * 2 - 18;
  const step = points.length > 1 ? innerW / (points.length - 1) : innerW;

  const coords = points.map((item, index) => {
    const x = padX + step * index;
    const y = padY + innerH * (1 - item.count / max);
    return { x, y, ...item };
  });
  const line = coords
    .map((point, index) => `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`)
    .join(" ");
  const area = `${line} L ${coords[coords.length - 1]?.x ?? padX} ${padY + innerH} L ${padX} ${padY + innerH} Z`;

  return (
    <figure className="volume-chart wrapup-card">
      <figcaption className="volume-chart-title">시간대별 통화량</figcaption>
      <svg
        className="volume-chart-svg"
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label="시간대별 통화량 mock 그래프"
      >
        <path className="volume-area" d={area} />
        <path className="volume-line" d={line} />
        {coords.map((point) => (
          <circle
            key={point.hour}
            className="volume-dot"
            cx={point.x}
            cy={point.y}
            r="3.5"
          />
        ))}
        {coords.map((point) => (
          <text
            key={`${point.hour}-label`}
            className="volume-hour"
            x={point.x}
            y={height - 4}
            textAnchor="middle"
          >
            {point.hour}
          </text>
        ))}
      </svg>
      <p className="wrapup-note">목업입니다. 실측 통화량이 아닙니다.</p>
    </figure>
  );
}
