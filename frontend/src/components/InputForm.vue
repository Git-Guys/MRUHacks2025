<template>
  <form
    class="space-y-4 p-6 max-w-lg mx-auto bg-gray-700 shadow-md rounded-md border border-violet-800"
    @submit.prevent="submitForm"
  >
    <div v-if="errorMessage != ''"
        class="bg-red-700 text-red-200 border border-red-200" 
    >
        {{errorMessage}}
    </div>
    <!-- Project Name -->
    <div>
      <label class="block font-medium text-gray-100">Project Name</label>
      <input
        v-model="form.projectName"
        type="text"
        class="w-full mt-1 p-2 border rounded-md bg-gray-800 text-white"
        placeholder="Enter project name"
      />
    </div>

    <!-- Start Date -->
    <div>
      <label class="block font-medium text-gray-100">Start Date</label>
      <input
        v-model="form.startDate"
        type="date"
        class="w-full mt-1 p-2 border rounded-md bg-gray-800 text-white"
      />
    </div>

    <!-- End Date -->
    <div>
      <label class="block font-medium text-gray-100">End Date</label>
      <input
        v-model="form.endDate"
        type="date"
        class="w-full mt-1 p-2 border rounded-md bg-gray-800 text-white"
      />
    </div>

    <!-- Description (only if no file chosen) -->
    <div v-if="!form.file">
      <label class="block font-medium text-gray-100">Description</label>
      <textarea
        v-model="form.description"
        class="w-full mt-1 p-2 border rounded-md bg-gray-800 text-white"
        rows="4"
        placeholder="Enter project description"
      ></textarea>
    </div>

    <!-- File Upload -->
    <div>
      <input
        ref="fileInput"
        type="file"
        accept=".pdf,.docx,.txt"
        @change="handleFileUpload"
        class="hidden"
      />

      <!-- Drop zone -->
      <div
        class="mt-2 border-2 border-dashed rounded-md p-6 text-center cursor-pointer transition hover:bg-gray-900"
        :class="dragOver ? 'border-violet-500 bg-gray-800' : 'border-gray-600'"
        @click="triggerFileSelect"
        @dragover.prevent="dragOver = true"
        @dragleave.prevent="dragOver = false"
        @drop.prevent="handleDrop"
      >
        <p v-if="!form.file" class="text-gray-200">
          Drag & drop a file here, or
          <span class="text-violet-300 underline">browse</span>
        </p>
        <p v-else class="font-semibold text-gray-100">
          Selected file: {{ form.file.name }}
        </p>
      </div>
    </div>
    <div v-if="errorMessage != ''"
        class="bg-red-700 text-red-200 border border-red-200" 
    >
        {{errorMessage}}
    </div>
    <!-- Submit -->
    <button
      type="submit"
      class="bg-violet-600 text-white px-4 py-2 rounded-md hover:bg-violet-700 transition"
    >
      Submit
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useEventStore } from "../stores/events.js"
const router = useRouter()
const fileInput = ref(null)
const dragOver = ref(false)
const errorMessage = ref("")
const today = new Date().toISOString().split('T')[0]

const form = ref({
  projectName: '',
  startDate: today,
  endDate: '',
  description: '',
  file: null,
})
const eventStore = useEventStore();
// 🔍 Validate file type
function validateFile(file) {
  const allowed = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
  ]
  if (!allowed.includes(file.type)) {
    alert('Only PDF, DOCX, or TXT files are allowed.')
    return false
  }
  return true
}

function triggerFileSelect() {
  fileInput.value.click()
}

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file && validateFile(file)) {
    form.value.file = file
    form.value.description = ''
  } else {
    form.value.file = null
  }
}

function handleDrop(event) {
  dragOver.value = false
  const file = event.dataTransfer.files[0]
  if (file && validateFile(file)) {
    form.value.file = file
    form.value.description = ''
  }
}

async function submitForm() {
  try {
    const { projectName, startDate, endDate, description, file } = form.value
    const formData = new FormData()
    formData.append('projectName', projectName)
    formData.append('startDate', startDate)
    formData.append('endDate', endDate)
    console.log(formData) 
    if (!file && description) {
      formData.append('description', description)
    }

    if (file) {
      formData.append('file', file)
    }

    const res = await fetch('https://mruhacks2025.onrender.com/test', {
      method: 'POST',
      body: formData,
    })

    if (!res.ok) {
      const text = await res.text()
      throw new Error(`Upload failed (${res.status}): ${text}`)
    }

    const result = await res.json()
    eventStore.projectName = projectName;
    eventStore.parseEvents(result) 
    console.log('✅ Upload success:', result)

    // Navigate to calendar route
    router.push({ name: 'calendar', state: { result } })
  } catch (err) {
    errorMessage.value = `Error: ${err}`
  }
}
</script>

