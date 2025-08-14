import ClerkProviderWithRoutes from './auth/ClerkProviderWithRoutes';
import {Routes, Route} from 'react-router-dom'
import {AuthenticationPage} from './auth/AuthenticationPage'
import {Layout} from './layout/Layout'
import {HistoryPanel} from './history/HistoryPanel'
import {ChallengeGenerator} from './challenge/ChallengeGenerator'

import './App.css'

function App() {
  // calling clerkProviderWithRoutes to wrap the routes  - it contains browser router and clerk provider
  // this is necessary to use clerk authentication with react router v6
  // wraping whole application under authentication by clerk.
  return <ClerkProviderWithRoutes>

      <Routes>

        <Route path = "/sign-in/*" element={<AuthenticationPage/>} />
        <Route path = "/sign-up/*" element={<AuthenticationPage/>} />
    
        <Route element = {<Layout/>}>
          <Route path = "/history" element={<HistoryPanel/>} />
          <Route path = "/" element={<ChallengeGenerator/>} />
        </Route>

      </Routes>

  </ClerkProviderWithRoutes>     
}

export default App
