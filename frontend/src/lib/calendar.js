export function generateICS(events) {
  const formatDate = (date) => {
    // Converts JS date → ICS datetime format (UTC)
    const d = new Date(date)
    return d.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z'
  }

  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//YourApp//EN',
  ]


  for (const event of events) {
    let start = event.start
    let end = event.end 
    start.setHours(23, 0, 0, 0, 0)
    end.setHours(23, 30, 0, 0, 0)
    lines.push('BEGIN:VEVENT')
    lines.push(`UID:${crypto.randomUUID()}`)
    lines.push(`DTSTAMP:${formatDate(new Date())}`)
    lines.push(`DTSTART:${formatDate(event.start)}`)
    lines.push(`DTEND:${formatDate(event.end)}`)
    lines.push(`SUMMARY:${event.title}`)
    if (event.description) lines.push(`DESCRIPTION:${event.description}`)
    lines.push('END:VEVENT')
  }

  lines.push('END:VCALENDAR')

  return lines.join('\r\n')
}
