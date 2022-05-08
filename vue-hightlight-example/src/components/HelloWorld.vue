<script setup lang="ts">
import { ref } from "vue"

defineProps<{
    msg: string
}>()

</script>

<template>
  <div class="greetings">
    <h1>{{ msg }}</h1>
  </div>
</template>

<style scoped>

</style>
