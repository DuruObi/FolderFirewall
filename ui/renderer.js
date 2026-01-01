async function startSession() {
  const res = await fetch("http://localhost:8000/session/start", {
    method: "POST"
  })
  const data = await res.json()
  alert("Session started: " + data.session_id)
}
