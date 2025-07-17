import { render } from 'solid-js/web'
import { Router, Route } from '@solidjs/router'
import './App.css'

import { Layout } from './components/layout/Layout'
import { NotFound } from './components/statuses/NotFound'
import { Home } from './components/home/Home'

const AppRouter = () => {
  return (
    <Router root={Layout}>
      <Route path="/" component={Home} />
      <Route path="*404" component={NotFound} />
    </Router>
  )
}

render(
  () => <AppRouter />,
  document.getElementById('app')!
)

