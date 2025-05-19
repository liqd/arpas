import React from 'react'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'

import { ArcApp } from 'arpas-arc'
import { HashRouter } from 'react-router-dom'

function init () {
  ReactWidget.initialise('arpas', 'arc',
    function (el) {
      const props = el.dataset.attributes ? JSON.parse(el.dataset.attributes) : {}
      const root = createRoot(el)
      root.render(
        <React.StrictMode>
          <HashRouter>
            <ArcApp {...props} buttonClassName="btn btn--bg-tertiary btn--small" />
          </HashRouter>
        </React.StrictMode>
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
