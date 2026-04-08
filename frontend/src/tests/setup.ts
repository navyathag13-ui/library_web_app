/**
 * Vitest global setup — polyfills required by Vuetify in happy-dom.
 */

// Vuetify's VOverlay / VNavigationDrawer reads window.visualViewport
if (!window.visualViewport) {
  Object.defineProperty(window, 'visualViewport', {
    value: {
      width:        window.innerWidth,
      height:       window.innerHeight,
      offsetTop:    0,
      offsetLeft:   0,
      pageTop:      0,
      pageLeft:     0,
      scale:        1,
      addEventListener:    () => {},
      removeEventListener: () => {},
    },
    writable: true,
  })
}

// CSS.supports stub (used by some Vuetify internals in happy-dom)
if (typeof CSS === 'undefined' || !CSS.supports) {
  // @ts-ignore
  global.CSS = { supports: () => false }
}
