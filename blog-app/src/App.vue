<template>
  <div id="app">
    <!-- <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </nav>
    <router-view/> -->
    <!-- <NavBar /> -->
    <!-- <HomeView /> -->

    <router-view>
      <router-link to="/home">Home</router-link>
      <router-link to="/about">About</router-link>
    </router-view>
  </div>
</template>
<script>
export default {
  name: 'app',
}
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #f4f6f8;
  overflow-y: auto;
  height: 100vh;
}

nav {
  padding: 30px;
}


nav a.router-link-exact-active {
  font-weight: bold;
  color: #2c3e50;
}
</style>
