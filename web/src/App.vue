<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header>
    <img
      alt="Vue logo"
      class="center-block"
      src="https://www.mythicalmysfits.com/images/mysfits_banner.gif"
      width="800"
      height="200"
    />
  </header>

  <RouterView />
</template>

<style scoped>
  
@media (min-width: 1024px) {
  header {
    display: block;
    width: 100%;
    place-items: center;
    text-align: center;
  }
}
</style>
