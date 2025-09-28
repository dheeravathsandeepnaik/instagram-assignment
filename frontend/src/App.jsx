import React, { useEffect, useMemo, useState } from 'react'
import { fetchProfile, fetchPosts, fetchReels, triggerScrape } from './api'
import ProfileHeader from './components/ProfileHeader'
import ProfileStats from './components/ProfileStats'
import PostsGrid from './components/PostsGrid'
import ReelsGrid from './components/ReelsGrid'
import Analytics from './components/Analytics'

const DEFAULT_USERNAME = 'demo_influencer'

export default function App() {
  const [username, setUsername] = useState(DEFAULT_USERNAME)
  const [profile, setProfile] = useState(null)
  const [posts, setPosts] = useState([])
  const [reels, setReels] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSearch = async (e) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const u = formData.get('username').trim()
    if (!u) return
    setUsername(u)
  }

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      setError('')
      try {
        let prof
        try {
          prof = await fetchProfile(username)
        } catch (err) {
          if (err?.status === 404) {
            // trigger mock scrape then refetch
            await triggerScrape(username)
            prof = await fetchProfile(username)
          } else {
            throw err
          }
        }
        setProfile(prof)
        const [pRes, rRes] = await Promise.all([
          fetchPosts(username),
          fetchReels(username)
        ])
        setPosts(pRes.posts || [])
        setReels(rRes.reels || [])
      } catch (err) {
        console.error(err)
        setError(err?.message || 'Failed to load data')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [username])

  const engagementSeries = useMemo(() => {
    if (!posts?.length) return { likes: [], comments: [] }
    const sorted = [...posts].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
    return {
      likes: sorted.map(p => p.likes),
      comments: sorted.map(p => p.comments)
    }
  }, [posts])

  return (
    <div className="container">
      <header className="topbar">
        <div className="brand">InfluenceScope</div>
        <form className="search" onSubmit={handleSearch}>
          <input name="username" placeholder="Enter Instagram username" defaultValue={username} />
          <button type="submit">Load</button>
        </form>
      </header>

      {loading && <div className="notice">Loading...</div>}
      {error && <div className="error">{error}</div>}

      {profile && (
        <>
          <ProfileHeader influencer={profile.influencer} />
          <ProfileStats profile={profile} />
          <Analytics engagementSeries={engagementSeries} />

          <section>
            <h2>Recent Posts</h2>
            <PostsGrid posts={posts} />
          </section>

          <section>
            <h2>Recent Reels</h2>
            <ReelsGrid reels={reels} />
          </section>
        </>
      )}

      <footer className="footer">Built with FastAPI + React (Vite)</footer>
    </div>
  )
}
