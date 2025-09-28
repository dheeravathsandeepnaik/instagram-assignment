import React from 'react'

function Tags({ analysis }) {
  if (!analysis?.tags?.length) return null
  return (
    <div className="tags">
      {analysis.tags.map((t, i) => (
        <span key={i} className="tag">{t}</span>
      ))}
    </div>
  )
}

export default function ReelsGrid({ reels }) {
  if (!reels?.length) return <div className="notice">No reels found</div>
  return (
    <div className="grid">
      {reels.map(r => (
        <article className="card" key={r.id}>
          <img className="media" src={r.thumbnail_url} alt={r.caption || 'reel'} />
          <div className="card-body">
            <div className="metrics">
              <span>👀 {r.views.toLocaleString()}</span>
              <span>❤️ {r.likes.toLocaleString()}</span>
              <span>💬 {r.comments.toLocaleString()}</span>
              <span>🕒 {new Date(r.timestamp).toLocaleDateString()}</span>
            </div>
            {r.caption && <p className="caption">{r.caption}</p>}
            {r.analysis && (
              <div className="analysis">
                <Tags analysis={r.analysis} />
                <div className="vibe">Vibe: <strong>{r.analysis.vibe}</strong></div>
              </div>
            )}
          </div>
        </article>
      ))}
    </div>
  )
}
