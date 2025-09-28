import React from 'react'

// Simple inline SVG line chart without external deps
function LineChart({ series, labels, colors = ['#2563eb', '#f59e0b'] }) {
  const width = 800
  const height = 200
  const padding = 32
  const allValues = series.flat()
  const maxVal = Math.max(1, ...allValues)

  const scaleX = (i, n) => padding + (i * (width - 2 * padding)) / Math.max(1, n - 1)
  const scaleY = (v) => height - padding - (v * (height - 2 * padding)) / maxVal

  const pathFor = (arr) => arr.map((v, i) => `${i === 0 ? 'M' : 'L'} ${scaleX(i, arr.length)} ${scaleY(v)}`).join(' ')

  const yTicks = 4
  const ticks = Array.from({ length: yTicks + 1 }, (_, i) => Math.round((i * maxVal) / yTicks))

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="chart">
      {/* grid */}
      {ticks.map((t, i) => (
        <g key={i}>
          <line x1={padding} y1={scaleY(t)} x2={width - padding} y2={scaleY(t)} stroke="#e5e7eb" strokeWidth="1" />
          <text x={8} y={scaleY(t) + 4} fontSize="10" fill="#6b7280">{t.toLocaleString()}</text>
        </g>
      ))}

      {series.map((arr, idx) => (
        <path key={idx} d={pathFor(arr)} fill="none" stroke={colors[idx % colors.length]} strokeWidth="2" />
      ))}

      {/* legend */}
      <g transform={`translate(${padding}, ${padding - 12})`}>
        {labels.map((l, idx) => (
          <g key={idx} transform={`translate(${idx * 120}, 0)`}>
            <rect width="12" height="12" fill={colors[idx % colors.length]} rx="2" />
            <text x="16" y="10" fontSize="12" fill="#374151">{l}</text>
          </g>
        ))}
      </g>
    </svg>
  )
}

export default function Analytics({ engagementSeries }) {
  const likes = engagementSeries.likes || []
  const comments = engagementSeries.comments || []
  if (!likes.length && !comments.length) return null

  return (
    <section>
      <h2>Engagement Trend</h2>
      <LineChart series={[likes, comments]} labels={["Likes", "Comments"]} />
    </section>
  )
}
