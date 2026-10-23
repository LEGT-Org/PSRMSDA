
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ApiFetch } from '@/api/Client'
import { Categories } from '@/services/state/InventoryReference'
import { GetCategories } from '@/services/useInventoryReference'

type ReportType = 'spare-parts' | 'service-requests'
type ExportFormat = 'csv' | 'excel' | 'pdf'

const exporting = ref<string | null>(null)
const errorMessage = ref('')

const sparePartSearch = ref('')
const categoryId = ref<number | ''>('')

const serviceRequestSearch = ref('')
const serviceRequestStatus = ref('')
const createdDate = ref('')

const statuses = [
    'Pending',
    'In Progress',
    'For Further Inspection',
    'Completed',
    'Unsuccessful',
]

const reports = [
    {
        type: 'spare-parts',
        title: 'Spare Parts Report',
        description: 'Export spare-part inventory and category information.',
        icon: '📦',
        formats: ['csv', 'excel', 'pdf'],
    },
    {
        type: 'service-requests',
        title: 'Service Requests Report',
        description: 'Export service requests, diagnoses, and requested parts.',
        icon: '🔧',
        formats: ['csv', 'excel', 'pdf'],
    },
] as const

onMounted(async () => {
    await GetCategories()
})

function buildQuery(reportType: ReportType): string {
    const params = new URLSearchParams()

    if (reportType === 'spare-parts') {
        if (sparePartSearch.value.trim()) {
            params.set('search', sparePartSearch.value.trim())
        }

        if (categoryId.value !== '') {
            params.set('category_id', String(categoryId.value))
        }
    } else {
        if (serviceRequestSearch.value.trim()) {
            params.set('search', serviceRequestSearch.value.trim())
        }

        if (serviceRequestStatus.value) {
            params.set('status', serviceRequestStatus.value)
        }

        if (createdDate.value) {
            params.set('created_date', createdDate.value)
        }
    }

    const query = params.toString()

    return query ? `?${query}` : ''
}

async function exportReport(
    reportType: ReportType,
    format: ExportFormat,
) {
    const key = `${reportType}-${format}`

    if (exporting.value) return

    exporting.value = key
    errorMessage.value = ''

    try {
        const response = await ApiFetch(
            `/reports/${reportType}/${format}${buildQuery(reportType)}`,
            { method: 'GET' },
        )

        if (!response.ok) {
            throw new Error(
                `Export failed. Server returned ${response.status}.`,
            )
        }

        const blob = await response.blob()

        const extension = format === 'excel' ? 'xlsx' : format
        const filename = `${reportType}.${extension}`
        const url = window.URL.createObjectURL(blob)

        const link = document.createElement('a')
        link.href = url
        link.download = filename

        document.body.appendChild(link)
        link.click()
        link.remove()

        window.URL.revokeObjectURL(url)
    } catch (error) {
        console.error('Report export failed:', error)

        errorMessage.value =
            error instanceof Error
                ? error.message
                : 'Unable to export the report. Please try again.'
    } finally {
        exporting.value = null
    }
}
</script>

<template>
    <div class="Reports-Page">
        <header class="Reports-Header">
            <div>
                <h1>Reports</h1>
                <p>Generate and download system reports.</p>
            </div>
        </header>

        <p
            v-if="errorMessage"
            class="Reports-Error"
            role="alert"
        >
            {{ errorMessage }}
        </p>

        <section class="Report-Card">
            <h2>Spare Parts Filters</h2>

            <div class="Report-Filters">
                <input
                    v-model="sparePartSearch"
                    type="search"
                    placeholder="Search spare parts..."
                />

                <select v-model="categoryId">
                    <option value="">All categories</option>

                    <option
                        v-for="category in Categories"
                        :key="category.id"
                        :value="category.id"
                    >
                        {{ category.name }}
                    </option>
                </select>
            </div>
        </section>

        <section class="Report-Card">
            <h2>Service Request Filters</h2>

            <div class="Report-Filters">
                <input
                    v-model="serviceRequestSearch"
                    type="search"
                    placeholder="Search service requests..."
                />

                <select v-model="serviceRequestStatus">
                    <option value="">All statuses</option>

                    <option
                        v-for="status in statuses"
                        :key="status"
                        :value="status"
                    >
                        {{ status }}
                    </option>
                </select>

                <input
                    v-model="createdDate"
                    type="date"
                    aria-label="Service request creation date"
                />
            </div>
        </section>

        <section class="Reports-Grid">
            <article
                v-for="report in reports"
                :key="report.type"
                class="Report-Card Report-Export-Card"
            >
                <div class="Report-Icon">
                    {{ report.icon }}
                </div>

                <h2>{{ report.title }}</h2>

                <p>{{ report.description }}</p>

                <div class="Report-Actions">
                    <button
                        v-for="format in report.formats"
                        :key="format"
                        type="button"
                        :disabled="exporting !== null"
                        @click="
                            exportReport(
                                report.type,
                                format,
                            )
                        "
                    >
                        {{
                            exporting === `${report.type}-${format}`
                                ? 'Exporting...'
                                : `Download ${format.toUpperCase()}`
                        }}
                    </button>
                </div>
            </article>
        </section>
    </div>
</template>