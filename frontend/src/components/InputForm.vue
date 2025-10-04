<template>
  <form class="space-y-4 p-6 max-w-lg mx-auto bg-gray-700 shadow-md rounded-md border border-violet-800">
    <!-- Project Name -->
    <div>
      <label class="block font-medium">Project Name</label>
      <input
        v-model="form.projectName"
        type="text"
        class="w-full mt-1 p-2 border rounded-md"
        placeholder="Enter project name"
      />
    </div>

    <!-- Start Date -->
    <div>
      <label class="block font-medium">Start Date</label>
      <input
        v-model="form.startDate"
        type="date"
        class="w-full mt-1 p-2 border rounded-md"
      />
    </div>

    <!-- End Date -->
    <div>
      <label class="block font-medium">End Date</label>
      <input
        v-model="form.endDate"
        type="date"
        class="w-full mt-1 p-2 border rounded-md"
      />
    </div>

    <!-- Description (only if no file chosen) -->
    <div v-if="!form.file">
      <label class="block font-medium">Description</label>
      <textarea
        v-model="form.description"
        class="w-full mt-1 p-2 border rounded-md"
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
        :class="dragOver ? 'border-blue-700 bg-violet-100' : 'border-gray-300'"
        @click="triggerFileSelect"
        @dragover.prevent="dragOver = true"
        @dragleave.prevent="dragOver = false"
        @drop.prevent="handleDrop"
      >
        <p v-if="!form.file" class="text-white">
          Drag & drop a file here, or <span class="text-violet-300 underline">browse</span>
        </p>
        <p v-else class="font-semibold text-gray-200 font-medium">
          Selected file: {{ form.file.name }}
        </p>
      </div>

      <!-- File name display -->
      <p v-if="form.file" class="font-semibold text-sm text-gray-200 mt-2">
        Selected file: <span class="font-medium">{{ form.file.name }}</span>
      </p>
    </div>

    <!-- Submit -->
    <button
      type="button"
      @click="submitForm"
      class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
    >
      Submit
    </button>
  </form>
</template>

<script setup>
import { ref } from "vue"

const today = new Date().toISOString().split("T")[0]
const fileInput = ref(null);
const dragOver = ref(false)

const form = ref({
  projectName: "",
  startDate: today,
  endDate: "",
  description: "",
  file: null,
})

function validateFile(file) {
  const allowed = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
  ]
  if (!allowed.includes(file.type)) {
    alert("Only PDF, DOCX, or TXT files are allowed")
    return false
  }
  return true
}

function triggerFileSelect() {
  fileInput.value.click()
}

function handleDrop(event) {
  dragOver.value = false
  const file = event.dataTransfer.files[0]
  if (file && validateFile(file)) {
    form.value.file = file
    form.value.description = ""
  }
}
function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file) {
    // only allow PDF, DOCX, TXT
    const allowed = ["application/pdf", 
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                     "text/plain"]
    if (!allowed.includes(file.type)) {
      alert("Only PDF, DOCX, or TXT files are allowed")
      event.target.value = null
      form.value.file = null
      return
    }
    form.value.file = file
    // clear description if file exists
    form.value.description = ""
  } else {
    form.value.file = null
  }
}

function submitForm() {
  console.log("Form submitted:", form.value)
  // here you’d send via fetch/axios to backend
}
</script>

