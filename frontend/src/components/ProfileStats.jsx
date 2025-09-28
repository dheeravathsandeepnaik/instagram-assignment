import React from 'react'

export default function ProfileStats({ profile }) {
  if (!profile) return null
  const { avg_likes, avg_comments, engagement_rate } = profile
  return (
    <section className="stats">
      <div className="stat">
        <div className="label">Avg Likes</div>
        <div className="value">{avg_likes.toLocaleString()}</div>
      </div>
      <div className="stat">
        <div className="label">Avg Comments</div>
        <div className="value">{avg_comments.toLocaleString()}</div>
      </div>
      <div className="stat">
        <div className="label">Engagement Rate</div>
        <div className="value">{engagement_rate.toFixed(2)}%</div>
      </div>
    </section>
  )
}
