<script setup lang="ts">
import axios from "axios";
import { onMounted, ref } from "vue";

const datatypes = ref<any[]>([]);
const favoriteDatatypes = ref<any[]>([]);

onMounted(async () => {
    await loadDatatypes();
    await loadFavoriteDatatypes();
});

async function loadDatatypes() {
	const path = 'api/datatypes';
	try {
    	const response = await axios.get(path);
    	datatypes.value = response.data;
    } catch (error) {
    	console.error(error);
	}
}

async function loadFavoriteDatatypes() {
	const path = 'api/users/current/favorite_datatypes';
	try {
    	const response = await axios.get(path);
    	favoriteDatatypes.value = response.data.sort();
    } catch (error) {
    	console.error(error);
	}
}

async function mark(datatype) {
    const path = `api/users/current/favorite_datatypes/${datatype}`;
	try {
    	await axios.post(path);
        await loadFavoriteDatatypes();
    } catch (error) {
    	console.error(error);
	}
}

async function unmark(datatype) {
    const path = `api/users/current/favorite_datatypes/${datatype}`;
	try {
    	await axios.delete(path);
        await loadFavoriteDatatypes();
    } catch (error) {
    	console.error(error);
	}
}

</script>

<template>
	<div>
        <h1>Favorite Datatypes</h1>

        <ul>
        	<li v-for="dt in datatypes" :key="dt">
                {{ dt }}
                <a @click="unmark(dt)" href="#" v-if="favoriteDatatypes.indexOf(dt) >= 0" class="red">X</a>
                <a @click="mark(dt)" href="#" v-else class="green">+</a>
            </li>

    	</ul>

	</div>
</template>

<style>
.red {
    color: red;
}
.green {
    color: green;
}
</style>
