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

export default function PostsGrid({ posts }) {
  if (!posts?.length) return <div className="notice">No posts found</div>
  return (
    <div className="grid">
      {posts.map(p => (
        <article className="card" key={p.id}>
          <img className="media" src={p.image_url} alt={p.caption || 'post'} />
          <div className="card-body">
            <div className="metrics">
              <span>❤️ {p.likes.toLocaleString()}</span>
              <span>💬 {p.comments.toLocaleString()}</span>
              <span>🕒 {new Date(p.timestamp).toLocaleDateString()}</span>
            </div>
            {p.caption && <p className="caption">{p.caption}</p>}
            {p.analysis && (
              <div className="analysis">
                <Tags analysis={p.analysis} />
                <div className="vibe">Vibe: <strong>{p.analysis.vibe}</strong></div>
                <div className="quality">
                  <span>Lighting: {(p.analysis.quality_lighting * 100).toFixed(0)}%</span>
                  <span>Visual: {(p.analysis.quality_visual * 100).toFixed(0)}%</span>
                </div>
              </div>
            )}
          </div>
        </article>
      ))}
    </div>
  )
}
