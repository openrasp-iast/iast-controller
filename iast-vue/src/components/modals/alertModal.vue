<script setup lang="ts">
import { IconCheck } from '@tabler/icons-vue';
import { ref } from 'vue';

const props = defineProps({
    title: String,
    message: String,
    icon: String,
    type: String,
    show: Boolean,
    dismissCountDown: Number,
    duration: Number,
    onClose: Function,
    onDismissed: Function,
    dismissible: Boolean
})

let show = ref(props.show)
let dispalyStyle = ref("display: hiden")

if (props.show) {
    console.log(props.show);
    
    dispalyStyle.value = "display: block"
}


function onClose() {
    dispalyStyle.value = "display: hiden"
    show.value = false
}
</script>

<template>
    <div class="modal modal-blur show " tabindex="-1" role="dialog" aria-modal="true" :style="dispalyStyle">
        <div class="modal-dialog modal-sm modal-dialog-centered" role="document">
            <div class="modal-content">
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="onClose">
                </button>
                <div class="modal-status bg-success"></div>
                <div class="modal-body text-center py-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon mb-2 text-green icon-lg" width="24" height="24"
                        viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round"
                        stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                        <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"></path>
                        <path d="M9 12l2 2l4 -4"></path>
                    </svg>
                    <h3>{{ title }}</h3>
                    <div class="text-secondary">
                        {{ message }}
                    </div>
                </div>
                <div class="modal-footer">
                    <div class="w-100">
                        <div class="row">
                            <div class="col"><a href="#" class="btn w-100" aria-disabled="true">
                                    Cancel
                                </a></div>
                            <div class="col"><a href="#" class="btn btn-primary w-100" data-bs-dismiss="modal">
                                    Delete 84 items
                                </a></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<style scoped></style>