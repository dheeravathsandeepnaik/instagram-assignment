const API_BASE = (import.meta?.env?.VITE_API_BASE || 'http://localhost:8000') + '/api'

async function handle(res) {
  if (!res.ok) {
    const text = await res.text()
    const err = new Error(text || 'Request failed')
    err.status = res.status
    throw err
  }
  return res.json()
}

export async function fetchProfile(username) {
  const res = await fetch(`${API_BASE}/profile/${encodeURIComponent(username)}`)
  return handle(res)
}

export async function fetchPosts(username) {
  const res = await fetch(`${API_BASE}/posts/${encodeURIComponent(username)}`)
  return handle(res)
}

export async function fetchReels(username) {
  const res = await fetch(`${API_BASE}/reels/${encodeURIComponent(username)}`)
  return handle(res)
}

export async function triggerScrape(username) {
  const res = await fetch(`${API_BASE}/scrape/${encodeURIComponent(username)}`, {
    method: 'POST'
  })
  return handle(res)
}
