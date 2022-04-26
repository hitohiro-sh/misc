<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
import Calc from './components/Calc.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <HelloWorld msg="Hello!" />
    </div>
  </header>

  <main>
    <Calc />
  </main>
</template>

<style>
@import './assets/base.css';

#app {
  max-width: 1280px;
}
</style>
