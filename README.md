# MRUHacks2025 - PADJ BOPR Hackathon Project

## Inspiration
We noticed a common pain point in both academic and professional settings: people have big ideas, ambitious projects, or detailed assignments, but they often struggle to break them down into manageable pieces. It’s easy to feel overwhelmed when faced with a wall of requirements in a Word document, a dense PDF, or even just scattered notes. Instead of clear next steps, you’re left with stress and disorganization.

Our team wanted to create a tool that doesn’t just organize tasks—it links them together into a coherent execution plan, showing exactly when to work on what. That’s how **PADJ BOPR** was born: a smart planning assistant designed to take raw requirements and turn them into actionable, scheduled roadmaps.

## What it does
**PADJ BOPR** takes in project requirements—whether that’s a school assignment, a formal requirements document, or even a photo of handwritten notes—and uses a large language model to automatically break them down into dependency-linked subtasks.

- Subtasks are mapped onto a **calendar view**, showing the logical order of execution and recommended timeframes.
- Users can **drag and adjust tasks** across days, ensuring flexibility.
- Calendars can be **exported as ICS files**, making them easy to import into Gmail, Outlook, or any calendar application.

## How we built it
PADJ BOPR is a **full-stack web application**:

**Frontend:**  
- Built with **Vue**, **Tailwind CSS**, and **Vite** for a fast, modern, and responsive experience.  
- Users can upload documents, review generated subtasks, and interact with a drag-and-drop calendar.  
- Deployed on **Netlify** for reliability and speed.

**Backend:**  
- Developed with **Flask**, handling routing, API logic, and integration with external services.  

**AI Processing:**  
- Used **Groq** for LLM inference to quickly and accurately break down project requirements into dependency-based subtasks.

**File Parsing:**  
- Supports **Word documents, PDFs, plain text**, and even **handwritten notes** using parsing and OCR libraries.

**Hosting & Cloud:**  
- Backend deployed on **Render**, supporting scalable Flask hosting.

**Calendar Exporting:**  
- Subtasks are formatted into **universal ICS files**, compatible with all major calendar platforms.

## Challenges we ran into
- **Dependency logic:** Teaching the LLM to not just list subtasks, but capture dependencies and sequence them correctly.  
- **File support:** Handling PDFs, Word docs, and handwritten images introduced edge cases.  
- **Calendar integration:** Ensuring ICS files import cleanly across platforms.  
- **Deployment:** Coordinating frontend (Netlify) and backend (Render) introduced CORS and routing issues.  
- **ML model complexity:** Training a custom ML model was too complex, so we pivoted to using Groq.

## Accomplishments that we're proud of
- Transforming unstructured requirements into **structured, actionable subtasks**.  
- Supporting **multiple input formats**: Word, PDF, TXT, and handwritten images.  
- Building a **beautiful, responsive frontend** with Vue + Tailwind.  
- Seamlessly **exporting plans as ICS files**.  
- Overcoming technical hurdles in AI integration and backend deployment **under a tight hackathon timeline**.

## What we learned
- Balancing **AI-generated structure with user flexibility**.  
- The importance of **universal formats (ICS)** for interoperability.  
- Integrating modern frontend stacks (**Vue + Vite + Tailwind**) with a Python backend.  
- Critical **team communication** when dividing frontend, backend, and AI tasks.  
- Small **design touches**, like drag-and-drop subtasks, greatly improve UX.

## What's next for PADJ BOPR
- **Collaboration features:** Allow multiple users to generate shared project calendars.  
- **Direct calendar syncing:** Explore optional integration with Google Calendar and Outlook APIs.  
- **Progress tracking:** Add task completion tracking, reminders, and visual progress dashboards.  
- **Mobile support:** Build a mobile-friendly interface for managing tasks on the go.
