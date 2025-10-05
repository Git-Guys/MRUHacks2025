<template>
    <form
        class="space-y-4 p-6 max-w-lg mx-auto bg-gray-700 shadow-md rounded-md border border-violet-800"
        @submit.prevent="submitForm"
    >
    <div v-if="errorMessage != ''"
        class="bg-red-700 text-red-200 border border-red-200 p-4" 
    >
        {{errorMessage}}
    </div>

    <div>
        <label class="block font-medium text-gray-100">Project Name</label>
        <input
            v-model="form.projectName"
            type="text"
            class="w-full mt-1 p-2 border rounded-md bg-gray-800 text-white w-fit"
            placeholder="Enter project name"
        />
    </div>

    <div>
        <label class="block font-medium text-gray-100">Start Date</label>
        <input
            v-model="form.startDate"
            type="date"
            class="w-full mt-1 p-2 border rounded-md bg-gray-800 text-white"
        />
    </div>

    <div>
        <label class="block font-medium text-gray-100">End Date</label>
        <input
            v-model="form.endDate"
            type="date"
            class="w-full mt-1 p-2 border rounded-md bg-gray-800 text-white"
        />
    </div>

    <div v-if="!form.file">
        <label class="block font-medium text-gray-100">Description</label>
        <textarea
            v-model="form.description"
            class="w-full mt-1 p-2 border rounded-md bg-gray-800 text-white"
            rows="4"
            placeholder="Enter project description"
        ></textarea>
    </div>

    <div>
        <input
            ref="fileInput"
            type="file"
            accept=".pdf,.docx,.txt,.png,.jpg,.jpeg,.heic,.heic,.bmp,.tiff,.webp"
            @change="handleFileUpload"
            class="hidden"
        />

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
                <div><strong>Valid types: </strong> .pdf .docx .txt .png .jpg .jpeg .heic .heif .bmp .tiff .webp</div>
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
        <div class="flex justify-end">
            <button
              type="submit"
              class="bg-violet-600 text-white px-4 py-2 rounded-md hover:bg-violet-700 transition"
            >
                Submit
            </button>
        </div>
  </form>
  <NConfigProvider :theme="darkTheme" :theme-overrides="themeOverides">
  <NModal class="bg-gray-900 text-white" :show="modalOpen" preset="dialog" title="Loading...">
    <div class="">
        <NSpin></NSpin>
    </div>
  </NModal>
  </NConfigProvider>
</template>


<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useEventStore } from "../stores/events.js"
import { NModal, NSpin, NConfigProvider, darkTheme } from "naive-ui"


const router = useRouter()
const fileInput = ref(null)
const dragOver = ref(false)
const errorMessage = ref("")

const today = new Date().toISOString().split('T')[0]

const modalOpen = ref(false)

//Overides for modal
const themeOverrides = {
    common: {
        primaryColor: '#7c3aed', 
    },
    Modal: {
        color: '#1e1b4b', 
        textColor: '#f3e8ff', 
        boxShadow: '0 0 20px rgba(124, 58, 237, 0.4)',
        borderRadius: '1rem'
    },
}

const form = ref({
    projectName: '',
    startDate: today,
    endDate: '',
    description: '',
    file: null,
})

const eventStore = useEventStore();

function validateFile(file) {
    const allowed = [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'image/jpeg',        
        'image/png',         
        'image/gif',         
        'image/webp',        
        'image/bmp',         
        'image/x-icon',      
        'image/tiff',        
        'image/heic',        
        'image/heif'        
    ]
    if (!allowed.includes(file.type)) {
        errorMessage.value = "Invalid File type" 
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
        if(!projectName){
            errorMessage.value = "Please enter a project name"
            return
        }
        else if(!startDate) {
            errorMessage.value = "Please enter a start date"
            return
        }else if(!endDate){
            errorMessage.value = "Please enter an end date"
            return
        }else if (!description && !file) {
            errorMessage.value = "Please provide a project description"
            return
        }
        const formData = new FormData()
        formData.append('projectName', projectName)
        formData.append('startDate', startDate)
        formData.append('endDate', endDate)

        if (!file && description) {
          formData.append('description', description)
        }

        if (file) {
          formData.append('file', file)
        }
        modalOpen.value = true //Open the loading dialog
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

        // Navigate to calendar route
        router.push({ name: 'calendar', state: { result } })
    } catch (err) {
        errorMessage.value = `Error: ${err}`
    }
    modalOpen.value = false;
}
</script>

