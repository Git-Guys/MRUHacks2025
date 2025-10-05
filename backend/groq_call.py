from groq import Groq
from datetime import datetime, timedelta
import json
import os
import re

class GroqTaskBreakdown:
    def __init__(self, api_key=None):
        """
        Initialize with Groq API key
        """
        self.client = Groq(api_key=api_key or os.environ.get("GROQ_API_KEY"))
    
    def break_down_project(self, input_json):
        """
        Takes input JSON and returns task breakdown with specific deadline dates
        
        Input:
        {
          "project_name": "Website Redesign",
          "start_date": "2025-10-04",
          "end_date": "2025-12-15",
          "project_description": "Complete redesign..."
        }
        
        Output:
        {
          "tasks": [
            {"task": "Requirements gathering", "deadline": "2025-10-18"},
            {"task": "UI/UX design", "deadline": "2025-11-10"},
            ...
          ]
        }
        """
        
        # Calculate duration
        print(input_json['start_date'])
        start = datetime.strptime(input_json['start_date'], '%Y-%m-%d')
        end = datetime.strptime(input_json['end_date'], '%Y-%m-%d')
        total_days = (end - start).days
        
        # Create prompt
        prompt = f"""Break down this project into 5-10 specific, actionable tasks with day allocations.

Project: {input_json['project_name']}
Description: {input_json['project_description']}
Total Duration: {total_days} days
Start Date: {input_json['start_date']}
End Date: {input_json['end_date']}

Requirements:
1. Create a number of tasks appropriate to size and scope of the project and the comlexity of each given task.
2. No minimums or maximums for task amount
2. Each task needs a name and number of days
3. Days must sum to EXACTLY {total_days}
4. Tasks must be in chronological order
5. Be realistic with time allocations
6. Strictly adhere to the requirements of the project 
7. Do not assume any deliverables exist outside of the provided project description
8. Avoid grandular tasks
9. Keep tasks mid to high level depending on the scope and time of the project

Return ONLY this JSON format with NO markdown, NO explanations:
[
  {{"task": "Requirements gathering and stakeholder interviews", "days": 14}},
  {{"task": "UI/UX design and wireframing", "days": 21}},
  {{"task": "Frontend development", "days": 18}}
]

CRITICAL: The sum of all days values must equal exactly {total_days}. Start with [ and end with ]."""

        # Call Groq
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a project management API. Return only valid JSON arrays with no markdown formatting or explanations. The days field must sum to the exact total requested."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.2,
            max_tokens=2000,
        )
        
        # Get response
        response_text = chat_completion.choices[0].message.content.strip()
        
        # Clean markdown formatting
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        # Extract JSON array
        array_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if array_match:
            response_text = array_match.group()
        
        # Parse JSON
        try:
            tasks_with_days = json.loads(response_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from model: {e}\nResponse: {response_text}")
        
        # Validate structure
        if not isinstance(tasks_with_days, list) or len(tasks_with_days) == 0:
            raise ValueError(f"Expected non-empty list, got: {type(tasks_with_days)}")
        
        # Verify all tasks have required fields
        for idx, task in enumerate(tasks_with_days):
            if not isinstance(task, dict):
                raise ValueError(f"Task {idx} is not a dict: {task}")
            if 'task' not in task or 'days' not in task:
                raise ValueError(f"Task {idx} missing 'task' or 'days': {task}")
        
        # Normalize days to integers
        for task in tasks_with_days:
            task['days'] = int(task['days'])
        
        # Adjust to match exact total and ensure no task exceeds remaining time
        total_allocated = sum(t['days'] for t in tasks_with_days)
        
        if total_allocated != total_days:
            diff = total_days - total_allocated
            # Distribute the difference across tasks proportionally
            if diff > 0:
                # Add days to the largest task(s)
                tasks_with_days.sort(key=lambda x: x['days'], reverse=True)
                tasks_with_days[0]['days'] += diff
            else:
                # Remove days from the largest task(s)
                tasks_with_days.sort(key=lambda x: x['days'], reverse=True)
                tasks_with_days[0]['days'] += diff  # diff is negative
                if tasks_with_days[0]['days'] < 1:
                    tasks_with_days[0]['days'] = 1
                    # Redistribute if needed
                    remaining = total_days - sum(t['days'] for t in tasks_with_days)
                    if remaining != 0:
                        for task in tasks_with_days[1:]:
                            if remaining == 0:
                                break
                            adjustment = min(abs(remaining), task['days'] - 1)
                            if remaining > 0:
                                task['days'] += adjustment
                                remaining -= adjustment
                            else:
                                task['days'] -= adjustment
                                remaining += adjustment
        
        # Calculate deadline dates sequentially, ensuring last one ends on end_date
        output_tasks = []
        current_date = start
        days_accumulated = 0
        
        for i, task_info in enumerate(tasks_with_days):
            days_accumulated += task_info['days']
            
            # For the last task, ensure it ends exactly on the end date
            if i == len(tasks_with_days) - 1:
                task_deadline = end
            else:
                # Calculate deadline as start + accumulated days
                task_deadline = start + timedelta(days=days_accumulated)
                # Ensure we don't exceed end date
                if task_deadline > end:
                    task_deadline = end
            
            output_tasks.append({
                "task": task_info['task'],
                "deadline": task_deadline.strftime('%Y-%m-%d')
            })
        
        return {"tasks": output_tasks}


# Main Call
def groq_call(input_json):
    """
    Call Groq API to break down project into tasks
    Returns: dict with tasks and deadlines
    """
    breakdown = GroqTaskBreakdown(api_key=os.environ.get("GROQ_API_KEY"))
    
    try:
        result = breakdown.break_down_project(input_json)
        return result  # Return the dict, don't just print
        
    except Exception as e:
        # Log the error but raise it so Flask can handle it
        print(f"Error in groq_call: {e}")
        raise
