let baseEvents = [
  {
    title: 'Write project proposal',
    start: '2025-10-06',
    end: '2025-10-06',
  },
  {
    title: 'Design UI mockups',
    start: '2025-10-08',
    end: '2025-10-08',
  },
  {
    title: 'Backend API prototype',
    start: '2025-10-10',
    end: '2025-10-10',
  },
  {
    title: 'Team review meeting',
    start: '2025-10-12',
    end: '2025-10-12',
  },
  {
    title: 'Finalize documentation',
    start: '2025-10-15',
    end: '2025-10-15',
  },
  {
    title: 'Deployment deadline',
    start: '2025-10-20',
    end: '2025-10-20',
  }
]

const dateEvents = () => {
    return events.map(task => {
        const start = new Date(task.dueDate)
        const end = new Date(start)
        end.setHours(start.getHours() + 1) 
        return {
            title: task.name,
            start: start.toISOString(),
            end: end.toISOString()
        }
    })
}
baseEvents = dateEvents(baseEvents)
export {baseEvents}
