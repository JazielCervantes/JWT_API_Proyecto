<template>
  <!-- Trigger button -->
  <button
    @click="open = true"
    class="hidden sm:flex items-center gap-3 px-3 py-2 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800/50 text-zinc-400 dark:text-zinc-500 text-sm hover:border-zinc-300 dark:hover:border-zinc-600 hover:text-zinc-500 dark:hover:text-zinc-400 transition-all duration-200 cursor-pointer min-w-[220px] focus:outline-none focus:ring-2 focus:ring-indigo-500/40"
    aria-label="Abrir paleta de comandos (Ctrl+K)"
  >
    <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/>
    </svg>
    <span class="flex-1 text-left">Buscar...</span>
    <kbd class="px-1.5 py-0.5 rounded-md bg-zinc-200/70 dark:bg-zinc-700 text-[11px] font-mono font-medium text-zinc-500 dark:text-zinc-400">Ctrl K</kbd>
  </button>

  <!-- Command Palette Modal -->
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="open" class="fixed inset-0 z-[100] flex items-start justify-center pt-[20vh]" role="dialog" aria-modal="true" aria-label="Paleta de comandos">
        <div class="fixed inset-0 bg-black/20 dark:bg-black/50 backdrop-blur-sm" @click="open = false"></div>
        <div class="relative w-full max-w-lg mx-4 bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-2xl dark:shadow-black/40 overflow-hidden" @click.stop>
          <!-- Search input -->
          <div class="flex items-center gap-3 px-4 border-b border-zinc-200 dark:border-zinc-700">
            <svg class="w-5 h-5 text-zinc-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/>
            </svg>
            <input
              ref="searchInput"
              v-model="query"
              type="text"
              placeholder="Escribe un comando o busca..."
              class="flex-1 py-4 bg-transparent text-sm text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 outline-none"
              @keydown.escape="open = false"
              @keydown.down.prevent="moveSelection(1)"
              @keydown.up.prevent="moveSelection(-1)"
              @keydown.enter.prevent="executeSelected"
              aria-label="Buscar comando"
              aria-activedescendant=""
            />
            <kbd class="px-1.5 py-0.5 rounded-md bg-zinc-100 dark:bg-zinc-800 text-[11px] font-mono text-zinc-400 dark:text-zinc-500">ESC</kbd>
          </div>
          <!-- Results -->
          <div class="max-h-[320px] overflow-y-auto p-2" role="listbox">
            <p v-if="filtered.length > 0" class="px-3 py-2 text-[11px] font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">
              {{ query ? 'Resultados' : 'Acciones rápidas' }}
            </p>
            <button
              v-for="(item, index) in filtered"
              :key="item.id"
              @click="execute(item)"
              @mouseenter="selectedIndex = index"
              role="option"
              :aria-selected="selectedIndex === index"
              class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-left transition-colors duration-100"
              :class="selectedIndex === index
                ? 'bg-indigo-50 dark:bg-indigo-500/10 text-indigo-700 dark:text-indigo-400'
                : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/70'"
            >
              <span class="w-8 h-8 rounded-lg flex items-center justify-center text-base flex-shrink-0"
                :class="selectedIndex === index
                  ? 'bg-indigo-100 dark:bg-indigo-500/20'
                  : 'bg-zinc-100 dark:bg-zinc-800'">
                {{ item.icon }}
              </span>
              <div class="flex-1 min-w-0">
                <p class="font-medium truncate">{{ item.label }}</p>
                <p v-if="item.desc" class="text-xs text-zinc-400 dark:text-zinc-500 truncate mt-0.5">{{ item.desc }}</p>
              </div>
              <span v-if="item.shortcut" class="text-xs text-zinc-400 dark:text-zinc-500 font-mono flex-shrink-0">{{ item.shortcut }}</span>
            </button>
            <div v-if="query && filtered.length === 0" class="px-3 py-8 text-center text-sm text-zinc-400 dark:text-zinc-500">
              <p class="text-2xl mb-2">🔍</p>
              No se encontraron resultados para "<span class="font-medium">{{ query }}</span>"
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'

const open = ref(false)
const query = ref('')
const selectedIndex = ref(0)
const searchInput = ref(null)

const API_URL = (typeof import.meta !== 'undefined' && import.meta.env?.PUBLIC_API_URL) || 'http://localhost:8000'

const commands = [
  { id: 'dashboard', label: 'Ir a Dashboard', desc: 'Panel principal', icon: '📊', action: () => navigateTo('/dashboard') },
  { id: 'products', label: 'Ir a Productos', desc: 'Catálogo de productos', icon: '📦', action: () => navigateTo('/products') },
  { id: 'profile', label: 'Ir a Mi Perfil', desc: 'Configuración de cuenta', icon: '👤', action: () => navigateTo('/profile') },
  { id: 'users', label: 'Ir a Usuarios', desc: 'Gestión de usuarios (admin)', icon: '👥', action: () => navigateTo('/users') },
  { id: 'theme', label: 'Cambiar tema', desc: 'Alternar entre modo claro y oscuro', icon: '🎨', action: toggleTheme },
  { id: 'docs', label: 'Abrir API Docs', desc: 'Documentación Swagger', icon: '📖', action: () => window.open(API_URL + '/docs', '_blank') },
  { id: 'home', label: 'Ir al Inicio', desc: 'Página principal', icon: '🏠', action: () => navigateTo('/') },
  { id: 'logout', label: 'Cerrar sesión', desc: 'Salir de tu cuenta', icon: '🚪', action: doLogout },
]

const filtered = computed(() => {
  if (!query.value) return commands
  const q = query.value.toLowerCase()
  return commands.filter(c =>
    c.label.toLowerCase().includes(q) ||
    (c.desc && c.desc.toLowerCase().includes(q))
  )
})

watch(filtered, () => { selectedIndex.value = 0 })

watch(open, async (val) => {
  if (val) {
    query.value = ''
    selectedIndex.value = 0
    document.body.style.overflow = 'hidden'
    await nextTick()
    searchInput.value?.focus()
  } else {
    document.body.style.overflow = ''
  }
})

function navigateTo(path) {
  window.location.href = path
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark')
  localStorage.setItem('theme', isDark ? 'dark' : 'light')
}

function doLogout() {
  if (typeof window !== 'undefined') {
    sessionStorage.clear()
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    window.location.href = '/login'
  }
}

function moveSelection(dir) {
  const len = filtered.value.length
  if (len === 0) return
  selectedIndex.value = (selectedIndex.value + dir + len) % len
}

function executeSelected() {
  if (filtered.value[selectedIndex.value]) {
    execute(filtered.value[selectedIndex.value])
  }
}

function execute(item) {
  open.value = false
  item.action()
}

function handleKeydown(e) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault()
    open.value = !open.value
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.fade-enter-active { transition: opacity 0.15s ease; }
.fade-leave-active { transition: opacity 0.1s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
