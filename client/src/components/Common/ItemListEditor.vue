<script setup lang="ts">
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { ref } from "vue";

interface Props {
    itemName?: String;
}

const props = withDefaults(defineProps<Props>(), {
    itemName: "item",
});

const emit = defineEmits<{
    (e: "onItems", doi: Array): void;
}>();

const items = ref([]);
const editIndex = ref(null);
const showForm = ref(false);
const currentItem = ref(null);
const currentItemError = ref(null);

function onAdd() {
    showForm.value = true;
}

function onEdit(index) {
    showForm.value = true;
    editIndex.value = index;
    currentItem.value = items.value[index];
}

function onRemove(index) {
    items.value.splice(index, 1);
    emit("onItems", items.value);
}

function onSave() {
    if (validate()) {
        if (isNewItem()) {
            items.value.push(currentItem.value);
        } else {
            items.value[editIndex.value] = currentItem.value;
        }
        resetForm();
        emit("onItems", items.value);
    }
}

function onReset() {
    resetForm();
}

function validate() {
    const item = currentItem.value;
    if (!item) {
        currentItemError.value = "Please provide a value";
        return false;
    }
    const foundIndex = items.value.indexOf(item);
    if (foundIndex > -1) {
        if (isNewItem() || (!isNewItem() && foundIndex != editIndex.value)) {
            currentItemError.value = `This ${props.itemName} has already been added`;
            return false;
        }
    }
    return true;
}

function isNewItem() {
    return editIndex.value === null;
}

function removeErrorMessage() {
    currentItemError.value = null;
}

function resetForm() {
    removeErrorMessage();
    editIndex.value = null;
    currentItem.value = null;
    showForm.value = false;
}
</script>

<template>
    <div>
        <div v-if="showForm">
            <b-input v-model="currentItem" :state="currentItemError ? false : null" @click="removeErrorMessage" />
            <div class="spacer"></div>
            <div v-if="currentItemError" class="error">{{ currentItemError }}</div>
            <b-button variant="primary" @click="onSave">Save</b-button>
            <b-button variant="danger" @click="onReset">Cancel</b-button>
        </div>
        <div v-else>
            <div v-if="items.length > 0">
                <div v-for="(item, index) in items" :key="index">
                    {{ item }}
                    <b-button
                        v-b-tooltip.hover
                        class="inline-icon-button"
                        variant="link"
                        size="sm"
                        :title="`Edit ${props.itemName}`"
                        @click="onEdit(index)">
                        <FontAwesomeIcon icon="edit" />
                    </b-button>
                    <b-button
                        v-b-tooltip.hover
                        class="inline-icon-button"
                        variant="link"
                        size="sm"
                        :title="`Remove ${props.itemName}`"
                        @click="onRemove(index)">
                        <FontAwesomeIcon icon="times" />
                    </b-button>
                </div>
            </div>
            <i>
                <a href="#" @click.prevent="onAdd()">Add a new {{ itemName }}</a>
            </i>
        </div>
    </div>
</template>

<style>
.error {
    color: red;
}
.spacer {
    padding: 5px;
}
</style>
