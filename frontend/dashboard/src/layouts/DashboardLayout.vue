<template>
  <div class="dashboard-layout">
    <nav class="navbar">
      <div class="navbar-brand">
        <a class="navbar-item" href="/">
          EcoCharge
        </a>
      </div>
    </nav>
    <main class="main-content">
      <slot></slot>
    </main>
  </div>
</template>

<style scoped>
.dashboard-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.navbar {
  background-color: #f5f5f5;
  border-bottom: 1px solid #dbdbdb;
  padding: 0.5rem 1rem;
}

.navbar-brand {
  font-weight: bold;
}

.main-content {
  flex-grow: 1;
  padding: 2rem;
}
</style>
