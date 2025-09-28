import React from 'react'

export default function ProfileHeader({ influencer }) {
  if (!influencer) return null
  return (
    <section className="profile-header">
      <img className="avatar" src={influencer.profile_picture_url} alt={influencer.username} />
      <div className="meta">
        <div className="name-row">
          <h1>{influencer.name}</h1>
          <span className="handle">@{influencer.username}</span>
        </div>
        <div className="counts">
          <div><strong>{influencer.followers.toLocaleString()}</strong><span>Followers</span></div>
          <div><strong>{influencer.following.toLocaleString()}</strong><span>Following</span></div>
          <div><strong>{influencer.posts_count.toLocaleString()}</strong><span>Posts</span></div>
        </div>
      </div>
    </section>
  )
}
